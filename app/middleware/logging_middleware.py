"""全局 API 请求日志中间件：控制台 + 文件。"""
import logging
import os
import time
from datetime import datetime

from flask import Flask, g, request


def _setup_file_logger(log_dir: str, log_file: str) -> logging.Logger:
    """配置文件日志处理器。"""
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    logger = logging.getLogger("api_request")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def register_logging_middleware(app: Flask) -> None:
    """注册请求前后钩子，记录 API 访问日志。"""
    api_logger = _setup_file_logger(app.config["LOG_DIR"], app.config["LOG_FILE"])

    @app.before_request
    def _start_timer():
        g.request_start_time = time.perf_counter()

    @app.after_request
    def _log_request(response):
        # 仅记录 /api/ 路径
        if not request.path.startswith("/api/"):
            return response

        elapsed_ms = 0.0
        if hasattr(g, "request_start_time"):
            elapsed_ms = (time.perf_counter() - g.request_start_time) * 1000

        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if client_ip and "," in client_ip:
            client_ip = client_ip.split(",")[0].strip()

        log_msg = (
            f"time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
            f"method={request.method} "
            f"url={request.path} "
            f"query={request.query_string.decode('utf-8', errors='ignore')} "
            f"ip={client_ip} "
            f"status={response.status_code} "
            f"duration_ms={elapsed_ms:.2f}"
        )
        api_logger.info(log_msg)
        return response
