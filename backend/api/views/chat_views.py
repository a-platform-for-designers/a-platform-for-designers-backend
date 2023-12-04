# from django.db.models import Q
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import viewsets

# from api.permissions import IsInitiatorOrReceiverChatPermission
# from api.serializers.chat_serializers import ChatCreateSerializer
# from api.serializers.chat_serializers import ChatReadSerializer
# from job.models import Chat


# class ChatViewSet(viewsets.ModelViewSet):
#     """"
#     Класс ChatViewSet для работы с чатами.

#     """

#     http_method_names = ['get', 'post']
#     permission_classes = [
#         IsAuthenticated,
#         IsInitiatorOrReceiverChatPermission
#     ]

#     def get_queryset(self):
#         user = self.request.user
#         return Chat.objects.filter(Q(initiator=user) | Q(receiver=user))

#     def get_serializer_class(self):
#         if self.request.method in ('POST'):
#             return ChatCreateSerializer
#         return ChatReadSerializer

#     def perform_create(self, serializer):
#         serializer.save(initiator=self.request.user)


from job.models import Chat
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import User
from api.serializers.chat_serializers import (
    ChatCreateSerializer, ChatReadSerializer,
)
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_convo(request, ):
    data = request.data
    username = data.pop('username')
    try:
        participant = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user'})

    chat = Chat.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))
    if chat.exists():
        return redirect(reverse('get_conversation', args=(chat[0].id,)))
    else:
        chat = Chat.objects.create(initiator=request.user, receiver=participant)
        return Response(ChatCreateSerializer(instance=chat).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation(request, convo_id):
    conversation = Chat.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Conversation does not exist'})
    else:
        serializer = ChatCreateSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversations(request):
    conversation_list = Chat.objects.filter(Q(initiator=request.user) |
                                                    Q(receiver=request.user))
    serializer = ChatReadSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)
