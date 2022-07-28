from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel
from auth.token import TokenPayload

from database import users
from auth import social, Token


router = APIRouter(prefix='/social')

class LoginBody(BaseModel):
    token: str
    type: str

@router.post('/login')
async def login(body: LoginBody, res: Response):
    method = social.methods.get(body.type, None)

    if not method:
        res.status_code = 400
        return {"error": "Invalid social type"}
    
    succ, data = method.valid(body.token)

    if not succ or not data or isinstance(data, str):
        res.status_code = 400
        return {"error": f"Authentication failed: {data}"}

    with users.scope() as sess:
        user = sess.query(users.User).filter(users.User.social_id == data.id).first()

        if not user:
            user = users.User(
                nickname=users.User.create_nickname(sess),
                email=data.email,
                social_id=data.id,
                social_type=method.type
            )

            sess.add(user)

        user_id = user.id
        secret = str(user.secret)
        
    token = Token.encode(TokenPayload(id=user_id), secret)  # type: ignore
    
    return {
        'token': token,
    }