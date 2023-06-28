
from fastapi import APIRouter, FastAPI
from fastapi.routing import Mount

def mount_subapps(app: FastAPI, router: APIRouter):
    for route in router.routes:
        if not isinstance(route, Mount):
            continue
        app.mount(path = router.prefix + route.path, app = route.app, name = route.name)

def include_router(app: FastAPI, router: APIRouter):
    app.include_router(router)
    mount_subapps(app, router)
