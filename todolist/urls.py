from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(('core.urls', 'core'))),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("goals/", include(("goals.urls", "goals"))),
    path('bot/', include(('bot.urls', 'bot'))),
]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls'))
    ]