from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, Comment

User = get_user_model()


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # скрытое поле

    class Meta:
        model = GoalCategory
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated', 'user']


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')

        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated', 'user']


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        read_only_fields = ['id', 'created', 'updated', 'user', 'goal']
        fields = '__all__'
