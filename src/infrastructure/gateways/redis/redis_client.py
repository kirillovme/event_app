import functools
from typing import Any, Callable

from django.conf import settings
from django.core.cache import cache


class RedisClient:
    """Класс для взаимодействия с Redis."""

    def delete_keys_by_pattern(self, pattern: str = '*'):
        """Удаление ключей по паттерну"""
        keys_list = cache.keys(pattern)
        for key in keys_list:
            cache.delete(key)

    def cache_result(self, key_format: str, timeout: int = settings.CACHE_TIMEOUT) -> Callable:
        """Декоратор для кеширования результатов функции"""

        def decorator(func: Callable) -> Callable:

            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                request = args[0]
                user_identifier = request.user.username
                all_args = {**kwargs, 'user_identifier': user_identifier}
                for i, arg in enumerate(args):
                    all_args[func.__code__.co_varnames[i]] = arg
                cache_key = key_format.format(**all_args)
                cached_value = cache.get(cache_key)
                if cached_value is not None:
                    return cached_value
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout=timeout)
                return result

            return wrapper

        return decorator

    def invalidate_cache(self, key_format_list: list[str]) -> Callable:
        """Декоратор для инвалидации кеша."""

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                request = args[0]
                user_identifier = request.user.username
                all_args = {**kwargs, 'user_identifier': user_identifier}
                for i, arg in enumerate(args):
                    all_args[func.__code__.co_varnames[i]] = arg
                for key_format in key_format_list:
                    cache_key = key_format.format(**all_args)
                    cache.delete(cache_key)
                result = func(*args, **kwargs)
                return result

            return wrapper

        return decorator


redis_client = RedisClient()
