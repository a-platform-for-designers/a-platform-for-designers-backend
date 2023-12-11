from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from api.filters import CaseFilter
from api.pagination import LimitPageNumberPagination
from api.serializers.caseimage_serializers import CaseImageSerializer
from api.serializers.case_serializers import (CaseSerializer,
                                              CaseCreateSerializer,
                                              CaseShortSerializer,
                                              )
from job.models import Case, FavoriteCase, CaseImage
from api.permissions import IsAuthorOrReadOnly


class CaseViewSet(ModelViewSet):
    """"
    Класс CaseViewSet для работы с проектами авторов.

    """
    queryset = Case.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CaseFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CaseSerializer
        return CaseCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.user.is_customer:
            return Response(
                {"detail": "Заказчик не может создавать кейс"},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            return super().create(request, *args, **kwargs)

    # @action(
    #     detail=True,
    #     methods=['POST', 'DELETE'],
    # )
    # def favorite(self, request, pk):
    #     case_obj = get_object_or_404(Case, pk=pk)
    #     if request.method == 'POST':
    #         already_existed, created = FavoriteCase.objects.get_or_create(
    #             user=request.user,
    #             case=case_obj
    #         )
    #         if not created:
    #             return Response(
    #                 {'errors': 'Ошибка при создании записи'},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )
    #         serializer = CaseShortSerializer(case_obj,
    #                                          context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     if request.method == 'DELETE':
    #         favorite = FavoriteCase.objects.filter(user=request.user,
    #                                                case=case_obj)
    #         if favorite.delete()[0]:
    #             return Response(
    #                 {'message': 'Проект удален из избранного.'},
    #                 status=status.HTTP_204_NO_CONTENT,
    #             )
    #         return Response(
    #             {'errors': 'Проект не найден в избранном.'},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
