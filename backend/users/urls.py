from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
