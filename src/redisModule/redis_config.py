from src.dotenvModule.load import get_var


class RedisCache(object):
    config = {
        'CACHE_TYPE': get_var('CACHE_TYPE'),
        'CACHE_REDIS_HOST': get_var('CACHE_REDIS_HOST'),
        'CACHE_REDIS_PORT': get_var('CACHE_REDIS_PORT'),
        'CACHE_REDIS_DB': get_var('CACHE_REDIS_DB'),
        'CACHE_REDIS_URL': get_var('CACHE_REDIS_URL'),
        'CACHE_DEFAULT_TIMEOUT': get_var('CACHE_DEFAULT_TIMEOUT')}
