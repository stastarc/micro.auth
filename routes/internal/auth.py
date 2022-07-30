from pydantic import BaseModel
from fastapi.routing import APIRouter

from auth.token import Token, TokenPayload

router = APIRouter(prefix='/auth')

class ValidBody(BaseModel):
    success: bool
    payload: TokenPayload | str

@router.get('/valid')
async def valid(
    key: str,
    check_active: bool=True
):
    succ, payload = Token.auth(key, check_active=check_active)

    return ValidBody(
        success=succ, 
        payload=payload
    )

