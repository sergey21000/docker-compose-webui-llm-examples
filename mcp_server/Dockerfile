FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim
WORKDIR /app
ENV UV_SYSTEM_PYTHON=1
COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt
COPY app/ .
EXPOSE 9000
CMD ["uv", "run", "main.py"]
