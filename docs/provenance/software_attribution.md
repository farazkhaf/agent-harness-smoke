# Software and service attribution

Agent Harness Smoke is built and evaluated with third-party software and hosted model infrastructure. This page records the components that are material to reproducing the recorded executions; it is not a claim that those projects endorse this work.

| Component | Version / identity used | Role in this project | Reference |
|---|---|---|---|
| Harbor | 0.22.0 | Task execution, agent/environment orchestration, trial records, and verifier execution | Harbor Framework Team, *Harbor: A framework for evaluating and optimizing agents and models in container environments*. Apache-2.0. Concept DOI: `10.5281/zenodo.20953922`. https://github.com/harbor-framework/harbor |
| Docker Engine | Docker-backed local execution | Container build and task environment runtime used by Harbor | https://docs.docker.com/engine/ |
| OpenCode | 1.18.30 | Public coding-agent harness used in the focused suite and Scenario 1 | https://github.com/anomalyco/opencode/releases/tag/v1.18.30 |
| Mini-SWE-Agent | 2.4.6 | Public coding-agent harness used in the focused suite and Scenario 1 | https://github.com/SWE-agent/mini-swe-agent/releases/tag/v2.4.6 |
| GLM-5.3-Flash | `accounts/fireworks/models/glm-5p3-flash` | Language model used for the recorded public-harness runs and Scenario 1 custom-harness runs | Z.ai model served through Fireworks AI: https://fireworks.ai/models/fireworks/glm-5p3-flash |
| Fireworks AI | serverless inference service | Model provider for the recorded GLM-5.3-Flash executions | https://fireworks.ai/ |

Harbor 0.22.0 is the Harbor version used throughout the recorded focused and Scenario 1 executions. Harbor's own `CITATION.cff` identifies version 0.22.0, an Apache-2.0 license, and the concept DOI above.

Mini-SWE-Agent's upstream repository asks users of that work to cite the SWE-agent paper:

> John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik R. Narasimhan, and Ofir Press. “SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.” NeurIPS 2024. https://arxiv.org/abs/2405.15793

The Agent Harness Smoke source release does not vendor Harbor, Docker Engine, OpenCode, Mini-SWE-Agent, GLM model weights, or Fireworks service code. Runtime profiles and build scripts refer to external software that remains subject to its own license and service terms.

The private `custom-harness` is an independent execution configuration and is not redistributed in this repository.
