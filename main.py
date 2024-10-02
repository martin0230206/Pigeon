import http
import time
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from tortoise import Tortoise

from libs import email_sender
from libs.config import CONFIG

sentry_sdk.init(
    dsn=CONFIG.sentry.dsn,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # region 啟動時執行
    logger.info('API docs 請造訪: http://127.0.0.1:24048/docs ')

    await Tortoise.init(CONFIG.mysql.connections)
    # endregion

    yield
    # region 終止時執行
    await Tortoise.close_connections()
    # endregion

# 建立 app 實例
app = FastAPI(
    title="Email Sender",
    description="寄信",
    version="VERSION 2024.02.17",  # VER: 版本號
    swagger_ui_parameters={
        # 在 API 文件上展開所有 schema 內容
        "defaultModelExpandDepth": 100,
    },
    lifespan=lifespan,  # 啟動時執行
)

# 解決 CORS 問題
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    """ 輸出 log 並加上響應處理時間(秒數)到 header
    """
    start_time = time.time()
    logger.debug(
        f"{request.method} {request.url} ...",
    )
    response = await call_next(request)
    logger.debug(
        f"{request.method} {request.url} {response.status_code} {http.client.responses[response.status_code]}",
    )
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(
    email_sender.router,
    prefix="/Email",
    tags=["電子郵件"]
)
