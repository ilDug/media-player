# from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, Header, Request, Response
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware
from core.middlewares import (
    req_validation_error_handler,
    dag_http_error_handler,
    mongo_error_handler,
)

from pymongo.errors import PyMongoError

app = FastAPI(root_path="/api")
# app = FastAPI(root_path="/")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "https://play.dag.lan",
    ],
    allow_methods=["OPTIONS", "POST", "PUT", "GET", "DELETE"],
    expose_headers=[
        "Origin",
        "Content-Type",
        "Set-Cookie",
        "X-Error",
        "X-Auth-Token",
        "Authorization",
    ],
    allow_headers=[
        "Origin",
        "Content-Type",
        "Set-Cookie",
        "X-Error",
        "Accept",
        "Authorization",
    ],
    # allow_headers=["*"],)
)

# app.add_middleware(IntegrityLogMiddleware)


app.add_exception_handler(RequestValidationError, req_validation_error_handler)
app.add_exception_handler(HTTPException, dag_http_error_handler)
app.add_exception_handler(PyMongoError, mongo_error_handler)

# app.include_router(reagents_acceptence_router)


# app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="static_media")


@app.get("/", response_class=PlainTextResponse)
async def root():
    now = datetime.now()
    return f"API SERVER RUNNING... FAST. Server time: {now} (isoformat: {datetime.isoformat(now)})"
