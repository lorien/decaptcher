from six.moves.urllib.request import urlopen, Request
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.parse import urlencode, urljoin
import socket
import time
import logging
from datetime import timedelta

from .error import (
    ServiceNotAvailable, ResultNotReady
)
from .backend.rucaptcha import RucaptchaBackend
from .backend.browser import BrowserBackend


BACKEND_ALIAS = {
    'rucaptcha': RucaptchaBackend,
    'browser': BrowserBackend,
}
logger = logging.getLogger('decaptcher.service')


class Service(object):
    network_errors = (URLError, socket.error)
    network_config = {
        'read_timeout': 5,
    }

    def __init__(self, backend, **kwargs):
        assert isinstance(self.network_errors, tuple)

        if isinstance(backend, str):
            backend_cls = BACKEND_ALIAS[backend]
        else:
            backend_csl = backend
        self.backend = backend_cls(**kwargs)

    def submit_task(self, data, options=None):
        req = self.backend.build_task_request(
            data, options=options
        )
        return self.backend.parse_task_response(
            self.process_network_request(
                req['url'], 
                req['data'],
                timeout=self.network_config['read_timeout'],
            )
        )

    def check_result(self, data):#, options=None):
        req = self.backend.build_result_request(
            data#, options=options,
        )
        return self.backend.parse_result_response(
            self.process_network_request(
                req['url'], 
                req['data'],
                timeout=self.network_config['read_timeout'],
            )
        )

    def process(
                self,
                data=None,
                submit_timeout=30,
                submit_retry_delay=5,
                check_initial_delay=10,
                check_timeout=120,
                check_retry_delay=5,
                network_retry_delay=1,
                verbose=False,
                task_options=None,
                #result_options=None,
        ):
        if isinstance(data, file):
            data = data.read()
        start = time.time()
        retry_count = 0
        while True:
            retry_count += 1
            try:
                if retry_count > 1:
                    retry_str = ', retry #%d' % retry_count
                else:
                    retry_str = ''
                logger.debug('Submitting task%s', retry_str)
                task = self.submit_task(data, task_options)
            except ServiceNotAvailable:
                if time.time() > start + submit_timeout:
                    raise
                else:
                    time.sleep(submit_retry_delay)
            except self.network_errors:
                if time.time() > start + submit_timeout: 
                    raise
                else:
                    time.sleep(network_retry_delay)
            else:
                break

        time.sleep(check_initial_delay)

        start = time.time()
        retry_count = 0
        while True:
            retry_count += 1
            try:
                if retry_count > 1:
                    retry_str = ', retry #%d' % retry_count
                else:
                    retry_str = ''
                logger.debug('Checking task%s', retry_str)
                result = self.check_result(
                    task['task_id']#, result_options,
                )
            except (ServiceNotAvailable, ResultNotReady):
                if time.time() > start + check_timeout:
                    raise
                else:
                    time.sleep(check_retry_delay)
            except (URLError, socket.error):
                if time.time() > start + check_timeout:
                    raise
                else:
                    time.sleep(network_retry_delay)
            else:
                break

        if verbose:
            result['task_id'] = task['task_id']
            return result
        else:
            return result['result']

    def process_file(self, path, **kwargs):
        with open(path) as inp:
            return self.process(inp.read(), **kwargs)

    def process_network_request(self, url, data, timeout):
        if data:
            for key in data.keys():
                if isinstance(data[key], unicode):
                    data[key] = data[key].encode('utf-8')

            req_data = urlencode(data).encode('utf-8')
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
