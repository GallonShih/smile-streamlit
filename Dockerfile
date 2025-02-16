# 使用輕量級 Python 基礎映像
FROM python:3.10-slim

# 設定環境變數，避免 Python 產生 .pyc 檔案
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 設定工作目錄
WORKDIR /app

# 複製專案檔案（排除 .dockerignore 內的內容）
COPY . /app

# 安裝相依套件
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit 預設 Port
EXPOSE 8501

# 執行 Streamlit 應用程式
CMD ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
