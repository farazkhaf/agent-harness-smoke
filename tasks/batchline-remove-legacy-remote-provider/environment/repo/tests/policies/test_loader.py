from batchline.policies import load_job_policies


def test_loads_job_policy_catalog():
    catalog = load_job_policies()
    assert len(catalog) == 20
    assert catalog.get("thumbnail").queue == "media"
    assert catalog.get("billing_export").owner == "billing"
    assert catalog.get("daily_digest").retry_policy in {"none", "standard", "aggressive"}


def test_all_policies_have_supported_retry_policy():
    catalog = load_job_policies()
    assert {catalog.get(kind).retry_policy for kind in catalog.kinds()} <= {"none", "standard", "aggressive"}
