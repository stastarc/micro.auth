from fastapi import APIRouter
from fastapi.responses import Response
from database import users

router = APIRouter(prefix='/info')

@router.get('/{user_id}')
async def info(
        user_id: int,
    ):
    if user_id < 0:
        return Response(status_code=400)

    with users.scope() as sess:
        user: users.User = sess.query(users.User).filter(users.User.id == user_id).first()  # type: ignore

        if user is None:
            return Response(status_code=404)

        return {
            'profile': {
                'id': user.id,
                'nickname': user.nickname,
                'picture': user.picture,
            }
        }

@router.get('/{user_id}/detail')
async def info_detail(
        user_id: int,
    ):
    if user_id < 0:
        return Response(status_code=400)

    with users.scope() as sess:
        user: users.User = sess.query(users.User).filter(users.User.id == user_id).first()  # type: ignore
        
        if user is None:
            return Response(status_code=404)

        return {
            'profile': {
                'id': user.id,
                'nickname': user.nickname,
                'email': user.email,
                'status': user.status,
                'picture': user.picture,
                'social_id': user.social_id,
                'social_type': user.social_type,
                'created_at': user.created_at,
            }
        }
