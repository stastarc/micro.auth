from dataclasses import asdict, dataclass
import random
import jwt

from database import scope, User


@dataclass
class TokenPayload:
    id: int

class Token:
    @staticmethod
    def encode(payload: TokenPayload, secret: str) -> str:
        data = asdict(payload)
        data['$'] = f'{random.randint(0, 9999999)}'
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

        del payload['$']

        return TokenPayload(**payload)

    @staticmethod
    def auth(token: str, check_active: bool = True) -> tuple[bool, str | TokenPayload]:
        with scope() as sess:
            return Token.session_auth(sess, token, check_active)
    
    @staticmethod
    def session_auth(sess, token: str, check_active: bool = True) -> tuple[bool, str | TokenPayload]:
        def verify(secret: str):
            try: return Token.decode(token, secret, verify_sign=bool(secret))
            except: return False
        
        payload = verify('')

        if not payload:
            return False, "Invalid token"

        user = sess.query(User).filter(User.id == payload.id).scalar()
        payload = verify(str(user.secret))

        if not payload:
            return False, "Invalid token"
        elif check_active and user.status != 'active':
            return False, "The user cannot be found or disabled."
            
        return True, payload