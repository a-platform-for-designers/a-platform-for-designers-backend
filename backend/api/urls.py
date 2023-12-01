from django.urls import include, path
from rest_framework import routers

from api.views.case_views import CaseViewSet
from api.views.caseimage_views import CaseImageViewSet
from api.views.chat_views import ChatViewSet
from api.views.comment_views import CommentViewSet
from api.views.instrument_views import InstrumentViewSet
from api.views.language_views import LanguageViewSet
from api.views.order_views import OrderViewSet
from api.views.resume_views import ResumeViewSet
from api.views.skill_views import SkillViewSet
from api.views.specialization_views import SpecializationViewSet
from api.views.sphere_views import SphereViewSet
from api.views.message_views import MessageViewSet
from api.views.user_views import ProfileCustomerViewSet, ProfileDesignerViewSet
from api.views.user_views import UserProfileViewSet
from api.views.user_views import TokenCreateView


router = routers.DefaultRouter()

router.register('users', UserProfileViewSet, basename='users')
# router.register('comments', CommentViewSet, basename='comments')
router.register('spheres', SphereViewSet, basename='spheres')
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
router.register('cases', CaseViewSet, basename='cases')
# router.register('chats', ChatViewSet, basename='chats')
# router.register(
#     r'chats/(?P<chat_id>\d+)/messages',
#     MessageViewSet,
#     basename='messages'
# )
router.register(
    'specializations',
    SpecializationViewSet,
    basename='specializations'
)
router.register('orders', OrderViewSet, basename='orders')
router.register('resume', ResumeViewSet, basename='resume')
router.register('instruments', InstrumentViewSet, basename='instruments')
router.register('skills', SkillViewSet, basename='skills')
router.register('languages', LanguageViewSet, basename='languages')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
