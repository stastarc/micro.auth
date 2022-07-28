from fastapi.routing import APIRouter
from . import social

router = APIRouter(prefix='/auth')

router.include_router(social.router)