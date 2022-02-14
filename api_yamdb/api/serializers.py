from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        model = Category
        exclude = ('id',)


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        model = Genre
        exclude = ('id',)


class TitlesReadOnlySerializer(serializers.ModelSerializer):
    """Сериализатор тайтлов для GET запросов."""
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlesCreateSerializer(serializers.ModelSerializer):
    """Сериализатор тайтлов для POST, PATCH и DELETE запросов."""
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
        required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        required=False, many=True
    )

    def validate_year(self, value):
        if value > timezone.now().year:
            raise ValidationError('Год выхода не может быть больше текущего.')
        return value

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, attrs):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        review_exists = Review.objects.filter(
            author=request.user,
            title__id=title_id
        ).exists()
        if not review_exists or request.method in ('PATCH', 'DELETE'):
            return attrs
        raise serializers.ValidationError('data failed')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Не допустимое имя пользователя')
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
