from .social_auth import SocialAuth
from .kakao import KakaoSocialAuth
from .google import GoogleSocialAuth

methods: dict[str, SocialAuth] = {
    'kakao': KakaoSocialAuth(),
    'google': GoogleSocialAuth()
}