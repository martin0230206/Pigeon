import http
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from libs import email


@asynccontextmanager
async def lifespan(app: FastAPI):
    # region 啟動時執行
    logger.info('API docs 請造訪: http://127.0.0.1:24048/docs ')
    # endregion

    yield
    # region 終止時執行
    ...
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
    email.router,
    prefix="/Email",
    tags=["電子郵件"]
)
