from batchline.events.registry import event_type_info, event_types, is_supported_event_type
from batchline.events.validation import registry_schema_errors, schema_event_types


def test_registry_exposes_known_types():
    assert is_supported_event_type("job.failed")
    assert event_type_info("worker.heartbeat").domain == "worker"
    assert {item.name for item in event_types(domain="service")} == {
        "service.config_loaded", "service.config_rejected"
    }


def test_registry_and_schema_cover_the_same_event_types():
    assert registry_schema_errors() == ()
    assert set(schema_event_types()) == {item.name for item in event_types()}
