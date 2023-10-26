from api.views.user_views import UserProfileViewSet
from api.views import CaseViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserProfileViewSet, basename='user')
router.register('cases', CaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
