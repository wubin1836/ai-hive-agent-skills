from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Iterable

import requests


DEFAULT_BASE_URL = "https://ai-hive.iclip.cn/api"
TERMINAL_STATUSES = {"COMPLETED", "FAILED"}


class AiHiveApiError(RuntimeError):
    """Raised when AI Hive returns an API, upload, or validation error."""


@dataclass(frozen=True)
class UploadedMedia:
    media_id: str
    mime_type: str


class AiHiveClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 30,
        session: requests.Session | None = None,
    ) -> None:
        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.base_url}/openapi/v1/{path.lstrip('/')}"

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        headers = dict(kwargs.pop("headers", {}))
        headers.setdefault("Authorization", f"Bearer {self.api_key}")
        headers.setdefault("Content-Type", "application/json")
        try:
            response = self.session.request(
                method,
                self._url(path),
                headers=headers,
                timeout=kwargs.pop("timeout", self.timeout),
                **kwargs,
            )
        except requests.RequestException as exc:
            raise AiHiveApiError(f"无法连接 AI Hive：{exc}") from exc

        if not response.ok:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise AiHiveApiError(f"AI Hive 请求失败（{response.status_code}）：{detail}")
        if response.status_code == 204:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise AiHiveApiError("AI Hive 返回了无法解析的响应。") from exc

    def get_user_info(self) -> dict[str, Any]:
        return self._request("GET", "user-info")

    def list_models(self, model_type: str | None = None) -> list[dict[str, Any]]:
        params = {"modelType": model_type} if model_type else None
        data = self._request("GET", "models", params=params)
        if not isinstance(data, list):
            raise AiHiveApiError("AI Hive 模型列表格式异常。")
        return data

    def find_model(self, public_model_id: str, model_type: str) -> dict[str, Any]:
        for model in self.list_models(model_type):
            if model.get("publicModelId") == public_model_id:
                return model
        raise AiHiveApiError(f"当前账户未找到模型：{public_model_id}")

    @staticmethod
    def pricing_snapshot(model: dict[str, Any], routing_mode: str) -> dict[str, Any]:
        for snapshot in model.get("pricingSnapshot", []):
            if snapshot.get("routingMode") == routing_mode:
                return snapshot
        raise AiHiveApiError(
            f"模型 {model.get('publicModelId', '')} 不支持路由模式 {routing_mode}。"
        )

    def upload_blob(self, filename: str, mime_type: str, blob: bytes) -> UploadedMedia:
        token = self._request(
            "POST",
            "media/upload-token",
            json={
                "filename": filename,
                "contentType": mime_type,
                "sizeBytes": len(blob),
            },
        )
        media_id = token.get("mediaId")
        upload = token.get("upload") or {}
        upload_url = upload.get("url")
        if not media_id or not upload_url:
            raise AiHiveApiError("AI Hive 未返回有效的素材上传凭证。")

        try:
            response = self.session.request(
                upload.get("method", "PUT"),
                upload_url,
                headers=upload.get("headers") or {},
                data=blob,
                timeout=300,
            )
        except requests.RequestException as exc:
            raise AiHiveApiError(f"素材上传失败：{exc}") from exc
        if not response.ok:
            raise AiHiveApiError(f"素材上传失败（{response.status_code}）。")

        self._request("POST", f"media/{media_id}/complete")
        return UploadedMedia(media_id=str(media_id), mime_type=mime_type)

    def upload_dify_files(self, files: Iterable[Any] | None) -> list[UploadedMedia]:
        uploaded: list[UploadedMedia] = []
        for index, file in enumerate(files or []):
            blob = getattr(file, "blob", None)
            if not isinstance(blob, bytes):
                raise AiHiveApiError("输入文件缺少可读取的二进制内容。")
            filename = (
                getattr(file, "filename", None)
                or getattr(file, "name", None)
                or f"upload-{index + 1}"
            )
            mime_type = getattr(file, "mime_type", None) or "application/octet-stream"
            uploaded.append(self.upload_blob(str(filename), str(mime_type), blob))
        return uploaded

    def submit_image(
        self,
        public_model_id: str,
        prompt: str,
        routing_mode: str,
        batch_size: int,
        image_media_ids: list[str],
        params: dict[str, Any],
    ) -> dict[str, Any]:
        model = self.find_model(public_model_id, "IMAGE")
        pricing = self.pricing_snapshot(model, routing_mode)
        return self._request(
            "POST",
            "generation/image",
            json={
                "publicModelId": public_model_id,
                "routingMode": routing_mode,
                "prompt": prompt,
                "batchSize": batch_size,
                "imageMediaIds": image_media_ids,
                "params": params,
                "pricingSnapshot": pricing,
            },
        )

    def submit_video(
        self,
        public_model_id: str,
        prompt: str,
        routing_mode: str,
        image_media_ids: list[str],
        video_media_ids: list[str],
        audio_media_ids: list[str],
        first_frame_media_id: str | None,
        last_frame_media_id: str | None,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        model = self.find_model(public_model_id, "VIDEO")
        pricing = self.pricing_snapshot(model, routing_mode)
        body: dict[str, Any] = {
            "publicModelId": public_model_id,
            "routingMode": routing_mode,
            "prompt": prompt,
            "imageMediaIds": image_media_ids,
            "videoMediaIds": video_media_ids,
            "audioMediaIds": audio_media_ids,
            "params": params,
            "pricingSnapshot": pricing,
        }
        if first_frame_media_id:
            body["firstFrameMediaId"] = first_frame_media_id
        if last_frame_media_id:
            body["lastFrameMediaId"] = last_frame_media_id
        return self._request("POST", "generation/video", json=body)

    def get_task(self, task_id: str) -> dict[str, Any]:
        return self._request("GET", f"generation/tasks/{task_id}")

    def wait_task(self, task_id: str, timeout_seconds: int = 600, interval: int = 3) -> dict[str, Any]:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            task = self.get_task(task_id)
            items = task.get("items") or []
            if items and all(str(item.get("status")) in TERMINAL_STATUSES for item in items):
                return task
            time.sleep(interval)
        raise AiHiveApiError(
            f"等待任务超时。任务仍可继续运行，请使用任务查询工具：{task_id}"
        )


def parse_json_object(value: Any, field_name: str = "params") -> dict[str, Any]:
    if value in (None, ""):
        return {}
    if isinstance(value, dict):
        return value
    try:
        data = json.loads(str(value))
    except json.JSONDecodeError as exc:
        raise AiHiveApiError(f"{field_name} 必须是有效的 JSON 对象。") from exc
    if not isinstance(data, dict):
        raise AiHiveApiError(f"{field_name} 必须是 JSON 对象。")
    return data


def summarize_task(task: dict[str, Any]) -> dict[str, Any]:
    items = task.get("items") or []
    statuses = [str(item.get("status", "UNKNOWN")) for item in items]
    if items and all(status == "COMPLETED" for status in statuses):
        status = "COMPLETED"
    elif items and all(s in TERMINAL_STATUSES for s in statuses):
        status = "PARTIAL" if "COMPLETED" in statuses else "FAILED"
    else:
        status = str(task.get("status") or (statuses[0] if len(set(statuses)) == 1 else "RUNNING"))

    result_urls = [
        str(item["resultUrl"])
        for item in items
        if item.get("status") == "COMPLETED" and item.get("resultUrl")
    ]
    last_frame_urls = [
        str(item["lastFrameUrl"])
        for item in items
        if item.get("lastFrameUrl")
    ]
    errors = [
        str(item.get("errorMessage"))
        for item in items
        if item.get("status") == "FAILED" and item.get("errorMessage")
    ]
    return {
        "task_id": str(task.get("taskId") or task.get("id") or ""),
        "task_type": str(task.get("taskType") or ""),
        "status": status,
        "result_urls": result_urls,
        "last_frame_urls": last_frame_urls,
        "errors": errors,
    }
