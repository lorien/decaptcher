from base64 import b64encode
from six.moves.urllib.parse import urlencode, urljoin
import json

from ..base_backend import BaseServiceBackend
from ..error import (
    ServiceNotAvailable, ResultNotReady, ZeroBalance,
    RemoteServiceError, InvalidServiceResponse
)


class CommonBackend(BaseServiceBackend):
    software_id = None
    base_url = 'http://rucaptcha.com'

    def __init__(self, api_key):
        self.api_key = api_key

    # ***************
    # Submitting Task
    # ***************

    def build_task_request(self, data=None, options=None):
        post = {
            'key': self.api_key,
        }
        if data:
            post.update({
                'method': 'base64',
                'body': b64encode(data).decode('ascii'),
            })
        if self.software_id:
            post['soft_id'] = self.software_id
        if options:
            post.update(options)
        return {
            'url': urljoin(self.base_url, '/in.php'),
            'data': post,
        }

    def parse_task_response(self, res):
        if res['code'] == 200:
            body = res['body'].decode('utf-8')
            if body.startswith('OK|'):
                return {
                    'task_id': body.split('|', 1)[1]
                }
            elif body == 'ERROR_NO_SLOT_AVAILABLE':
                raise ServiceNotAvailable('Service too busy')
            elif body == 'ERROR_ZERO_BALANCE':
                raise ZeroBalance('Balance too low')
            else:
                raise RemoteServiceError(body)
        else:
            raise RemoteServiceError('Unexpected HTTP code: %d' % res['code'])

    # ***************
    # Checking Result
    # ***************

    def build_result_request(self, task_id):#, options=None):
        params = {
            'key': self.api_key,
            'action': 'get',
            'id': task_id,
        }
        #if options:
        #    params.update(**options)
        return {
            'url': urljoin(
                self.base_url,
                '/res.php?%s' % urlencode(params)
            ),
            'data': None,
        }

    def parse_result_response(self, res):
        if res['code'] == 200:
            body = res['body'].decode('utf-8')
            if body.startswith('OK|'):
                return {
                    'result': body.split('|', 1)[1]
                }
            elif body == 'CAPCHA_NOT_READY':
                raise ResultNotReady('Result is not ready')
            else:
                raise RemoteServiceError(body)
        else:
            raise RemoteServiceError('Unexpected HTTP code: %d' % res['code'])
