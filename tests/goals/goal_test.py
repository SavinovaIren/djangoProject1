import pytest
from django.utils import timezone

from goals.serializers import GoalSerializer
from tests.factories import GoalFactory

from goals.models import Goal


@pytest.mark.django_db
def test_goal_create(client, get_credentials, board_participant, goal_category):
    """create goal tests"""
    data = {
        "title": "testgoal",
        "user": board_participant.user.pk,
        "category": goal_category.id,

    }

    response = client.post(
        path="/goals/goal/create",
        HTTP_AUTHORIZATION=get_credentials,
        data=data,
        content_type="application/json"
    )
    goal = Goal.objects.last()
    assert response.status_code == 201
    assert response.data == {
        "id": goal.id,
        "category": goal_category.id,
        "created": timezone.localtime(goal.created).isoformat(),
        "updated": timezone.localtime(goal.updated).isoformat(),
        "title": "testgoal",
        "description": None,
        "status": goal.status,
        "priority": goal.priority,
        "due_date": None
    }


@pytest.mark.django_db
def test_goal_list(client, get_credentials, board_participant, goal_category):
    """goal list tests"""
    goals = GoalFactory.create_batch(5, user=board_participant.user, category=goal_category)

    response = client.get(
        path="/goals/goal/list",
        HTTP_AUTHORIZATION=get_credentials
    )

    assert response.status_code == 200
    assert response.data == GoalSerializer(goals, many=True).data


@pytest.mark.django_db
def test_goal_retrieve(client, get_credentials, goal, user, board_participant):
    """goal detail tests"""
    response = client.get(
        path=f"/goals/goal/{goal.id}",
        HTTP_AUTHORIZATION=get_credentials
    )

    assert response.status_code == 200
    assert response.data == GoalSerializer(goal).data


@pytest.mark.django_db
def test_goal_update(client, get_credentials, goal, board_participant):
    """goal update tests"""
    new_title = "updated_title"

    response = client.patch(
        path=f"/goals/goal/{goal.id}",
        HTTP_AUTHORIZATION=get_credentials,
        data={"title": new_title},
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.data.get("title") == new_title


@pytest.mark.django_db
def test_goal_delete(client, get_credentials, goal, board_participant):
    """goal delete tests"""
    response = client.delete(
        path=f"/goals/goal/{goal.id}",
        HTTP_AUTHORIZATION=get_credentials,
    )

    assert response.status_code == 204
    assert response.data is None
