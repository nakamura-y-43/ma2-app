# 第2回 完成版 Dockerfile
# 授業では上から1行ずつ書いていく。各行が1レイヤになる。

# 1) ベースイメージ: Python 3.12 の軽量版
FROM python:3.12-slim

# 2) コンテナ内の作業ディレクトリ（以降の COPY / RUN はここが基準）
WORKDIR /app

# 3) 依存だけを先にコピーしてインストールする
#    （ソースより前に置くのが重要。アプリを直しても、この層のキャッシュが効く）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) アプリのソースをコピー
COPY app.py .

# 5) このコンテナが待ち受けるポート（ドキュメントとしての宣言）
EXPOSE 5000

# 6) コンテナ起動時に実行するコマンド
CMD ["python", "app.py"]
