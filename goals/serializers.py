from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, Comment, Board, BoardParticipant

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

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"

class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id","user", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board

class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True,
        choices=BoardParticipant.Role.choices[1:]
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id]["role"]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            instance.title = validated_data["title"]
            instance.save()

        return instance
