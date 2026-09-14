"""MA-2 研修用の小さな Web アプリ（Flask）。

第2回でこのアプリを Dockerfile でイメージ化する。
第3回で PostgreSQL 版に差し替え、第4回以降で AWS へデプロイする。

- GET  /        メッセージ一覧を表示（HTML）
- POST /add     メッセージを追加してトップへリダイレクト
- GET  /health  ヘルスチェック（JSON）。ロードバランサが参照する
"""
import os

from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

# 第2回はデータベースを使わないので、メモリ上のリストに保持する。
# プロセスが終われば消える（コンテナを消すと消えるのと同じ）。第3回で DB に置き換える。
MESSAGES = ["ようこそ MA-2 へ", "このメッセージはコンテナの中で動いています"]

PAGE = """<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>MA-2 sample app</title></head>
<body style="font-family: sans-serif; max-width: 40em; margin: 2em auto;">
  <h1>MA-2 sample app</h1>
  <p>version: {{ version }} / host: {{ hostname }}</p>
  <ul>
    {% for m in messages %}<li>{{ m }}</li>{% endfor %}
  </ul>
  <form action="/add" method="post">
    <input name="text" placeholder="メッセージ" required>
    <button type="submit">追加</button>
  </form>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(
        PAGE,
        messages=MESSAGES,
        version=os.environ.get("APP_VERSION", "1.0"),
        hostname=os.environ.get("HOSTNAME", "unknown"),
    )


@app.post("/add")
def add():
    text = (request.form.get("text") or "").strip()
    if text:
        MESSAGES.append(text)
    return redirect("/")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # 0.0.0.0 で待ち受けないと、コンテナの外（ホスト）から届かない。
    app.run(host="0.0.0.0", port=5000)
