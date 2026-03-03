import pytest
from temporalio.testing import ActivityEnvironment

from api.temporal_workflows.hello.your_activities_dacx import HelloActivities


@pytest.mark.asyncio
async def test_your_activity(mock_event_model_v1):
    output = "hello Jonathan, Ndamba!"
    activity_environment = ActivityEnvironment()
    activities = HelloActivities()

    assert output == await activity_environment.run(activities.your_activity, mock_event_model_v1)
