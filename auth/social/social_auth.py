

from dataclasses import dataclass

@dataclass
class SocialAuthResponse:
    id: str
    nickname: str | None
    email: str | None

class SocialAuth:
    type: str
    
    def valid(self, token: str) -> tuple[bool, str | SocialAuthResponse]:
        raise NotImplementedError()