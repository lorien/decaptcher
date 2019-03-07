from six.moves.urllib.request import urlopen, Request
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.parse import urlencode, urljoin
import socket
import time
import logging

from .error import (
    ServiceNotAvailable, ResultNotReady
)
from .backend.rucaptcha import RucaptchaBackend


BACKEND_ALIAS = {
    'rucaptcha': RucaptchaBackend,
}


class Service(object):
    network_config = {
        'read_timeout': 5,
    }

    def __init__(self, backend, **kwargs):
        if isinstance(backend, str):
            backend_cls = BACKEND_ALIAS[backend]
        else:
            backend_csl = backend
        self.backend = backend_cls(**kwargs)

    def submit_task(self, data):
        req = self.backend.build_task_request(data)
        return self.backend.parse_task_response(
            self.process_network_request(
                req['url'], 
                req['data'],
                timeout=self.network_config['read_timeout'],
            )
        )

    def check_result(self, data):
        req = self.backend.build_result_request(data)
        return self.backend.parse_result_response(
            self.process_network_request(
                req['url'], 
                req['data'],
                timeout=self.network_config['read_timeout'],
            )
        )

    def process_data(
                self,
                data,
                submit_timeout=30,
                submit_retry_delay=5,
                check_initial_delay=10,
                check_timeout=120,
                check_retry_delay=5,
                network_retry_delay=1,
        ):
        start = time.time()
        while True:
            try:
                task = self.submit_task(data)
            except ServiceNotAvailable:
                if time.time() > start + timedelta(seconds=submit_timeout):
                    raise
                else:
                    time.sleep(submit_retry_delay)
            except (URLError, socket.error):
                if time.time() > start + timedelta(seconds=submit_timeout):
                    raise
                else:
                    time.sleep(network_retry_delay)
            else:
                break

        print('task_id', task['task_id'])
        time.sleep(check_initial_delay)

        start = time.time()
        while True:
            try:
                result = self.check_result(task['task_id'])
            except (ServiceNotAvailable, ResultNotReady):
                if time.time() > start + timedelta(seconds=check_timeout):
                    raise
                else:
                    time.sleep(check_retry_delay)
            except (URLError, socket.error):
                if time.time() > start + timedelta(seconds=submit_timeout):
                    raise
                else:
                    time.sleep(network_retry_delay)
            else:
                break

        return result

    def process_file(self, path, **kwargs):
        with open(path) as inp:
            return self.process_data(inp.read(), **kwargs)

    def process_network_request(self, url, data, timeout):
        if data:
            req_data = urlencode(data).encode('ascii')
        else:
            req_data = None
        req = Request(url, req_data)
        try:
            response = urlopen(req, timeout=timeout)
            body = response.read()
            code = response.getcode()
        except HTTPError as ex:
            code = ex.code
            body = ex.fp.read()
        return {
            'code': code,
            'body': body,
            'url': url,
        }
