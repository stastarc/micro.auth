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

        if not 'Google_account' in profile:
            return False, "Required permission(s) not granted"
        
        data = profile['Google_account'].get('profile', None)

        if data is None:
            return False, "Cannot get social profile"
        
        return True, SocialAuthResponse(
            id=data['id'],
            nickname=data.get('nickname', None),
            email=profile['Google_account'].get('email', None)
        )