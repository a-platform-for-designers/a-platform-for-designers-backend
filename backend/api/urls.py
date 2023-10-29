from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('users', views.UserProfileViewSet, basename='users')
router.register('chats', views.ChatViewSet, basename='chats')
router.register(
    r'chats/(?P<chat_id>\d+)/messages',
    views.MessageViewSet,
    basename='messages'
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
