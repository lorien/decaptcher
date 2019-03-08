class BaseServiceBackend(object):

    # ***************
    # Submitting Task
    # ***************

    def build_task_request(self, data=None, options=None):
        raise NotImplementedError

    def parse_task_response(self, res):
        raise NotImplementedError

    # ***************
    # Checking Result
    # ***************

    def build_result_request(self, task_id):#, options=None):
        raise NotImplementedError

    def parse_result_response(self, res):
        raise NotImplementedError
