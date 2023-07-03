from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsUserOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrReadOnly] # пользователь может просматривать других, но не изменять

    @method_decorator(cache_page(60 * 60 * 1))  # кеширование на 1 час
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 1))  # кеширование на 1 час
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
