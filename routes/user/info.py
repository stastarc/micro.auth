from fastapi import APIRouter
from fastapi.responses import Response
from database import users
from auth import Token


router = APIRouter(prefix='/info')

@router.get('/{user_id}')
async def info(
        res: Response,
        user_id: int,
        key: str,
    ):
    if user_id < 0:
        res.status_code = 400
        return None

    with users.scope() as sess:
        succ, payload = Token.session_auth(sess, key, check_active=False)

        if not succ or isinstance(payload, str):
            res.status_code = 401
            return {"error": payload}

        me = user_id == 0 or payload.id == user_id

        if me:
            user_id = payload.id

        user = sess.query(users.User).filter(users.User.id == user_id).first()

        if not user or (not me and user.status != 'active'):
            res.status_code = 404
            return {"error": "User not found"}

        profile = {
            'id': user.id,
            'nickname': user.nickname,
            'picture': user.picture,
            'social_type': user.social_type,
        }

        if me:
            profile['email'] = user.email
            profile['status'] = user.status
            profile['created_at'] = user.created_at

        return {
            'profile': profile
        }
