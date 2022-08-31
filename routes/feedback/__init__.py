from fastapi.routing import APIRouter
from . import feedback

router = APIRouter(prefix='/feedback')
router.include_router(feedback.router)