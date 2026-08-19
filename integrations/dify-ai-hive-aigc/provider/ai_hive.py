from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from internal.ai_hive_client import AiHiveApiError, AiHiveClient


class AiHiveProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = str(credentials.get("api_key") or "").strip()
        base_url = str(credentials.get("base_url") or "https://ai-hive.iclip.cn/api").strip()
        if not api_key.startswith("sk-api-"):
            raise ToolProviderCredentialValidationError("AI Hive API Key 应以 sk-api- 开头。")

        try:
            AiHiveClient(api_key=api_key, base_url=base_url).get_user_info()
        except AiHiveApiError as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
