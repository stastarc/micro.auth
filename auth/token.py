from dataclasses import asdict, dataclass
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
        with users.scope() as sess:
            return Token.session_auth(sess, token, check_active)
    
    @staticmethod
    def session_auth(sess, token: str, check_active: bool = True) -> tuple[bool, str | TokenPayload]:
        def verify(secret: str, verify_sign: bool):
            try: return Token.decode(token, secret if verify_sign else '', verify_sign=verify_sign)
            except: return False
        
        payload = verify('', False)

        if not payload:
            return False, "Invalid token"

        user = sess.query(users.User).filter(users.User.id == payload.id).scalar()
        payload = verify(user.secret, True)
        status = user.status

        if not payload:
            return False, "Invalid token"
        elif not status or (check_active and status != 'active'):
            return False, "The user cannot be found or disabled."
            
        return True, payload