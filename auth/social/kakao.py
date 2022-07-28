import requests
from .social_auth import SocialAuth, SocialAuthResponse

class KakaoSocialAuth(SocialAuth):
    type = 'kakao'

    def valid(self, token: str) -> tuple[bool, str | SocialAuthResponse]:
        profile = requests.post("https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "secure_resource" : True,
                "property_keys" : [
                    "kakao_account.profile",
                    "kakao_account.name",
                    "kakao_account.email"
                ]
            }
        )

        if profile.status_code != 200:
            return False, "Invalid token"

        profile = profile.json()

        if not 'kakao_account' in profile:
            return False, "Required permission(s) not granted"
        
        data = profile['kakao_account'].get('profile', None)

        if data is None:
            return False, "Cannot get social profile"
        
        return True, SocialAuthResponse(
            id=profile['id'],
            nickname=data.get('nickname', None),
            email=profile['kakao_account'].get('email', None)
        )