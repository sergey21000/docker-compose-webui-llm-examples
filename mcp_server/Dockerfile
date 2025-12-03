FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim
WORKDIR /app
COPY requirements.txt .
ENV UV_SYSTEM_PYTHON=1
RUN uv pip install --no-cache-dir -r requirements.txt
COPY app/ .
EXPOSE 9000
CMD ["uv", "run", "main.py"]