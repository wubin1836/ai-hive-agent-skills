from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from internal.ai_hive_client import AiHiveApiError, AiHiveClient, summarize_task


class QueryTaskTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            task_id = str(tool_parameters.get("task_id") or "").strip()
            if not task_id:
                raise AiHiveApiError("请填写 taskId。")
            client = AiHiveClient(
                api_key=str(self.runtime.credentials["api_key"]),
            )
            summary = summarize_task(client.get_task(task_id))
            summary["task_id"] = task_id
            yield self.create_variable_message("task_id", task_id)
            yield self.create_variable_message("status", summary["status"])
            yield self.create_variable_message("result_urls", summary["result_urls"])
            yield self.create_json_message(summary)
            for url in summary["result_urls"]:
                if any(url.lower().split("?")[0].endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp")):
                    yield self.create_image_message(url)
                else:
                    yield self.create_link_message(url)
        except AiHiveApiError as exc:
            yield self.create_text_message(f"AI Hive 任务查询失败：{exc}")
