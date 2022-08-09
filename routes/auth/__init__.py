from fastapi.routing import APIRouter
from . import social, auth

router = APIRouter(prefix='/auth')

router.include_router(social.router)
router.include_router(auth.router)