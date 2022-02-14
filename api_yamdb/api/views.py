from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reviews.models import Review
from titles.models import Category, Genre, Title
from users.models import User

from .filters import TitlesFilter
from .mixins import ListCreateDeleteViewSet
from .paginators import CustomPagination
from .permissions import (IsAdmin, IsAdminOrReadOnly, IsAdminOrReadOnlyTitles,
                          OwnerOrHasRights)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          ConfirmationCodeSerializer, GenresSerializer,
                          ReviewSerializer, TitlesCreateSerializer,
                          TitlesReadOnlySerializer, UserEmailSerializer,
                          UserSerializer)


class CategoriesViewSet(ListCreateDeleteViewSet):
    """Вьюесет для категорий."""
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']


class GenresViewSet(ListCreateDeleteViewSet):
    """Вьюсет для жанров."""
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюесет для тайтлов."""
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (IsAdminOrReadOnlyTitles,)
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesReadOnlySerializer
        elif self.request.method in ('POST', 'PATCH', 'DELETE'):
            return TitlesCreateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    permission_classes = (OwnerOrHasRights,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, title=title, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = (OwnerOrHasRights,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        review = Review.objects.filter(
            title_id=self.kwargs.get('title_id')
        )
        return review

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])

        serializer.save(author=self.request.user, title=title)


@api_view(['POST'])
def create_user(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    if username is not None:
        user = User.objects.filter(
            Q(username=username) | Q(email=email))
        if user.count() == 0:
            User.objects.create_user(username=username, email=email)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [f'{user.email}', ]
    send_mail(subject, message, email_from, recipient_list)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = PageNumberPagination
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=username']
    queryset = User.objects.all()

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request, pk=None):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)
