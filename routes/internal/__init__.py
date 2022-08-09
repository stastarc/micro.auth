from fastapi.routing import APIRouter
from . import auth, info

router = APIRouter(prefix='/internal')

router.include_router(auth.router)
router.include_router(info.router)