from api.views.user_views import UserProfileViewSet
from .views1 import CaseViewSet, InstrumentViewSet, SkillViewSet
from django.urls import include, path
from rest_framework import routers
# from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('users', UserProfileViewSet, basename='user')
router.register('cases', CaseViewSet)
router.register('skills', SkillViewSet)
router.register('instruments', InstrumentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('api-token-auth/', views.obtain_auth_token),
]
