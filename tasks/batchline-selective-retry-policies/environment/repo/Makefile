PYTHON ?= python
PYTHONPATH := src

.PHONY: test check validate-config validate-events validate-policies deployment-report sample-events

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest

validate-config:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) tools/validate_deploy.py --environment production

validate-events:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) tools/validate_events.py examples/events

validate-policies:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) tools/validate_policies.py

deployment-report:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) tools/deployment_report.py --environment production

sample-events:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) tools/sample_events.py

check: test validate-config validate-events validate-policies
