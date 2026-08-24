#!/usr/bin/env python3
"""AI Hive OpenAPI Skill — 通用 AI 能力调用工具。

封装 AI Hive OpenAPI 的文本聊天、图片生成、视频生成、模型查询、
媒体上传和任务轮询能力。通过 argparse 子命令调用。

依赖：requests（pip3 install requests）
"""

import argparse
import json
import os
import sys
import time
import webbrowser
from pathlib import Path

try:
    import requests
except ImportError:
    print("缺少依赖：requests。请运行 pip3 install requests", file=sys.stderr)
    sys.exit(1)


# === 常量 ===

DEFAULT_BASE_URL = "https://ai-hive.iclip.cn/api"
API_KEY_HELP_URL = "https://ai-hive.iclip.cn/chat"
CONFIG_FILE_PATH = os.path.expanduser("~/.ai-hive/config.json")
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Downloads/AiHive")
DEFAULT_TIMEOUT = 30  # HTTP 请求超时（秒）
DEFAULT_POLL_INTERVAL = 3  # 轮询间隔（秒）
DEFAULT_POLL_TIMEOUT = 1200  # 轮询总超时（秒），约 20 分钟

# 文件扩展名到 MIME 的映射（仅常见类型，最终以模型 videoConfig/imageConfig 为准）
MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
    ".tif": "image/tiff",
    ".heic": "image/heic",
    ".heif": "image/heif",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
}


# === 配置管理 ===

class Config:
    """三级优先级读取 API Key 和 Base URL：CLI > 环境变量 > 配置文件。"""

    def __init__(self, api_key=None, base_url=None, verbose=False):
        self.verbose = verbose
        self.api_key = self._resolve_api_key(api_key)
        self.base_url = self._resolve_base_url(base_url)

    def _resolve_api_key(self, cli_key):
        if cli_key:
            return cli_key
        env_key = os.environ.get("AI_HIVE_API_KEY")
        if env_key:
            return env_key
        file_config = self._read_config_file()
        if file_config.get("api_key"):
            return file_config["api_key"]
        raise SystemExit(
            "未找到 API Key。\n\n"
            "一键初始化（推荐）：\n"
            f"  python3 {sys.argv[0]} init --skill-name <skill-name>\n\n"
            "或按以下步骤手动获取：\n"
            f"  1. 访问 {API_KEY_HELP_URL}\n"
            "  2. 若未登录，会自动跳转到登录页，使用手机号 + 短信验证码登录\n"
            "  3. 登录后回到聊天页，点击左下角账户菜单（昵称旁下拉箭头，菜单向上展开）\n"
            "  4. 在下拉菜单中点击「API 接入」选项\n"
            "  5. 在「API Key 名称」输入框填写名称（例如：生产服务），点击「新建 API Key」\n"
            "  6. 在新建好的 API Key 卡片上点击「复制」按钮（格式：sk-api-*）\n\n"
            "配置方式（三选一）：\n"
            "  · 命令行参数：--api-key sk-api-xxxxx\n"
            "  · 环境变量：  export AI_HIVE_API_KEY=sk-api-xxxxx\n"
            f"  · 配置文件：  {CONFIG_FILE_PATH}"
        )

    def _resolve_base_url(self, cli_url):
        if cli_url:
            return cli_url.rstrip("/")
        env_url = os.environ.get("AI_HIVE_BASE_URL")
        if env_url:
            return env_url.rstrip("/")
        file_config = self._read_config_file()
        if file_config.get("base_url"):
            return file_config["base_url"].rstrip("/")
        return DEFAULT_BASE_URL

    @staticmethod
    def _read_config_file():
        try:
            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 防御性收紧权限：避免多用户系统下 API Key 被其他账号读取
            try:
                current_mode = os.stat(CONFIG_FILE_PATH).st_mode & 0o777
                if current_mode & 0o077:
                    os.chmod(CONFIG_FILE_PATH, 0o600)
            except OSError:
                pass
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def log(self, msg):
        if self.verbose:
            print(f"[verbose] {msg}", file=sys.stderr)


