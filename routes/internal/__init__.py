from fastapi.routing import APIRouter
from . import auth

router = APIRouter(prefix='/internal')

router.include_router(auth.router)