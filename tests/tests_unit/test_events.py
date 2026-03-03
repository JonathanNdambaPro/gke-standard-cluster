import pytest
from pydantic import ValidationError

from api.models.events import EventInputModel, EventModelV1

# ===================================================================
# EVENT INPUT MODEL TESTS
# ===================================================================


def test_create_valid_event_input():
    """Test creating a valid EventInputModel."""
    event = EventInputModel(name="Jonathan", lastname="Ndamba")
    assert event.name == "Jonathan"
    assert event.lastname == "Ndamba"


def test_event_input_missing_required_field_name():
    """Test that name field is required."""
    with pytest.raises(ValidationError) as exc_info:
        EventInputModel(lastname="Ndamba")

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("name",) for error in errors)


def test_event_input_missing_required_field_lastname():
    """Test that lastname field is required."""
    with pytest.raises(ValidationError) as exc_info:
        EventInputModel(name="Jonathan")

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("lastname",) for error in errors)


def test_event_input_empty_string_values():
    """Test that empty strings are accepted."""
    event = EventInputModel(name="", lastname="")
    assert event.name == ""
    assert event.lastname == ""


def test_event_input_model_dump():
    """Test serialization of EventInputModel."""
    event = EventInputModel(name="Jonathan", lastname="Ndamba")
    data = event.model_dump()
    assert data == {"name": "Jonathan", "lastname": "Ndamba"}


def test_event_input_model_dump_json():
    """Test JSON serialization."""
    event = EventInputModel(name="Jonathan", lastname="Ndamba")
    json_str = event.model_dump_json()
    assert "Jonathan" in json_str
    assert "Ndamba" in json_str


# ===================================================================
# EVENT MODEL V1 TESTS
# ===================================================================


def test_create_valid_event_model_v1():
    """Test creating a valid EventModelV1."""
    event = EventModelV1(id="123abc", name="Jonathan", lastname="Ndamba")
    assert event.id_ == "123abc"
    assert event.name == "Jonathan"
    assert event.lastname == "Ndamba"


def test_event_v1_create_with_alias_id():
    """Test creating EventModelV1 using 'id' alias."""
    event = EventModelV1(id="456def", name="Jonathan", lastname="Ndamba")
    assert event.id_ == "456def"


def test_event_v1_missing_required_field_id():
    """Test that id field is required."""
    with pytest.raises(ValidationError) as exc_info:
        EventModelV1(name="Jonathan", lastname="Ndamba")

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("id",) for error in errors)


def test_event_v1_missing_required_field_name():
    """Test that name field is required."""
    with pytest.raises(ValidationError) as exc_info:
        EventModelV1(id="123", lastname="Ndamba")

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("name",) for error in errors)


def test_event_v1_missing_required_field_lastname():
    """Test that lastname field is required."""
    with pytest.raises(ValidationError) as exc_info:
        EventModelV1(id="123", name="Jonathan")

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("lastname",) for error in errors)


def test_event_v1_model_dump_with_alias():
    """Test that serialization uses the 'id' alias."""
    event = EventModelV1(id="789ghi", name="Jonathan", lastname="Ndamba")
    data = event.model_dump(by_alias=True)
    assert data == {"id": "789ghi", "name": "Jonathan", "lastname": "Ndamba"}
    assert "id_" not in data


def test_event_v1_model_dump_without_alias():
    """Test serialization without alias."""
    event = EventModelV1(id="789ghi", name="Jonathan", lastname="Ndamba")
    data = event.model_dump(by_alias=False)
    assert data["id_"] == "789ghi"
    assert data["name"] == "Jonathan"
    assert data["lastname"] == "Ndamba"


def test_event_v1_populate_by_name_config():
    """Test that both 'id' and 'id_' can be used during initialization."""
    # Using the alias 'id'
    event1 = EventModelV1(id="abc123", name="John", lastname="Doe")
    assert event1.id_ == "abc123"

    # Using the actual field name 'id_'
    event2 = EventModelV1(id_="def456", name="Jane", lastname="Smith")
    assert event2.id_ == "def456"


def test_event_v1_special_characters_in_fields():
    """Test handling of special characters."""
    event = EventModelV1(id="special-id_123!@#", name="Jean-Pierre", lastname="O'Brien")
    assert event.id_ == "special-id_123!@#"
    assert event.name == "Jean-Pierre"
    assert event.lastname == "O'Brien"


def test_event_v1_model_json_serialization():
    """Test JSON serialization."""
    event = EventModelV1(id="json123", name="Jonathan", lastname="Ndamba")
    json_str = event.model_dump_json()
    assert "json123" in json_str
    assert "Jonathan" in json_str
    assert "Ndamba" in json_str


def test_event_v1_from_dict_with_alias():
    """Test creating model from dictionary with alias."""
    data = {"id": "dict123", "name": "Test", "lastname": "User"}
    event = EventModelV1(**data)
    assert event.id_ == "dict123"
    assert event.name == "Test"
    assert event.lastname == "User"
