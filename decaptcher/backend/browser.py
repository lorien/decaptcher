import tempfile
import webbrowser
import time
import os
import sys
import locale

from six.moves import input

from ..base_backend import BaseServiceBackend


class BrowserBackend(BaseServiceBackend):

    # ***************
    # Submitting Task
    # ***************

    def build_task_request(self, data=None, options=None):
        fd, path = tempfile.mkstemp()
        with open(path, 'wb') as out:
            out.write(data)
        os.close(fd)
        url = 'file://' + path
        return {
            'url': url,
            'data': None,
        }

    def parse_task_response(self, res):
        return {
            'task_id': res['url'].replace('file://', ''),
        }

    # ***************
    # Checking Result
    # ***************

    def build_result_request(self, task_id):#, options=None):
        url = 'file://' + task_id
        return {
            'url': url,
            'data': None,
        }

    def parse_result_response(self, res):
        webbrowser.open(url=res['url'])
        # Wait some time, skip some debug messages
        # which browser could dump to console
        time.sleep(0.5)
        solution = input('Enter solution: ')
        if hasattr(solution, 'decode'):
            solution = solution.decode(sys.stdin.encoding or
                                       locale.getpreferredencoding(True))
        path = res['url'].replace('file://', '')
        os.unlink(path)
        return {
            'result': solution,
        }
