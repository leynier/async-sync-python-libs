from fastapi import FastAPI

from .priori_way_with_types.router import router as priori_way_with_types_router
from .priori_way_without_types.router import router as priori_way_without_types_router
from .unasync_way.router import router as unasync_way_router

app = FastAPI()

app.include_router(priori_way_without_types_router, prefix="/priori_way_without_types")
app.include_router(priori_way_with_types_router, prefix="/priori_way_with_types")
app.include_router(unasync_way_router, prefix="/unasync_way")
