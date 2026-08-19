from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from internal.ai_hive_client import (
    AiHiveApiError,
    AiHiveClient,
    UploadedMedia,
    parse_json_object,
    summarize_task,
)


VIDEO_MODELS = {
    ("seedance_2_5", "t2v"): "public_model_seedance_2_5_t2v",
    ("seedance_2_5", "i2v"): "public_model_seedance_2_5_i2v",
    ("seedance_2_5", "r2v"): "public_model_seedance_2_5_r2v",
    ("seedance_2_5", "edit"): "public_model_seedance_2_5_video_edit",
    ("seedance_2_5", "extend"): "public_model_seedance_2_5_video_extend",
    ("minimax_h3", "t2v"): "public_model_minimax_h3_t2v",
    ("minimax_h3", "i2v"): "public_model_minimax_h3_i2v",
    ("minimax_h3", "r2v"): "public_model_minimax_h3_r2v",
    ("happyhorse", "t2v"): "public_model_happyhorse_t2v",
    ("happyhorse", "i2v"): "public_model_happyhorse_i2v",
    ("happyhorse", "r2v"): "public_model_happyhorse_r2v",
    ("happyhorse", "edit"): "public_model_happyhorse_video_edit",
}


def resolve_video_model(parameters: dict[str, Any]) -> str:
    custom = str(parameters.get("custom_public_model_id") or "").strip()
    if custom:
        if not custom.startswith("public_model_"):
            raise AiHiveApiError("自定义 publicModelId 应以 public_model_ 开头。")
        return custom
    key = (
        str(parameters.get("model_family") or "seedance_2_5"),
        str(parameters.get("generation_mode") or "t2v"),
    )
    model = VIDEO_MODELS.get(key)
    if not model:
        raise AiHiveApiError("所选模型暂不支持该生成模式，请更换模式或填写自定义 publicModelId。")
    return model


def split_media(items: list[UploadedMedia]) -> tuple[list[str], list[str], list[str]]:
    images: list[str] = []
    videos: list[str] = []
    audio: list[str] = []
    for item in items:
        if item.mime_type.startswith("image/"):
            images.append(item.media_id)
        elif item.mime_type.startswith("video/"):
            videos.append(item.media_id)
        elif item.mime_type.startswith("audio/"):
            audio.append(item.media_id)
        else:
            raise AiHiveApiError(f"不支持的参考素材类型：{item.mime_type}")
    return images, videos, audio


class GenerateVideoTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            prompt = str(tool_parameters.get("prompt") or "").strip()
            if not prompt:
                raise AiHiveApiError("请填写视频生成或编辑要求。")
            client = AiHiveClient(
                api_key=str(self.runtime.credentials["api_key"]),
                base_url=str(self.runtime.credentials.get("base_url") or "https://ai-hive.iclip.cn/api"),
            )

            references = client.upload_dify_files(tool_parameters.get("reference_files") or [])
            image_ids, video_ids, audio_ids = split_media(references)
            first = client.upload_dify_files(tool_parameters.get("first_frame") or [])
            last = client.upload_dify_files(tool_parameters.get("last_frame") or [])
            submitted = client.submit_video(
                public_model_id=resolve_video_model(tool_parameters),
                prompt=prompt,
                routing_mode=str(tool_parameters.get("routing_mode") or "COST_FIRST"),
                image_media_ids=image_ids,
                video_media_ids=video_ids,
                audio_media_ids=audio_ids,
                first_frame_media_id=first[0].media_id if first else None,
                last_frame_media_id=last[0].media_id if last else None,
                params=parse_json_object(tool_parameters.get("model_params"), "model_params"),
            )
            task_id = str(submitted.get("taskId") or "")
            if not task_id:
                raise AiHiveApiError("AI Hive 未返回任务 ID。")

            if bool(tool_parameters.get("wait_for_result", True)):
                task = client.wait_task(
                    task_id,
                    timeout_seconds=int(tool_parameters.get("timeout_seconds") or 600),
                )
                summary = summarize_task(task)
                summary["task_id"] = task_id
            else:
                summary = {
                    "task_id": task_id,
                    "task_type": "VIDEO",
                    "status": "SUBMITTED",
                    "result_urls": [],
                    "last_frame_urls": [],
                    "errors": [],
                }

            yield self.create_variable_message("task_id", task_id)
            yield self.create_variable_message("status", summary["status"])
            yield self.create_variable_message("result_urls", summary["result_urls"])
            yield self.create_json_message(summary)
            for url in summary["result_urls"]:
                yield self.create_link_message(url)
            if not summary["result_urls"]:
                yield self.create_text_message(f"任务已提交：{task_id}，状态：{summary['status']}")
        except AiHiveApiError as exc:
            yield self.create_text_message(f"AI Hive 视频任务失败：{exc}")
