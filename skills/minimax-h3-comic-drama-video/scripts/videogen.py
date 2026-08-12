#!/usr/bin/env python3
"""AI Hive OpenAPI skill CLI for model lookup, media upload, generation, polling, and downloads."""

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
    print("Missing dependency: requests. Run: pip3 install requests", file=sys.stderr)
    sys.exit(1)




DEFAULT_BASE_URL = "https://ai-hive.iclip.cn/api"
API_KEY_HELP_URL = "https://ai-hive.iclip.cn/chat"
CONFIG_FILE_PATH = os.path.expanduser("~/.ai-hive/config.json")
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Downloads/AiHive")
DEFAULT_TIMEOUT = 30  
DEFAULT_POLL_INTERVAL = 3  
DEFAULT_POLL_TIMEOUT = 1200  


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




class Config:
    """Resolve API key and base URL from CLI, environment, or config file."""

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
            "No AI Hive API key was found. Run the init command, set "
            "AI_HIVE_API_KEY, pass --api-key, or create ~/.ai-hive/config.json."
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




class AiHiveClient:
    """AI Hive OpenAPI HTTP client."""

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
                f"Unable to connect to the API server: {url}\n"
                f"Reason: {e}\n"
                "Check the network, base URL, and proxy settings."
            )
        except requests.exceptions.Timeout:
            raise SystemExit(
                f"API request timed out ({DEFAULT_TIMEOUT}s）：{url}\n"
                "Retry later or check network stability."
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"Network request error: {e}")
        if not resp.ok:
            try:
                detail = resp.json()
            except ValueError:
                detail = resp.text
            raise SystemExit(f"API request failed ({resp.status_code}): {detail}")
        if resp.status_code == 204:
            return None
        return resp.json()

    

    def get_user_info(self):
        return self._request("GET", self._url("user-info"))

    def list_models(self, model_type=None):
        params = {}
        if model_type:
            params["modelType"] = model_type
        return self._request("GET", self._url("models"), params=params)

    def find_model(self, public_model_id, model_type=None):
        """Find a model by publicModelId in the live model list."""
        models = self.list_models(model_type)
        for m in models:
            if m.get("publicModelId") == public_model_id:
                return m
        raise SystemExit(f"Model not found: {public_model_id}")

    def get_pricing_snapshot(self, model_entry, routing_mode):
        """Read the pricing snapshot for the selected routing mode."""
        snapshots = model_entry.get("pricingSnapshot", [])
        for s in snapshots:
            if s.get("routingMode") == routing_mode:
                return s
        raise SystemExit(
            f"Model {model_entry.get('publicModelId')} does not support routing mode: {routing_mode}"
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




def guess_mime(file_path):
    """Infer a MIME type from the file extension."""
    ext = Path(file_path).suffix.lower()
    return MIME_MAP.get(ext, "application/octet-stream")


def upload_media(client, file_path):
    """Upload media with upload-token, object storage PUT, and completion steps."""
    path = Path(file_path)
    if not path.is_file():
        raise SystemExit(f"File not found: {file_path}")

    filename = path.name
    content_type = guess_mime(str(path))
    size = path.stat().st_size

    print(f"[1/3] Creating upload credentials: {filename} ({content_type}, {size} bytes)")
    token = client.create_upload_token(filename, content_type, size)

    media_id = token["mediaId"]
    upload_url = token["upload"]["url"]
    upload_method = token["upload"].get("method", "PUT")
    upload_headers = token["upload"].get("headers", {})

    
    print(f"[2/3] Uploading to object storage...")
    with open(str(path), "rb") as f:
        try:
            oss_resp = requests.request(
                upload_method, upload_url, headers=upload_headers,
                data=f, timeout=300,
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(
                f"Object storage upload network error: {e}\n"
                "Check the network connection and file size."
            )
    if not oss_resp.ok:
        try:
            detail = oss_resp.text
        except Exception:
            detail = "<unable to read response>"
        raise SystemExit(f"Object storage upload failed ({oss_resp.status_code}): {detail}")

    print(f"[3/3] Confirming upload...")
    result = client.complete_upload(media_id)
    print(f"[ok] mediaId = {media_id}")
    return media_id




def download_file(url, out_path, timeout=300):
    """Stream a result file with progress output."""
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
        print(f"\n[error] Download failed: {e}", file=sys.stderr)




def poll_task(client, task_id, output_dir=DEFAULT_OUTPUT_DIR, no_download=False,
              timeout=DEFAULT_POLL_TIMEOUT, interval=DEFAULT_POLL_INTERVAL):
    """Poll until every subtask is completed or failed."""
    deadline = time.time() + timeout
    last_progress = {}
    
    STATUS_CN = {
        "PENDING": "queued",
        "QUEUED": "queued",
        "RUNNING": "running",
        "COMPLETED": "completed",
        "FAILED": "failed",
        "UNKNOWN": "unknown",
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
                print(f"  subtask {item_id}: {status_cn}" +
                      (f" ({progress}%)" if progress is not None else ""))
                last_progress[key] = progress
            if status not in ("COMPLETED", "FAILED"):
                all_done = False

        if all_done:
            break
        time.sleep(interval)
    else:
        raise SystemExit(f"Task polling timed out ({timeout}s），taskId={task_id}")

    
    task = client.get_task(task_id)
    items = task.get("items", [])
    failed = [i for i in items if i.get("status") == "FAILED"]
    succeeded = [i for i in items if i.get("status") == "COMPLETED"]

    if failed:
        for item in failed:
            print(f"[failed] Subtask {item.get('id')}: {item.get('errorMessage')}",
                  file=sys.stderr)

    if no_download:
        print(f"\nTask complete: {len(succeeded)} succeeded, {len(failed)} failed")
        print(json.dumps(task, ensure_ascii=False, indent=2))
        return

    if not succeeded:
        print("No successful subtasks are available for download.", file=sys.stderr)
        return

    
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

    
    for item in succeeded:
        last_frame = item.get("lastFrameUrl")
        if last_frame:
            out_path = out_dir / f"{task_type}_{task_id}_lastframe.png"
            download_file(last_frame, out_path)

    print(f"\nTask complete: {len(succeeded)} succeeded, {len(failed)} failed")




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
              f"routes: {', '.join(m.get('routingModes', []))}")


def cmd_chat(client, args):
    
    model_entry = client.find_model(args.model, "TEXT")
    pricing = client.get_pricing_snapshot(model_entry, args.mode)

    
    media_ids = []
    if args.image:
        for img_path in args.image:
            media_id = upload_media(client, img_path)
            media_ids.append(media_id)

    
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

    
    image_media_ids = []
    if args.image:
        for img_path in args.image:
            media_id = upload_media(client, img_path)
            image_media_ids.append(media_id)

    
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

    print(f"Image generation submitted: taskId = {task_id}")
    if args.no_download:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    poll_task(client, task_id, output_dir=args.output_dir,
              no_download=args.no_download)


def cmd_video(client, args):
    model_entry = client.find_model(args.model, "VIDEO")
    pricing = client.get_pricing_snapshot(model_entry, args.mode)

    # Upload media
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

    print(f"Video generation submitted: taskId = {task_id}")
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
    print("Pass this mediaId to an image or video generation request.")




def parse_params(param_list):
    """Parse key=value items into a dictionary."""
    if not param_list:
        return {}
    result = {}
    for p in param_list:
        if "=" not in p:
            raise SystemExit(f"Invalid parameter; expected key=value: {p}")
        k, v = p.split("=", 1)
        
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
    parser.add_argument("--base-url", help=f"API Base URL (default {DEFAULT_BASE_URL})")
    parser.add_argument("--verbose", action="store_true", help="Verbose logs")



# === API key initialization ===

def _try_read_existing_api_key():
    """Read a configured API key safely, returning None when unavailable."""
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
    """Initialize the API key interactively."""
    existing = _try_read_existing_api_key()
    if existing:
        print(f"Existing API key detected ({existing[:12]}...)")
        if input("Reconfigure it? (y/N): ").strip().lower() != "y":
            print("Keeping the existing configuration.")
            return

    skill_name = getattr(args, "skill_name", None) or "generic"
    url = f"{API_KEY_HELP_URL}?from=cli-skill&skill={skill_name}"
    print(f"Opening browser: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        print(f"Could not open a browser automatically. Visit: {url}")

    print("\n" + "=" * 64)
    print("In the AI Hive web app:")
    print("  1. Sign in with the available account method.")
    print("  2. Open the account menu in the lower-left corner.")
    print("  3. Open API Access.")
    print("  4. Create a named API key.")
    print("  5. Copy the full key, which starts with sk-api-.")
    print("=" * 64)

    while True:
        api_key = input("\nPaste the API key (sk-api-*): ").strip()
        if not api_key.startswith("sk-api-"):
            print("Invalid format: the API key must start with sk-api-.")
            continue
        if len(api_key) < 20:
            print("The API key looks incomplete. Paste the full key.")
            continue
        break

    config_dir = os.path.dirname(CONFIG_FILE_PATH)
    os.makedirs(config_dir, exist_ok=True)
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump({"api_key": api_key, "base_url": DEFAULT_BASE_URL}, f, indent=2)
    os.chmod(CONFIG_FILE_PATH, 0o600)
    print(f"\n[ok] Wrote {CONFIG_FILE_PATH} with permissions 0600.")


SKILL_CONFIG = json.loads("{\"models\": {\"i2v\": \"public_model_minimax_h3_i2v\", \"r2v\": \"public_model_minimax_h3_r2v\", \"t2v\": \"public_model_minimax_h3_t2v\"}, \"name\": \"minimax-h3-comic-drama-video\", \"rule\": \"optional\", \"title\": \"MiniMax H3 Comic Drama Video\"}")

def _validate_video_inputs(args, rule):
    has_image = bool(args.image)
    has_video = bool(args.video)
    has_audio = bool(args.audio)
    has_first = bool(args.first_frame)
    has_last = bool(args.last_frame)
    if rule == "none" and any((has_image, has_video, has_audio, has_first, has_last)):
        raise SystemExit("This text-to-video skill does not accept media inputs.")
    if rule == "first" and not has_first:
        raise SystemExit("Image-to-video requires --first-frame.")
    if rule == "first_last" and not (has_first and has_last):
        raise SystemExit("First-and-last-frame video requires both --first-frame and --last-frame.")
    if rule == "reference" and not any((has_image, has_video, has_audio)):
        raise SystemExit("Reference-to-video requires at least one --image, --video, or --audio input.")
    if rule == "image" and not has_image:
        raise SystemExit("Image-reference video requires --image.")
    if rule in ("video", "edit", "extend") and not has_video:
        raise SystemExit("This skill requires --video.")
    if rule == "audio" and not has_audio:
        raise SystemExit("Audio-reference video requires --audio.")

def _select_video_mode(args):
    modes = SKILL_CONFIG["models"]
    fixed = SKILL_CONFIG.get("fixed_mode")
    if fixed:
        return fixed
    if args.mode:
        return args.mode
    if args.first_frame:
        return "i2v"
    if args.image or args.video or args.audio:
        return "r2v"
    return "t2v"

def skill_generate(client, args):
    mode = _select_video_mode(args)
    if mode not in SKILL_CONFIG["models"]:
        raise SystemExit(f"This skill does not support mode: {mode}")
    rule = SKILL_CONFIG.get("rule", "optional")
    _validate_video_inputs(args, rule)
    params = list(args.param or [])
    if mode == "extend":
        params.append(f"extendDirection={args.extend_direction}")
    forwarded = argparse.Namespace(
        model=SKILL_CONFIG["models"][mode], mode=args.routing,
        prompt=args.prompt, image=args.image, video=args.video,
        audio=args.audio, first_frame=args.first_frame,
        last_frame=args.last_frame, param=params,
        output_dir=args.output_dir, no_download=args.no_download,
        api_key=args.api_key, base_url=args.base_url, verbose=args.verbose,
    )
    print(f"Mode: {mode} → {forwarded.model}")
    cmd_video(client, forwarded)

def build_skill_parser():
    parser = argparse.ArgumentParser(
        prog="videogen.py",
        description=SKILL_CONFIG["title"] + " — AI Hive OpenAPI video skill",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate", help="Generate video")
    p.add_argument("--mode", choices=list(SKILL_CONFIG["models"]), help="Generation mode; capability skills already set it")
    p.add_argument("--prompt", required=True, help="Video description")
    p.add_argument("--image", nargs="*", help="Reference image paths")
    p.add_argument("--video", nargs="*", help="Reference video paths")
    p.add_argument("--audio", nargs="*", help="Reference audio paths")
    p.add_argument("--first-frame", help="First-frame image path")
    p.add_argument("--last-frame", help="Last-frame image path")
    p.add_argument("--param", nargs="*", help="Model parameters as key=value")
    p.add_argument("--extend-direction", choices=["forward", "backward"], default="backward")
    p.add_argument("--routing", default="COST_FIRST", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"])
    p.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    p.add_argument("--no-download", action="store_true")
    add_common_args(p)
    p = sub.add_parser("task", help="Query generation task")
    p.add_argument("--task-id", required=True)
    add_common_args(p)
    p = sub.add_parser("upload", help="Upload media")
    p.add_argument("--file", required=True)
    add_common_args(p)
    p = sub.add_parser("init", help="Initialize API key")
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
