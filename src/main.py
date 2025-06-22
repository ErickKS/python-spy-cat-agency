from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.core.config_loader import settings

from src.domain.cat.controllers import router as cat_controllers
from src.domain.target.controllers import router as target_controllers
from src.domain.mission.controllers import router as mission_controllers

app = FastAPI()
if settings.BACKEND_CORS_ORIGINS:
  app.add_middleware(
    CORSMiddleware,
    # TODO: FIX CORS
    # allow_origins=[str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
  )

app.include_router(cat_controllers, prefix='/api', tags=['Cats'])
app.include_router(target_controllers, prefix='/api', tags=['Targets'])
app.include_router(mission_controllers, prefix='/api', tags=['Missions'])