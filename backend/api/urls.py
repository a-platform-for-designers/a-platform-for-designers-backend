from api.views.user_views import UserProfileViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserProfileViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('languages')
    path('auth/', include('djoser.urls.authtoken')),
]
