from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet, UserViewSet, create_user,
                    get_jwt_token)

router_v1 = DefaultRouter()
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    'comments'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    'reviews'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/signup/',
        create_user,
        name='token_obtain_pair'
    ),
    path('v1/auth/token/', get_jwt_token, name='token')
]
