from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, Comment, Board
from goals.permissions import BoardPermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalSerializer, CommentSerializer, \
    CommentCreateSerializer, GoalCreateSerializer, BoardSerializer, BoardCreateSerializer, BoardListSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ['board']

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GoalDateFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority']
    ordering = ['priority', 'due_date']

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class CommentCreateView(CreateAPIView):
    model = Comment
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]


class CommentListView(ListAPIView):
    model = Comment
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class CommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    ordering = ['title']
    search_fields = ('title',)

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user,
            is_deleted=False
        )