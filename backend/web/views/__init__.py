from .static import home, tools_view, legal_view, about_view, custom_404, custom_500
from .auth import login_view, logout_view, register_view, profile_view, edit_profile, change_password, delete_account
from .dashboard import dashboard_view, analytics_view, leaderboard_view
from .planner import planner_view, custom_planner_view, delete_custom_event, complete_custom_event
from .content import exercise_library, exercise_detail, recipe_list, recipe_detail, blog_list, article_detail, delete_comment, like_article
from .workout import workout_setup_view, workout_session_view, complete_workout, start_workout, workout_session, add_set_to_session, complete_workout_session, workout_history, workout_detail
from .onboarding import onboarding_welcome, onboarding_step1, onboarding_step2, onboarding_step3
from .admin_panel import admin_panel, admin_toggle_hide, admin_delete_user
from .program import program_list, program_detail, start_program, complete_program_day
from .shop import shop_list, shop_detail, cart_view, add_to_cart, remove_from_cart, update_cart_quantity, fake_checkout, order_success
from .favorites import favorites_view, add_favorite, remove_favorite
