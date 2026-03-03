import pytest
from temporalio import activity

from api.models.events import EventModelV1
from api.temporal_workflows.hello.config_excution_temporal import config_temporal_hello


@pytest.fixture
def mock_event_model_v1() -> EventModelV1:
    return EventModelV1(id="some_id", name="Jonathan", lastname="Ndamba")


# @pytest.fixture
# def mock_hello_activities(mocker):



@pytest.fixture
def mock_hello_your_activy():
    @activity.defn(name=config_temporal_hello.activity_name)
    async def your_activity(self, *_, **__) -> str:
        return "hello Jonathan, Ndamba!"

    return your_activity


@pytest.fixture
def mock_hello_your_activy_name():
    @activity.defn(name=f"{config_temporal_hello.activity_name}_name")
    async def your_activity_name(self, *_, **__) -> str:
        return "hello Jonathan, "

    return your_activity_name


@pytest.fixture
def mock_hello_your_activy_lastname():
    @activity.defn(name=f"{config_temporal_hello.activity_name}_lastname")
    async def your_activity_lastname(_: EventModelV1, prefix: str) -> str:
        # Concat prefix from first activity with lastname
        return prefix + "Ndamba!"

    return your_activity_lastname
