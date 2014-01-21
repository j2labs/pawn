### Attempt to setup gevent
from gevent import monkey
monkey.patch_all()

from gevent import pool

coro_pool = pool.Pool


def init_pool(pool=None):
    """Handles the generation of a pool and allows for two methods of
    overriding the default behavior: using a custom pool callable or using an
    existing pool.
    """
    if pool is None:
        instance = coro_pool()
    elif callable(pool):
        instance = pool()
    elif pool:
        instance = pool
    else:
        raise ValueError('Unable to initialize coroutine pool')
    return instance
