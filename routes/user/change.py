from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from auth import Token
from database import users
from micro.cdn import CDN
from utils import nickname as nickname_util
import numpy as np
import cv2

router = APIRouter(prefix='/change')

@router.post('/nickname')
async def change_nickname(
    res: Response,
    key: str,
    nickname: str,
):
    if not nickname_util.valid(nickname):
        res.status_code = 400
        return {"error": "Invalid nickname"}

    succ, payload = Token.auth(key)

    if not succ or isinstance(payload, str):
        res.status_code = 401
        return {"error": payload}

    with users.scope() as sess:
        if users.User.exists_nickname(sess, nickname):
            res.status_code = 400
            return {"error": "Nickname already exists"}
        
        user = sess.query(users.User).filter(users.User.id == payload.id).first()
        
        if not user:
            res.status_code = 500
            return {"error": "wtf??"}
        
        user.nickname = nickname

        sess.commit()

    res.status_code = 200

    return {
        'profile': {
            'nickname': user.nickname
        }
    }


@router.post('/picture')
async def change_picture(
    res: Response,
    key: str,
    picture: UploadFile = File(...),
):

    succ, payload = Token.auth(key)

    if not succ or isinstance(payload, str):
        res.status_code = 401
        return {"error": payload}

    try:
        img = cv2.imdecode(np.fromstring(picture.file.read(), dtype=np.uint8), cv2.IMREAD_COLOR)  # type: ignore
        h, w, _ = img.shape
        if not (h == w and h == 128): raise Exception()
        succ, img = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not succ: raise Exception()
    except:
        res.status_code = 400
        return {"error": "The wrong picture or size is not 128x128."}

    try:
        picture_id = CDN.upload_file(img, f'user picture {payload.id}', 'client upload')
    except:
        res.status_code = 500
        return {"error": "cdn error"}

    with users.scope() as sess:
        user = sess.query(users.User).filter(users.User.id == payload.id).first()

        if not user: raise Exception('wtf??')

        user.picture = picture_id

        sess.commit()

    res.status_code = 200
    return {
        'profile': {
            'picture': picture_id
        }
    }