# === HTTP 客户端 ===

class AiHiveClient:
    """封装 AI Hive OpenAPI HTTP 调用。"""

    def __init__(self, config):
        self.config = config
        self.base = config.base_url
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        }

    def _url(self, path):
        return f"{self.base}/openapi/v1/{path}"

    def _request(self, method, url, **kwargs):
        self.config.log(f"{method} {url}")
        try:
            resp = requests.request(
                method, url, headers=self.headers, timeout=DEFAULT_TIMEOUT, **kwargs
            )
        except requests.exceptions.ConnectionError as e:
            raise SystemExit(
                f"无法连接到 API 服务器：{url}\n"
                f"原因：{e}\n"
                "请检查：网络是否正常 / Base URL 是否正确 / 是否需要代理"
            )
        except requests.exceptions.Timeout:
            raise SystemExit(
                f"API 请求超时（{DEFAULT_TIMEOUT}s）：{url}\n"
                "可稍后重试，或检查网络稳定性"
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"网络请求异常：{e}")
        if not resp.ok:
            try:
                detail = resp.json()
            except ValueError:
                detail = resp.text
            raise SystemExit(f"API 请求失败 ({resp.status_code}): {detail}")
        if resp.status_code == 204:
            return None
        return resp.json()

    # --- 业务端点 ---

    def get_user_info(self):
        return self._request("GET", self._url("user-info"))

    def list_models(self, model_type=None):
        params = {}
        if model_type:
            params["modelType"] = model_type
        return self._request("GET", self._url("models"), params=params)

    def find_model(self, public_model_id, model_type=None):
        """查询模型列表并找到指定 publicModelId 的模型。"""
        models = self.list_models(model_type)
        for m in models:
            if m.get("publicModelId") == public_model_id:
                return m
        raise SystemExit(f"未找到模型：{public_model_id}")

    def get_pricing_snapshot(self, model_entry, routing_mode):
        """从模型条目中提取指定路由模式的 pricingSnapshot。"""
        snapshots = model_entry.get("pricingSnapshot", [])
        for s in snapshots:
            if s.get("routingMode") == routing_mode:
                return s
        raise SystemExit(
            f"模型 {model_entry.get('publicModelId')} 不支持路由模式：{routing_mode}"
        )

    def create_upload_token(self, filename, content_type, size_bytes):
        body = {
            "filename": filename,
            "contentType": content_type,
            "sizeBytes": size_bytes,
        }
        return self._request("POST", self._url("media/upload-token"), json=body)

    def complete_upload(self, media_id):
        return self._request(
            "POST", self._url(f"media/{media_id}/complete")
        )

    def chat_text(self, public_model_id, routing_mode, messages, pricing_snapshot,
                  thinking_enabled=False):
        body = {
            "publicModelId": public_model_id,
            "routingMode": routing_mode,
            "messages": messages,
            "thinkingEnabled": thinking_enabled,
            "pricingSnapshot": pricing_snapshot,
        }
        return self._request("POST", self._url("chat/text"), json=body)

    def generate_image(self, public_model_id, routing_mode, prompt, pricing_snapshot,
                       batch_size=1, image_media_ids=None, params=None):
        body = {
            "publicModelId": public_model_id,
            "routingMode": routing_mode,
            "prompt": prompt,
            "batchSize": batch_size,
            "imageMediaIds": image_media_ids or [],
            "params": params or {},
            "pricingSnapshot": pricing_snapshot,
        }
        return self._request("POST", self._url("generation/image"), json=body)

    def generate_video(self, public_model_id, routing_mode, prompt, pricing_snapshot,
                       image_media_ids=None, video_media_ids=None, audio_media_ids=None,
                       first_frame_media_id=None, last_frame_media_id=None,
                       params=None):
        body = {
            "publicModelId": public_model_id,
            "routingMode": routing_mode,
            "prompt": prompt,
            "imageMediaIds": image_media_ids or [],
            "videoMediaIds": video_media_ids or [],
            "audioMediaIds": audio_media_ids or [],
            "params": params or {},
            "pricingSnapshot": pricing_snapshot,
        }
        if first_frame_media_id:
            body["firstFrameMediaId"] = first_frame_media_id
        if last_frame_media_id:
            body["lastFrameMediaId"] = last_frame_media_id
        return self._request("POST", self._url("generation/video"), json=body)

    def get_task(self, task_id):
        return self._request("GET", self._url(f"generation/tasks/{task_id}"))


