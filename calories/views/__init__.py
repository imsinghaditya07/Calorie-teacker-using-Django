"""
calories/views/__init__.py
Re-exports all views so existing URL configurations work unchanged.
"""
from .auth import register_view, login_view, logout_view           # noqa: F401
from .dashboard import dashboard                                    # noqa: F401
from .food_log import add_food_log, edit_food_log, delete_food_log # noqa: F401
from .food_api import food_search_api, food_detail_api             # noqa: F401
from .food_custom import create_custom_food                        # noqa: F401
from .calculator import food_calculator, bulk_food_log             # noqa: F401
from .weight import weight_tracker, delete_weight_log              # noqa: F401
from .history import history                                       # noqa: F401
from .profile import profile                                       # noqa: F401
