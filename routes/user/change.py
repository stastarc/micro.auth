from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response
from auth import Token
from database import User, scope
from micro.cdn import CDN
from utils import nickname as nickname_util

router = APIRouter(prefix='/change')

@router.post('/')
async def change(
    res: Response,
    token: str,
    nickname: str | None = Form(default=None),
    image: UploadFile | None = File(default=None)
):
    if not nickname and not image:
        res.status_code = 400
        return {"error": "No data"}

    with scope() as sess:
        succ, payload = Token.session_auth(sess, token)

        if not succ or isinstance(payload, str):
            res.status_code = 401
            return {"error": payload}

        
        user = User.session_get(sess, payload.id)

        if not user:
            res.status_code = 404
            return {"error": "User not found"}

        if nickname:            
            if not nickname_util.valid(nickname):
                res.status_code = 400
                return {"error": "Invalid nickname"}
                
            if User.exists_nickname(sess, nickname):
                res.status_code = 400
                return {"error": "Nickname already exists"}

            user.nickname = nickname  # type: ignore
            
        img = None

        if image:
            try:
                img = CDN.upload_image(await image.read(), f'picture {user.id}')
                user.picture = img  # type: ignore
            except:
                res.status_code = 500
                return {"error": "cdn micro service error"}

        sess.commit()

    res.status_code = 200

    return {
        'profile': {
            'nickname': nickname,
            'picture': img
        }
    }
