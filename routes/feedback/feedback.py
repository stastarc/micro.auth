from fastapi import APIRouter, Response, Form
from auth import Token
from database.db import scope
from database import Feedback

router = APIRouter()

@router.post("/")
async def feedback(
    res: Response,
    token: str,
    feedback: str = Form(max_length=1000, min_length=2),
    info: str = Form(max_length=6000),
):
    with scope() as sess:
        succ, payload = Token.session_auth(sess, token)

        if not succ or isinstance(payload, str):
            res.status_code = 401
            return {"error": payload}

        Feedback.session_write(sess, payload.id, feedback, info)

        return {"success": True}
