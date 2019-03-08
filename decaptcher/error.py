__all__ = [
    'DecaptcherError',
    'RemoteServiceError',
    'ServiceNotAvailable',
    'ZeroBalance',
    'ResultNotReady',
    'InvalidServiceResponse',
]


class DecaptcherError(Exception):
    pass


class RemoteServiceError(DecaptcherError):
    pass


class ServiceNotAvailable(RemoteServiceError):
    pass


class InvalidServiceResponse(RemoteServiceError):
    pass


class ZeroBalance(RemoteServiceError):
    pass


class ResultNotReady(RemoteServiceError):
    pass
