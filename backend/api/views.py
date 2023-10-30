from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from job.models import Case, Favorite, Instrument, Skill
from pagination import LimitPageNumberPagination
from serializers import (CaseSerializer,
                         CaseCreateSerializer,
                         CaseShortSerializer,
                         InstrumentSerializer,
                         SkillSerializer)
from .permissions import (IsInitiatorOrReceiverChatPermission,
                          IsInitiatorOrReceiverMessagePermission)
from .serializers import (ChatCreateSerializer, ChatReadSerializer,
                          MessageSerializer, )
from job.models import Chat


class InstrumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]
    search_fields = ['^name', ]


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]


class CaseViewSet(ModelViewSet):
    """"
    Класс CaseViewSet для работы с проектами авторов.

    """
    queryset = Case.objects.all()
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CaseSerializer
        return CaseCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
    )
    def favorite(self, request, pk):
        case_obj = get_object_or_404(Case, pk=pk)
        if request.method == 'POST':
            already_existed, created = Favorite.objects.get_or_create(
                user=request.user,
                case=case_obj
            )
            if not created:
                return Response(
                    {'errors': 'Ошибка при создании записи.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = CaseShortSerializer(case_obj,
                                             context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = request.user.favorites.all()
            if favorite:
                favorite.delete()
                return Response(
                    {'message': 'Проект удален из избранного.'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            return Response(
                {'errors': 'Проект не найден в избранном.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChatViewSet(viewsets.ModelViewSet):
    """"Класс ChatViewSet для работы с чатами."""

    http_method_names = ['get', 'post']
    permission_classes = [
        permissions.IsAuthenticated,
        IsInitiatorOrReceiverChatPermission
    ]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(Q(initiator=user) | Q(receiver=user))

    def get_serializer_class(self):
        if self.request.method in ('POST'):
            return ChatCreateSerializer
        return ChatReadSerializer

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """"Класс MessageViewSet для работы с сообщениями чатов."""

    serializer_class = MessageSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [
        permissions.IsAuthenticated,
        IsInitiatorOrReceiverMessagePermission
    ]

    def get_chat(self):
        user = self.request.user
        return get_object_or_404(
            Chat.objects.filter(Q(initiator=user) | Q(receiver=user)),
            pk=self.kwargs.get('chat_id'),
        )

    def get_queryset(self):
        return self.get_chat().messages.all()

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
            chat=self.get_chat()
        )

