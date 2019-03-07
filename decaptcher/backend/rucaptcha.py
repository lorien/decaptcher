from base64 import b64encode
from six.moves.urllib.parse import urlencode, urljoin

from ..base_backend import BaseServiceBackend
from ..error import (
    ServiceNotAvailable, ResultNotReady, ZeroBalance,
    RemoteServiceError,
)


class RucaptchaBackend(BaseServiceBackend):
    software_id = 2373

    def __init__(self, api_key, service_url='http://rucaptcha.com'):
        self.api_key = api_key
        self.service_url = service_url

    # ***************
    # Submitting Task
    # ***************

    def build_task_request(self, data, **kwargs):
        post = {
            'key': self.api_key,
            'method': 'base64',
            'body': b64encode(data).decode('ascii'),
            'soft_id': self.software_id,
        }
        post.update(kwargs)
        return {
            'url': urljoin(self.service_url, 'in.php'),
            'data': post,
        }

    def parse_task_response(self, res):
        if res['code'] == 200:
            if res['body'].startswith(b'OK|'):
                return {
                    'task_id': res['body'].split(b'|', 1)[1].decode('ascii')
                }
            elif res['body'] == b'ERROR_NO_SLOT_AVAILABLE':
                raise ServiceNotAvailable('Service too busy')
            elif res['body'] == b'ERROR_ZERO_BALANCE':
                raise ZeroBalance('Balance too low')
            else:
                raise RemoteServiceError(res['body'])
        else:
            raise RemoteServiceError('Returned HTTP code: %d' % res['code'])

    # ***************
    # Checking Result
    # ***************

    def build_result_request(self, task_id):
        params = {
            'key': self.api_key,
            'action': 'get',
            'id': task_id,
        }
        return {
            'url': urljoin(
                self.service_url,
                'res.php?%s' % urlencode(params)
            ),
            'data': None,
        }

    def parse_result_response(self, res):
        if res['code'] == 200:
            if res['body'].startswith(b'OK|'):
                return res['body'].split(b'|', 1)[1].decode('utf8')
            elif res['body'] == b'CAPCHA_NOT_READY':
                raise ResultNotReady('Solution is not ready')
            else:
                raise RemoteServiceError(res['body'])
        else:
            raise RemoteServiceError('Returned HTTP code: %d' % res['code'])
