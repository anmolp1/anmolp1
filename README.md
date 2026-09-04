<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/anmolp1/anmolp1/raw/main/dist/header-dark.svg" />
  <img alt="Anmol Parimoo, AI over BI. Founder, MLDeep Systems" src="https://github.com/anmolp1/anmolp1/raw/main/dist/header-light.svg" width="880" />
</picture>

Dashboards tell you what happened. The decision about what to do next still gets made late, in a weekly meeting, by whoever happened to notice the number. I build the layer above the dashboard: AI agents on the semantic layer that trace why a metric moved and route the decision to a person who owns it.

I work across the whole stack, from the dbt models and the warehouse up through the agents. An agent inherits every problem in the data underneath it, so I build both.

## What I build

### Keystone

Keystone is an executive decision operating system. It sits read-only above your ERP, accounting system, and CRM. When something drifts, it traces the cause, sizes the financial impact, and routes the decision to a named owner with a due date. It also records whether the call worked. Leadership gets a daily brief, one focused meeting a week, and a ledger of every decision. Deployment takes weeks.

**[mldeep.io/keystone](https://mldeep.io/keystone)**

### agentdx

agentdx is an open-source diagnostic SDK for AI agent systems. Tracing tools show what an agent did. agentdx reads the same execution traces and identifies which of seven operational failure pathologies caused the breakdown, following the OWASP Agentic Top 10 and UC Berkeley's MAST framework.

```
pip install agentdx
```

**[pypi.org/project/agentdx](https://pypi.org/project/agentdx/)**

### Executive command centers

I also take on bespoke engagements: a semantic layer and AI agents built on your warehouse and wired into your approval chains. When an off-the-shelf model isn't enough, I fine-tune small and large language models on your domain so the agents work with your metric definitions and terminology.

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
