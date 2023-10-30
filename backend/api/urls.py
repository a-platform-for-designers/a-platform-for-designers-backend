from .views import CaseImageViewSet, CommentViewSet, SphereViewSet
from api.views.user_views import ProfileCustomerViewSet, ProfileDesignerViewSet
from api.views.user_views import UserProfileViewSet
from api.views import CaseViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserProfileViewSet, basename='user')
router.register('caseimages', CaseImageViewSet)
router.register('comments', CommentViewSet)
router.register('spheres', SphereViewSet)
router.register(
    'profile_customer',
    ProfileCustomerViewSet,
    basename='profile_customer'
)
router.register(
    'profile_designer',
    ProfileDesignerViewSet,
    basename='profile_designer'
)
router.register('cases', CaseViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
