FROM python:3.12-slim

# システムの基本パッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# poetry のインストール
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# 作業ディレクトリ作成
WORKDIR /app

# Poetry 設定をプロジェクトディレクトリ優先にする
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# pyproject.toml と poetry.lock をコピーして依存関係をインストール
COPY README.md .
COPY pyproject.toml .
COPY poetry.lock* .
RUN poetry install --no-root


# アプリケーションのコードをコピー
# COPY . .
# COPY graphrag /app/graphrag

CMD ["bash"]
