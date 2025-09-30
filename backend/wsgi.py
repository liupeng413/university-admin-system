# backend/wsgi.py
# 作为 Gunicorn 的入口：gunicorn backend.wsgi:app
from backend.app import app  # 确保 backend/app.py 里定义了 app = Flask(__name__)
