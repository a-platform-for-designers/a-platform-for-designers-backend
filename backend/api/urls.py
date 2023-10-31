from django.urls import include, path
from rest_framework import routers

from api.views.case_views import CaseViewSet
from api.views.caseimage_views import CaseImageViewSet
from api.views.chat_views import ChatViewSet
from api.views.comment_views import CommentViewSet
from api.views.order_views import OrderViewSet
from api.views.resume_views import ResumeViewSet
from api.views.specialization_views import SpecializationViewSet
from api.views.sphere_views import SphereViewSet
from api.views.message_views import MessageViewSet
from api.views.user_views import ProfileCustomerViewSet, ProfileDesignerViewSet, UserProfileViewSet


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
router.register('chats', ChatViewSet, basename='chats')
router.register(
    r'chats/(?P<chat_id>\d+)/messages',
    MessageViewSet,
    basename='messages'
)
router.register('specializations', SpecializationViewSet)
router.register('orders', OrderViewSet)
router.register('resume', ResumeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
