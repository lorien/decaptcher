from .common import CommonBackend


class TwocaptchaBackend(CommonBackend):
    software_id = 2373
    base_url = 'http://rucaptcha.com'
