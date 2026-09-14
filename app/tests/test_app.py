"""app.py の動作確認テスト（標準ライブラリの unittest のみ・Flask のテストクライアントを使用）。

実行:
    python3 -m unittest discover -s tests -v
第5回では、このテストを GitHub Actions の CI で自動実行する。
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_returns_ok(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {"status": "ok"})

    def test_index_returns_html(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("MA-2 sample app", res.get_data(as_text=True))

    def test_add_appends_message(self):
        res = self.client.post("/add", data={"text": "テスト投稿"})
        self.assertEqual(res.status_code, 302)  # リダイレクト
        body = self.client.get("/").get_data(as_text=True)
        self.assertIn("テスト投稿", body)

    def test_add_ignores_empty_text(self):
        before = self.client.get("/").get_data(as_text=True).count("<li>")
        self.client.post("/add", data={"text": "   "})
        after = self.client.get("/").get_data(as_text=True).count("<li>")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