# === 媒体上传流程 ===

def guess_mime(file_path):
    """根据扩展名推断 MIME 类型。"""
    ext = Path(file_path).suffix.lower()
    return MIME_MAP.get(ext, "application/octet-stream")


def upload_media(client, file_path):
    """三步上传：upload-token → PUT → complete。返回 mediaId。"""
    path = Path(file_path)
    if not path.is_file():
        raise SystemExit(f"文件不存在：{file_path}")

    filename = path.name
    content_type = guess_mime(str(path))
    size = path.stat().st_size

    print(f"[1/3] 创建上传凭证：{filename} ({content_type}, {size} bytes)")
    token = client.create_upload_token(filename, content_type, size)

    media_id = token["mediaId"]
    upload_url = token["upload"]["url"]
    upload_method = token["upload"].get("method", "PUT")
    upload_headers = token["upload"].get("headers", {})

    # PUT 到 OSS — 不携带 API Key，使用返回的 headers
    print(f"[2/3] 上传文件到对象存储...")
    with open(str(path), "rb") as f:
        try:
            oss_resp = requests.request(
                upload_method, upload_url, headers=upload_headers,
                data=f, timeout=300,
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(
                f"OSS 上传网络异常：{e}\n"
                "请检查网络连接或文件大小是否过大"
            )
    if not oss_resp.ok:
        try:
            detail = oss_resp.text
        except Exception:
            detail = "<无法读取响应>"
        raise SystemExit(f"OSS 上传失败 ({oss_resp.status_code}): {detail}")

    print(f"[3/3] 确认上传完成...")
    result = client.complete_upload(media_id)
    print(f"[ok] mediaId = {media_id}")
    return media_id


# === 文件下载 ===

def download_file(url, out_path, timeout=300):
    """流式下载文件，带进度条显示。"""
    print(f"[download] {out_path.name}")
    try:
        resp = requests.get(url, stream=True, timeout=timeout)
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        downloaded = 0
        with open(str(out_path), "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = int(downloaded * 100 / total)
                        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
                        print(f"\r  {bar} {pct}% ({downloaded // 1024}KB)", end="", flush=True)
        print()
        size_mb = downloaded / (1024 * 1024)
        print(f"[ok] {out_path} ({size_mb:.1f} MB)")
    except requests.exceptions.RequestException as e:
        print(f"\n[error] 下载失败: {e}", file=sys.stderr)


# === 任务轮询 ===

def poll_task(client, task_id, output_dir=DEFAULT_OUTPUT_DIR, no_download=False,
              timeout=DEFAULT_POLL_TIMEOUT, interval=DEFAULT_POLL_INTERVAL):
    """轮询任务直到全部子任务 COMPLETED 或 FAILED。"""
    deadline = time.time() + timeout
    last_progress = {}
    # 状态中文映射
    STATUS_CN = {
        "PENDING": "排队中",
        "QUEUED": "排队中",
        "RUNNING": "生成中",
        "COMPLETED": "已完成",
        "FAILED": "失败",
        "UNKNOWN": "未知",
    }

    while time.time() < deadline:
        task = client.get_task(task_id)
        items = task.get("items", [])
        all_done = True
        for item in items:
            status = item.get("status", "UNKNOWN")
            progress = item.get("progress")
            item_id = item.get("id", "?")
            key = f"{item_id}"
            if progress != last_progress.get(key):
                status_cn = STATUS_CN.get(status, status)
                print(f"  子任务 {item_id}: {status_cn}" +
                      (f" ({progress}%)" if progress is not None else ""))
                last_progress[key] = progress
            if status not in ("COMPLETED", "FAILED"):
                all_done = False

        if all_done:
            break
        time.sleep(interval)
    else:
        raise SystemExit(f"任务轮询超时（{timeout}s），taskId={task_id}")

    # 结果处理
    task = client.get_task(task_id)
    items = task.get("items", [])
    failed = [i for i in items if i.get("status") == "FAILED"]
    succeeded = [i for i in items if i.get("status") == "COMPLETED"]

    if failed:
        for item in failed:
            print(f"[failed] 子任务 {item.get('id')}: {item.get('errorMessage')}",
                  file=sys.stderr)

    if no_download:
        print(f"\n任务完成：{len(succeeded)} 成功, {len(failed)} 失败")
        print(json.dumps(task, ensure_ascii=False, indent=2))
        return

    if not succeeded:
        print("没有成功的子任务可下载", file=sys.stderr)
        return

    # 下载结果
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    task_type = task.get("taskType", "task")
    for i, item in enumerate(succeeded):
        result_url = item.get("resultUrl")
        if not result_url:
            continue
        ext = ".mp4" if "video" in task_type.lower() else ".png"
        filename = f"{task_type}_{task_id}_{i+1}{ext}"
        out_path = out_dir / filename
        download_file(result_url, out_path)

    # 尾帧
    for item in succeeded:
        last_frame = item.get("lastFrameUrl")
        if last_frame:
            out_path = out_dir / f"{task_type}_{task_id}_lastframe.png"
            download_file(last_frame, out_path)

    print(f"\n任务完成：{len(succeeded)} 成功, {len(failed)} 失败")


# === CLI 子命令处理 ===

def cmd_user_info(client, args):
    info = client.get_user_info()
    print(json.dumps(info, ensure_ascii=False, indent=2))


def cmd_models(client, args):
    models = client.list_models(args.type)
    if args.raw:
        print(json.dumps(models, ensure_ascii=False, indent=2))
        return
    for m in models:
        print(f"  {m.get('publicModelId', '?'):40s}  "
              f"{m.get('displayName', '?'):30s}  "
              f"{m.get('modelType', '?'):8s}  "
              f"路由: {', '.join(m.get('routingModes', []))}")


def cmd_chat(client, args):
    # 自动查询模型并提取 pricingSnapshot
    model_entry = client.find_model(args.model, "TEXT")
    pricing = client.get_pricing_snapshot(model_entry, args.mode)

    # 处理图片上传
    media_ids = []
    if args.image:
        for img_path in args.image:
            media_id = upload_media(client, img_path)
            media_ids.append(media_id)

    # 构造消息
    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system, "mediaIds": []})
    messages.append({
        "role": "user",
        "content": args.prompt,
        "mediaIds": media_ids,
    })

    result = client.chat_text(
        args.model, args.mode, messages, pricing,
        thinking_enabled=args.thinking,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_image(client, args):
    model_entry = client.find_model(args.model, "IMAGE")
    pricing = client.get_pricing_snapshot(model_entry, args.mode)

    # 上传参考图
    image_media_ids = []
    if args.image:
        for img_path in args.image:
            media_id = upload_media(client, img_path)
            image_media_ids.append(media_id)

    # 解析 --param key=value
    params = parse_params(args.param)

    result = client.generate_image(
        args.model, args.mode, args.prompt, pricing,
        batch_size=args.batch,
        image_media_ids=image_media_ids,
        params=params,
    )
    task_id = result.get("taskId")
    if not task_id:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"图片生成任务已提交：taskId = {task_id}")
    if args.no_download:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    poll_task(client, task_id, output_dir=args.output_dir,
              no_download=args.no_download)


