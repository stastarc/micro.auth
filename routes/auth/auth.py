from fastapi import Response
from fastapi.routing import APIRouter

from auth.token import Token

router = APIRouter()

@router.get('/verify')
async def verify(
    token: str
):
    if not token:
        return Response(status_code=400)

    succ, payload = Token.auth(token)

    if not succ:
        return Response(status_code=401)

    return {
        'payload': payload,
    }

