from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Password Reset Flow
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(
             template_name='web/password_reset_form.html',
             email_template_name='web/password_reset_email.html',
             form_class=CustomPasswordResetForm
         ), 
         name='password_reset'),
    path('reset_password/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='web/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='web/password_reset_confirm.html',
             form_class=CustomSetPasswordForm
         ), 
         name='password_reset_confirm'),
    path('reset_password/complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='web/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/like/', views.like_article, name='like_article'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # Espace Membre
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/password/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_account, name='delete_account'),

    # Dashboard Admin custom (super-utilisateur uniquement)
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/users/<int:user_id>/toggle-hide/', views.admin_toggle_hide, name='admin_toggle_hide'),
    path('admin-panel/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('planner/', views.planner_view, name='planner'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('agenda/', views.custom_planner_view, name='custom_planner'),
    path('agenda/delete/<int:event_id>/', views.delete_custom_event, name='delete_custom_event'),
    path('agenda/complete/<int:event_id>/', views.complete_custom_event, name='complete_custom_event'),
    path('exercises/', views.exercise_library, name='exercise_library'),
    path('exercises/<slug:slug>/', views.exercise_detail, name='exercise_detail'),
    path('nutrition/', views.recipe_list, name='recipe_list'),
    path('nutrition/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    
    # Programmes
    path('programs/', views.program_list, name='program_list'),
    path('programs/<slug:slug>/', views.program_detail, name='program_detail'),
    
    # Boutique
    path('shop/', views.shop_list, name='shop_list'),
    path('shop/<slug:slug>/', views.shop_detail, name='shop_detail'),
    
    # Panier & Favoris
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/checkout/', views.fake_checkout, name='fake_checkout'),
    path('cart/order-success/', views.order_success, name='order_success'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/add/<str:content_type>/<int:content_id>/', views.add_favorite, name='add_favorite'),
    path('favorites/remove/<int:favorite_id>/', views.remove_favorite, name='remove_favorite'),
    path('workout/', views.workout_session_view, name='workout_session'),
    path('workout/setup/', views.workout_setup_view, name='workout_setup'),
    path('workout/complete/', views.complete_workout, name='complete_workout'),
    
    # Workout Tracking
    path('workout/start/', views.start_workout, name='start_workout'),
    path('workout/session/<int:session_id>/', views.workout_session, name='workout_session_detail'),
    path('workout/session/<int:session_id>/add-set/', views.add_set_to_session, name='add_set_to_session'),
    path('workout/session/<int:session_id>/complete/', views.complete_workout_session, name='complete_workout_session'),
    path('workout/history/', views.workout_history, name='workout_history'),
    path('workout/detail/<int:session_id>/', views.workout_detail, name='workout_detail'),
    
    # Analytics
    path('analytics/', views.analytics_view, name='analytics'),
    
    # Onboarding
    path('onboarding/', views.onboarding_welcome, name='onboarding_welcome'),
    path('onboarding/step1/', views.onboarding_step1, name='onboarding_step1'),
    path('onboarding/step2/', views.onboarding_step2, name='onboarding_step2'),
    path('onboarding/step3/', views.onboarding_step3, name='onboarding_step3'),
    
    # Leaderboard
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    
    path('tools/', views.tools_view, name='tools'),
    
    # Pages Statiques
    path('legal/', views.legal_view, name='legal'),
    path('about/', views.about_view, name='about'),
]
