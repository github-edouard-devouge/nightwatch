from .models import Image
from .nightwatch import NightWatch

import os
from starlette.responses import JSONResponse, Response
from starlette_exporter import handle_metrics
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from typing import List
from uuid import UUID
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY

nw = NightWatch()
router = APIRouter()


@router.get("/metrics", tags=["metrics"])
def metrics():
    registry = REGISTRY
    if 'prometheus_multiproc_dir' in os.environ:
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)

    headers = {'Content-Type': CONTENT_TYPE_LATEST}
    return Response(generate_latest(registry), status_code=200, headers=headers)


@router.get("/status", tags=["status"])
def status():
    return JSONResponse(status_code=200, content=jsonable_encoder({"last_watch": nw.watch_ts, "status": nw.status, "watching": nw.watching}))


@router.get("/start", tags=["start"])
def start():
    nw.start()
    return JSONResponse(status_code=200, content=jsonable_encoder({"message": "Scheduled watches daemon started."}))


@router.get("/stop", tags=["stop"])
def stop():
    nw.stop()
    return JSONResponse(status_code=200, content=jsonable_encoder({"message": "Scheduled watches daemon stopped."}))


@router.get("/watch", tags=["watch"])
def watch():
    nw.watch()
    return JSONResponse(status_code=200, content=jsonable_encoder({"message": "New watch started"}))


@router.get("/images/", tags=["images"], response_model=List[Image])
def getImages():
    return JSONResponse(status_code=200, content=jsonable_encoder(nw.images))


@router.get("/images/{image_uuid}", tags=["images"], response_model=Image)
def getImage(image_uuid: UUID):
    for image in nw.images:
        if image.uuid == image_uuid:
            return JSONResponse(status_code=200, content=jsonable_encoder(image))
    return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Image not found."}))


@router.get("/outdated-images/", tags=["outdated-images"], response_model=List[Image])
def getOutdatedImages():
    return JSONResponse(status_code=200, content=jsonable_encoder(nw.imagesToUpdate))
