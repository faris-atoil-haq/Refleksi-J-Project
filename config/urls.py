from django.contrib import admin
from django.urls import include, path
from core import public

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', public.main, name='public'),
    path('app/', include('core.urls')),
]

# Error handlers
handler400 = 'core.error_handler.handle_400'
handler404 = 'core.error_handler.handle_404'
handler500 = 'core.error_handler.handle_500'
