from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, create_user, get_jwt_token

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls))
]

urlpatterns += [
    path(
        'auth/signup/',
        create_user,
        name='token_obtain_pair'
    ),
    path('auth/token/', get_jwt_token, name='token')
]
