from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from comments.models import Comment
from comments.serializers import CommentSerializer
from comments.permissions import IsOwnerOrReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None).prefetch_related('replies')
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_at', 'updated_at', 'author__username', 'author__email']
    ordering = ['-created_at']

    # если пользователь не авторизован, он не создаст комментарий, также может изменять только свое
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    @method_decorator(cache_page(30))  # кеширование на 1 час 60 * 60 * 1
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(30))  # кеширование на 1 час
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
