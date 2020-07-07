# Module: nightwatch
from .api import router, start, stop

from starlette_exporter import PrometheusMiddleware, handle_metrics
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pkg_resources

import os

WEBUI_ROOT =  os.getenv(
    "WEBUI_ROOT", "/app/nightwatch/webui")
API_ROOT = os.getenv("API_ROOT", "/api/v1")

tags_metadata = [
    {
        "name": "watch",
        "description": "This action endpoint is used to trigger an on-demand watch. A watch is a asynchronous operation to scan kubernetes cluster images."
    },
    {
        "name": "start",
        "description": "This action endpoint is used to start scheduled watch."
    },
    {
        "name": "stop",
        "description": "This action endpoint is used to start scheduled watch."
    },
    {
        "name": "status",
        "description": "Message containing the scheduled watch daemon status and the last watch timestamp."
    },
    {
        "name": "images",
        "description": "List of last watched images scan."
    },
    {
        "name": "outdated-images",
        "description": "List of last watched images scan containing a target tag."
    },
    {
        "name": "metrics",
        "description": "Expose API metrics at Prometheus openmetrics format."
    },
]

# Start web server
app = FastAPI(title="NightWatch",
                 description="Track freshly released docker images in a kubernetes cluster",
                 docs_url=API_ROOT,
                 openapi_tags=tags_metadata,
                 version=pkg_resources.require("nightwatch")[0].version)

# Fix CORS for local dev
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose prometheus metrics
app.add_middleware(PrometheusMiddleware, app_name="nightwatch", group_paths=True)
app.add_route("/metrics", handle_metrics)


# Expose api
app.include_router(router, prefix=API_ROOT)

# Expose statics files for webui
app.mount("/", StaticFiles(directory=WEBUI_ROOT, html=True), name="webui")


# Start nightwatch daemon before startup
@app.on_event("startup")
def startNightWatch():
    start()


# Stop nightwatch daemon before shutdown
@app.on_event("shutdown")
def shutdown_event():
    stop()
