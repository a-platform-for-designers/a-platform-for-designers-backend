from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from job.models import Case, Favorite, Instrument, Skill
from pagination import LimitPageNumberPagination
from serializers import (CaseSerializer,
                         CaseCreateSerializer,
                         CaseShortSerializer,
                         InstrumentSerializer,
                         SkillSerializer)


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
