import requests
from .social_auth import SocialAuth, SocialAuthResponse

class GoogleSocialAuth(SocialAuth):
    type = 'google'

    def valid(self, token: str) -> tuple[bool, str | SocialAuthResponse]:
        profile = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?alt=json?access_token={token}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        if profile.status_code != 200:
            return False, "Invalid token"

        profile = profile.json()

        if not 'sub' in profile:
            return False, "Required permission(s) not granted"
        
        return True, SocialAuthResponse(
            id=profile['sub'],
            nickname=None,
            email=profile.get('email', None) if profile.get('email_verified', False) else None,
        )