def cmd_video(client, args):
    model_entry = client.find_model(args.model, "VIDEO")
    pricing = client.get_pricing_snapshot(model_entry, args.mode)

    # 上传媒体
    image_media_ids = []
    video_media_ids = []
    audio_media_ids = []
    first_frame_id = None
    last_frame_id = None

    if args.image:
        for p in args.image:
            image_media_ids.append(upload_media(client, p))
    if args.video:
        for p in args.video:
            video_media_ids.append(upload_media(client, p))
    if args.audio:
        for p in args.audio:
            audio_media_ids.append(upload_media(client, p))
    if args.first_frame:
        first_frame_id = upload_media(client, args.first_frame)
    if args.last_frame:
        last_frame_id = upload_media(client, args.last_frame)

    params = parse_params(args.param)

    result = client.generate_video(
        args.model, args.mode, args.prompt, pricing,
        image_media_ids=image_media_ids,
        video_media_ids=video_media_ids,
        audio_media_ids=audio_media_ids,
        first_frame_media_id=first_frame_id,
        last_frame_media_id=last_frame_id,
        params=params,
    )
    task_id = result.get("taskId")
    if not task_id:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"视频生成任务已提交：taskId = {task_id}")
    if args.no_download:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    poll_task(client, task_id, output_dir=args.output_dir,
              no_download=args.no_download)


