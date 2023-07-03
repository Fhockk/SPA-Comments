from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None).prefetch_related('replies')
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'author__username', 'author__email']
    ordering = ['-created_at']

    @method_decorator(cache_page(30))  # кеширование на 1 час 60 * 60 * 1
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(30))  # кеширование на 1 час
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
