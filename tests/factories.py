import factory

from core.models import User
from goals.models import Goal, GoalCategory, Board, BoardParticipant, Comment


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    first_name = "test name"
    last_name = "test last name"
    email = "test@mail.ru"
    password = "test26758"


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker("name")
    is_deleted = False


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = 1


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = "tests category"
    is_deleted = False
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = "goal"
    description = "description"
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)
    status = 1
    priority = 2
    due_date = None


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = "tests comment"
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)