def cmd_task(client, args):
    task = client.get_task(args.task_id)
    print(json.dumps(task, ensure_ascii=False, indent=2))


def cmd_upload(client, args):
    media_id = upload_media(client, args.file)
    print(f"\nmediaId: {media_id}")
    print("可将此 mediaId 传给 chat/image/video 命令的 --image 或 --video 参数")


# === 辅助函数 ===

def parse_params(param_list):
    """将 ['key=value', ...] 解析为 dict。"""
    if not param_list:
        return {}
    result = {}
    for p in param_list:
        if "=" not in p:
            raise SystemExit(f"参数格式错误（应为 key=value）：{p}")
        k, v = p.split("=", 1)
        # 尝试解析为数字
        try:
            v = int(v)
        except ValueError:
            try:
                v = float(v)
            except ValueError:
                pass
        result[k] = v
    return result


def add_common_args(parser):
    parser.add_argument("--api-key", help="AI Hive API Key (sk-api-*)")
    parser.add_argument("--base-url", help=f"API Base URL (默认 {DEFAULT_BASE_URL})")
    parser.add_argument("--verbose", action="store_true", help="详细日志")


# === CLI 入口 ===

def _try_read_existing_api_key():
    """安全读取已配置的 API Key，失败返回 None。"""
    env_key = os.environ.get("AI_HIVE_API_KEY")
    if env_key:
        return env_key
    try:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("api_key")
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def cmd_init(args):
    """交互式初始化 API Key 配置。"""
    # 1. 检查是否已配置
    existing = _try_read_existing_api_key()
    if existing:
        print(f"已检测到 API Key（{existing[:12]}...）")
        response = input("是否重新配置？(y/N): ").strip().lower()
        if response != "y":
            print("保持现有配置。")
            return

    # 2. 打开浏览器到聊天页（带 from=cli-skill 查询参数，为后端归因预留）
    skill_name = getattr(args, "skill_name", None) or "generic"
    url = f"{API_KEY_HELP_URL}?from=cli-skill&skill={skill_name}"
    print(f"正在打开浏览器：{url}")
    try:
        webbrowser.open(url)
    except Exception:
        print(f"无法自动打开浏览器，请手动访问：{url}")

    # 3. 引导文字
    print("\n" + "=" * 60)
    print("请在浏览器中完成以下操作：")
    print("  1. 若未登录，使用手机号 + 短信验证码登录（首次需同意协议）")
    print("  2. 登录后回到聊天页，点击左下角账户菜单（菜单向上展开）")
    print("  3. 点击「API 接入」")
    print("  4. 输入 Key 名称，点击「新建 API Key」")
    print("  5. 点击新建 Key 旁的「复制」按钮")
    print("=" * 60)

    # 4. 等待粘贴并写入配置
    while True:
        api_key = input("\n粘贴 API Key (sk-api-*): ").strip()
        if not api_key.startswith("sk-api-"):
            print("格式错误：API Key 应以 sk-api- 开头，请重新粘贴")
            continue
        if len(api_key) < 20:
            print("API Key 长度异常，请确认复制完整")
            continue
        break

    config_dir = os.path.dirname(CONFIG_FILE_PATH)
    os.makedirs(config_dir, exist_ok=True)
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump({"api_key": api_key, "base_url": DEFAULT_BASE_URL}, f, indent=2)
    os.chmod(CONFIG_FILE_PATH, 0o600)

    print(f"\n[ok] 已写入 {CONFIG_FILE_PATH}（权限 0600）")
    print(f"\n验证：python3 {sys.argv[0]} user-info")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ai_hive.py",
        description="AI Hive OpenAPI Skill — 通用 AI 能力调用工具",
    )
    add_common_args(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    # user-info
    p = sub.add_parser("user-info", help="查询用户信息和钱包余额")
    add_common_args(p)

    # models
    p = sub.add_parser("models", help="查询可用模型列表")
    p.add_argument("--type", choices=["TEXT", "IMAGE", "VIDEO"],
                   help="按类型筛选模型")
    p.add_argument("--raw", action="store_true", help="输出原始 JSON")
    add_common_args(p)

    # chat
    p = sub.add_parser("chat", help="文本聊天（支持多模态图片输入）")
    p.add_argument("--model", required=True, help="publicModelId")
    p.add_argument("--mode", default="COST_FIRST",
                   choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
                   help="路由模式（默认 COST_FIRST）")
    p.add_argument("prompt", help="用户提问内容")
    p.add_argument("--system", help="系统提示词")
    p.add_argument("--image", nargs="*", help="图片文件路径（可多张）")
    p.add_argument("--thinking", action="store_true", help="启用思考模式")
    add_common_args(p)

    # image
    p = sub.add_parser("image", help="图片生成")
    p.add_argument("--model", required=True, help="publicModelId")
    p.add_argument("--mode", default="COST_FIRST",
                   choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
                   help="路由模式")
    p.add_argument("prompt", help="图片描述")
    p.add_argument("--image", nargs="*", help="参考图路径（可多张）")
    p.add_argument("--batch", type=int, default=1, help="生成数量（默认 1）")
    p.add_argument("--param", nargs="*", help="模型参数 key=value（可多个）")
    p.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="输出目录")
    p.add_argument("--no-download", action="store_true", help="仅提交不等待下载")
    add_common_args(p)

    # video
    p = sub.add_parser("video", help="视频生成")
    p.add_argument("--model", required=True, help="publicModelId")
    p.add_argument("--mode", default="COST_FIRST",
                   choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
                   help="路由模式")
    p.add_argument("prompt", help="视频描述")
    p.add_argument("--image", nargs="*", help="参考图路径（可多张）")
    p.add_argument("--video", nargs="*", help="参考视频路径（可多个）")
    p.add_argument("--audio", nargs="*", help="参考音频路径（可多个）")
    p.add_argument("--first-frame", help="首帧图片路径")
    p.add_argument("--last-frame", help="尾帧图片路径")
    p.add_argument("--param", nargs="*", help="模型参数 key=value（可多个）")
    p.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="输出目录")
    p.add_argument("--no-download", action="store_true", help="仅提交不等待下载")
    add_common_args(p)

    # task
    p = sub.add_parser("task", help="查询生成任务状态")
    p.add_argument("--task-id", required=True, help="任务 ID")
    add_common_args(p)

    # upload
    p = sub.add_parser("upload", help="上传媒体文件，获得 mediaId")
    p.add_argument("--file", required=True, help="文件路径")
    add_common_args(p)

    # init — 交互式初始化
    p = sub.add_parser("init", help="交互式初始化 API Key 配置（推荐首次使用）")
    p.add_argument("--skill-name", default=None,
                   help="Skill 名称，用于来源归因（如 seedance-2-5）")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # init 不需要 API Key，提前处理（避免触发 Config 的 SystemExit）
    if args.command == "init":
        cmd_init(args)
        return

    # 通用参数可能在子命令上，也可能在顶层
    api_key = getattr(args, "api_key", None)
    base_url = getattr(args, "base_url", None)
    verbose = getattr(args, "verbose", False)

    config = Config(api_key=api_key, base_url=base_url, verbose=verbose)
    client = AiHiveClient(config)

    cmd_map = {
        "user-info": cmd_user_info,
        "models": cmd_models,
        "chat": cmd_chat,
        "image": cmd_image,
        "video": cmd_video,
        "task": cmd_task,
        "upload": cmd_upload,
    }

    handler = cmd_map.get(args.command)
    if not handler:
        parser.print_help()
        sys.exit(1)

    handler(client, args)





