from dataclasses import asdict, dataclass
from distutils import bcppcompiler
import random
import jwt

from database import users


@dataclass
class TokenPayload:
    id: int

class Token:
    @staticmethod
    def encode(payload: TokenPayload, secret: str) -> str:
        data = asdict(payload)
        data['exp'] = f'empty! wow {random.randint(10000, 99999)}'
        return jwt.encode(data, secret, algorithm='HS256')

    @staticmethod
    def decode(token: str, key: str, verify_sign: bool = True) -> TokenPayload:
        payload = jwt.decode(
            token,
            key,
            algorithms=['HS256'],
            options={
                'verify_exp': False,
                'verify_signature': verify_sign
            }
        )

        del payload['exp']

        return TokenPayload(**payload)

    @staticmethod
    def auth(token: str, check_active: bool = True) -> tuple[bool, str | TokenPayload]:
        try: payload = Token.decode(token, '', verify_sign=False)
        except: return False, "Invalid token"

        with users.scope() as sess:
            status = sess.query(users.User.status).filter(users.User.id == payload.id).scalar()

            if not status or (check_active and status != 'active'):
                return False, "The user cannot be found or disabled."
            
        return True, payload