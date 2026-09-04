<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/anmolp1/anmolp1/raw/main/dist/header-dark.svg" />
  <img alt="Anmol Parimoo — AI over BI — Founder, MLDeep Systems" src="https://github.com/anmolp1/anmolp1/raw/main/dist/header-light.svg" width="880" />
</picture>

Dashboards tell you what happened. Most companies stop there: a wall of charts, a weekly meeting about the charts, and decisions that arrive too late. I build the layer above — AI agents that sit on the semantic layer, notice when a number moves, trace the cause, and hand the decision to a person who owns it.

I work across the whole stack, from the dbt models and the warehouse up through the agents, because an agent is only as reliable as the data underneath it.

## What I build

### Keystone

Keystone is an executive decision operating system. It sits read-only above your ERP, accounting system, and CRM. It detects anomalies, traces causal chains, ranks issues by financial impact, and routes each decision to a named owner with a due date. It then records whether the call actually worked. Leadership gets a daily brief, one focused meeting a week, and a ledger of every decision. Deployment takes weeks.

**[mldeep.io/keystone](https://mldeep.io/keystone)**

### agentdx

agentdx is an open-source diagnostic SDK for AI agent systems. Observability tools show you what an agent did; agentdx tells you why it failed. It analyses execution traces and detects seven operational failure pathologies at the reasoning level, aligned with the OWASP Agentic Top 10 and UC Berkeley's MAST framework.

```
pip install agentdx
```

**[pypi.org/project/agentdx](https://pypi.org/project/agentdx/)**

### Executive command centers

I also run bespoke engagements: a semantic layer and AI agents built on your warehouse and tuned to your workflows and approval chains. When an off-the-shelf model isn't enough, I fine-tune small and large language models on your domain, so the agents use your metric definitions, your terminology, and your thresholds.

**[mldeep.io](https://mldeep.io)**

## Selected work

- Designed and built a dbt + BigQuery datamart powering operational analytics for a healthcare company
- Built IaC-managed data-lake ingestion and processing pipelines for a payments platform
- Delivered agent-driven executive briefs over ERP and CRM data for mid-market leadership teams

## Stack

| Layer | Tools |
| --- | --- |
| Agents | MCP · agentdx · FAISS · Chroma |
| Models | Claude & Gemini APIs · fine-tuned SLMs and LLMs · PyTorch |
| Semantic & analytics | dbt · BigQuery · SQL · pandas |
| Platform | GCP (Cloud Run) · Kafka · Redis · Neo4j · Docker · GitHub Actions · Prometheus/Grafana |
| Product | Python · TypeScript · FastAPI · React 19 · SvelteKit · Tailwind |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/anmolp1/anmolp1/raw/main/dist/lang-chart-dark.svg" />
  <img alt="Lines of code by language" src="https://github.com/anmolp1/anmolp1/raw/main/dist/lang-chart-light.svg" />
</picture>

## Contact

[mldeep.io](https://mldeep.io) · [anmol@mldeep.io](mailto:anmol@mldeep.io) · [linkedin.com/in/anmol01](https://linkedin.com/in/anmol01)