# === Skill 固定配置（由构建器生成） ===
SKILL_CONFIG = json.loads('{"example": "为AI商品图自动质检制作一张主体准确、层级清晰的商业图片", "keywords": "商品图质检,AI图片质检,电商图片审核,商品准确性,图片检查", "model": "public_model_gpt_image_2", "name": "product-image-quality-check-ai-hive", "rule": "optional", "search": "用真实参考逐项对照，不以美观代替商品准确", "title": "AI商品图自动质检"}')

def _validate_image_inputs(args):
    count = len(args.image or [])
    rule = SKILL_CONFIG.get("rule", "optional")
    if rule == "none" and count:
        raise SystemExit("此文生图 Skill 不接受参考图片")
    if rule == "image" and count < 1:
        raise SystemExit("此 Skill 必须提供至少一张 --image")
    if rule == "multi" and count < 2:
        raise SystemExit("多参考图 Skill 必须提供至少两张 --image")

def skill_generate(client, args):
    _validate_image_inputs(args)
    forwarded = argparse.Namespace(
        model=SKILL_CONFIG["model"], mode=args.routing,
        prompt=args.prompt, image=args.image, batch=args.batch,
        param=args.param, output_dir=args.output_dir,
        no_download=args.no_download, api_key=args.api_key,
        base_url=args.base_url, verbose=args.verbose,
    )
    print(f"模型：{forwarded.model}")
    cmd_image(client, forwarded)

