"""Module & package import."""
from functools import wraps
from flask_login import current_user
from online_store import login_manager

# Create decorator for routes that require admin role


def admin_required(func):
    """Decorate route function to check is user isadmin."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            return login_manager.unauthorized()

    return wrapper
