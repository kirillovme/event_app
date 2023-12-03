from functools import wraps

from asgiref.sync import sync_to_async
from django.shortcuts import redirect


def async_login_required(view_func):
    """Декоратор для проверки аутентификации пользователя."""
    @wraps(view_func)
    async def _wrapped_view(request, *args, **kwargs):
        if not await sync_to_async(lambda: request.user.is_authenticated)():
            return redirect('login')
        return await view_func(request, *args, **kwargs)
    return _wrapped_view
