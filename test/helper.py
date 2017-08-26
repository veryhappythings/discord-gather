import asyncio
from unittest import mock


def async_test(f):
    # http://stackoverflow.com/a/23036785/304210
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


def get_mock_coro(return_value):
    # http://stackoverflow.com/questions/29881236/how-to-mock-asyncio-coroutines/29905620#29905620
    @asyncio.coroutine
    def mock_coro(*args, **kwargs):
        return return_value

    return mock.Mock(wraps=mock_coro)


def get_mock_coro_throwing_exception(exception_class, message):
    # http://stackoverflow.com/questions/29881236/how-to-mock-asyncio-coroutines/29905620#29905620
    @asyncio.coroutine
    def mock_coro(*args, **kwargs):
        raise exception_class(message)

    return mock.Mock(wraps=mock_coro)