def build_skill_parser():
    parser = argparse.ArgumentParser(
        prog="imagegen.py",
        description=SKILL_CONFIG["title"] + " — AI Hive 裸接口图片 Skill",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate", help="生成或编辑图片")
    p.add_argument("--prompt", required=True, help="图片描述或编辑要求")
    p.add_argument("--image", nargs="*", help="参考图片路径，可多张")
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--param", nargs="*", help="模型参数 key=value，可多个")
    p.add_argument("--routing", default="COST_FIRST", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"])
    p.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    p.add_argument("--no-download", action="store_true")
    add_common_args(p)
    p = sub.add_parser("task", help="查询生成任务")
    p.add_argument("--task-id", required=True)
    add_common_args(p)
    p = sub.add_parser("upload", help="上传图片")
    p.add_argument("--file", required=True)
    add_common_args(p)
    p = sub.add_parser("init", help="初始化 API Key")
    p.add_argument("--skill-name", default=SKILL_CONFIG["name"])
    return parser

def skill_main():
    args = build_skill_parser().parse_args()
    if args.command == "init":
        cmd_init(args)
        return
    config = Config(
        api_key=getattr(args, "api_key", None),
        base_url=getattr(args, "base_url", None),
        verbose=getattr(args, "verbose", False),
    )
    client = AiHiveClient(config)
    if args.command == "generate":
        skill_generate(client, args)
    elif args.command == "task":
        cmd_task(client, args)
    elif args.command == "upload":
        cmd_upload(client, args)

if __name__ == "__main__":
    skill_main()
