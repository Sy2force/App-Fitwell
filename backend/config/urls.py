from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Custom 404 error handler
handler404 = 'web.views.custom_404'
handler500 = 'web.views.custom_500'

# -----------------------------------------------------------------------------
# API DOCUMENTATION (Swagger)
# -----------------------------------------------------------------------------
schema_view = get_schema_view(
   openapi.Info(
      title="FitWell API",
      default_version='v1',
      description="FitWell API technical documentation",
      contact=openapi.Contact(email="contact@fitwell.local"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# -----------------------------------------------------------------------------
# MAIN ROUTES
# -----------------------------------------------------------------------------
urlpatterns = [
    # Interactive documentation (very useful for testing) - Outside i18n for now or included, your choice.
    # We keep it accessible without prefix or put it inside.
    # Generally API docs are in English, but we can keep them global.
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Route to change language (set_language)
    path('i18n/', include('django.conf.urls.i18n')),

    # API (Outside i18n_patterns to avoid /fr/api/ or /en/api/ prefixes)
    path('api/', include('api.urls')),
]

urlpatterns += i18n_patterns(
    # Django administration panel
    path('admin/', admin.site.urls),

    # Django Frontend
    path('', include('web.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# We serve media files (images) automatically in development mode
