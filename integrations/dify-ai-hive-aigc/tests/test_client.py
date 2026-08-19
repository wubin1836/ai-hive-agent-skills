import pathlib
import sys
import unittest


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from internal.ai_hive_client import AiHiveApiError, parse_json_object, summarize_task


class ClientHelpersTest(unittest.TestCase):
    def test_parse_json_object(self):
        self.assertEqual(parse_json_object('{"resolution":"1024x1024"}'), {"resolution": "1024x1024"})
        self.assertEqual(parse_json_object(""), {})

    def test_parse_json_rejects_arrays(self):
        with self.assertRaises(AiHiveApiError):
            parse_json_object("[]")

    def test_completed_task_summary(self):
        summary = summarize_task(
            {
                "taskId": "task-1",
                "taskType": "IMAGE",
                "items": [
                    {"status": "COMPLETED", "resultUrl": "https://example.com/a.png"},
                    {"status": "COMPLETED", "resultUrl": "https://example.com/b.png"},
                ],
            }
        )
        self.assertEqual(summary["status"], "COMPLETED")
        self.assertEqual(len(summary["result_urls"]), 2)

    def test_partial_task_summary(self):
        summary = summarize_task(
            {
                "id": "task-2",
                "items": [
                    {"status": "COMPLETED", "resultUrl": "https://example.com/a.mp4"},
                    {"status": "FAILED", "errorMessage": "failed"},
                ],
            }
        )
        self.assertEqual(summary["status"], "PARTIAL")
        self.assertEqual(summary["errors"], ["failed"])


if __name__ == "__main__":
    unittest.main()
