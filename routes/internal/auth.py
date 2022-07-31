from pydantic import BaseModel
from fastapi.routing import APIRouter

from auth.token import Token, TokenPayload

router = APIRouter(prefix='/auth')

class VerifyBody(BaseModel):
    success: bool
    payload: TokenPayload | str

@router.get('/verify')
async def verify(
    token: str,
    check_active: bool=True
):
    succ, payload = Token.auth(token, check_active=check_active)

    return VerifyBody(
        success=succ, 
        payload=payload
    )

