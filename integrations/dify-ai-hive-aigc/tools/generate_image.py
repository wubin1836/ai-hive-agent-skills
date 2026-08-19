from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from internal.ai_hive_client import (
    AiHiveApiError,
    AiHiveClient,
    parse_json_object,
    summarize_task,
)


class GenerateImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            prompt = str(tool_parameters.get("prompt") or "").strip()
            if not prompt:
                raise AiHiveApiError("请填写图片生成或编辑要求。")

            client = AiHiveClient(
                api_key=str(self.runtime.credentials["api_key"]),
                base_url=str(self.runtime.credentials.get("base_url") or "https://ai-hive.iclip.cn/api"),
            )
            uploaded = client.upload_dify_files(tool_parameters.get("reference_images") or [])
            submitted = client.submit_image(
                public_model_id=str(tool_parameters.get("model") or "public_model_nano_banana_pro"),
                prompt=prompt,
                routing_mode=str(tool_parameters.get("routing_mode") or "COST_FIRST"),
                batch_size=max(1, min(4, int(tool_parameters.get("batch_size") or 1))),
                image_media_ids=[item.media_id for item in uploaded],
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
                    "task_type": "IMAGE",
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
                yield self.create_image_message(url)
            if not summary["result_urls"]:
                yield self.create_text_message(f"任务已提交：{task_id}，状态：{summary['status']}")
        except AiHiveApiError as exc:
            yield self.create_text_message(f"AI Hive 图片任务失败：{exc}")
