from fastapi.routing import APIRouter
from . import info
from . import change

router = APIRouter(prefix='/user')

router.include_router(info.router)
router.include_router(change.router)
