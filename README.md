# MonitorFlow

> AI-powered multi-agent monitoring optimization pipeline
> AI 驱动的多 Agent 智能监控优化流水线

---

## What is MonitorFlow? / 什么是 MonitorFlow?

MonitorFlow is a multi-agent collaborative system that analyzes your monitoring configurations (Prometheus, Grafana, Datadog, etc.), detects anomalies and blind spots, correlates alerts to reduce noise, and generates actionable improvement recommendations.

MonitorFlow 是一个多 Agent 协作系统，深度分析监控配置（Prometheus、Grafana、Datadog 等），检测异常和盲区，关联告警降低噪音，并生成可执行的优化建议。

## Architecture / 架构

```
Metrics Collector --> Anomaly Detector --> Alert Correlator --> Advisor
   (指标收集器)         (异常检测器)         (告警关联器)       (优化顾问)
```

**Four specialized agents run in sequence:**

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| Metrics Collector | Analyze monitoring configs, identify metrics & gaps | Raw config files | Coverage report |
| Anomaly Detector | Detect missing baselines, blind spots, config drift | Collector report | Anomaly report |
| Alert Correlator | Correlate alerts, reduce noise, design grouping | Anomaly report | Alert strategy |
| Monitoring Advisor | Synthesize all analysis into improvement plan | All 3 reports | Action plan |

## Quick Start / 快速开始

```bash
# 1. Clone
git clone https://github.com/dongjieliang8-blip/monitorflow.git
cd monitorflow

# 2. Install
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env, fill in your DeepSeek API key

# 4. Run on demo project
python -m src.main run ./demo/sample_project

# 5. Dry run (metrics collector only)
python -m src.main run ./demo/sample_project --dry-run

# 6. Check config
python -m src.main config
```

## Demo / 演示

```bash
python -m src.main run ./demo/sample_project -o report.json
```

Expected output:
```
+-------------------------------------------------------+
|              MonitorFlow Pipeline                      |
|  Target: ./demo/sample_project                        |
|  Model: deepseek-chat                                 |
|  Mode: Full Pipeline                                  |
+-------------------------------------------------------+
[STAGE 1/4] Metrics Collector Agent ...
[STAGE 2/4] Anomaly Detector Agent ...
[STAGE 3/4] Alert Correlator Agent ...
[STAGE 4/4] Monitoring Advisor Agent ...

+-----------------------+
| Pipeline Complete      |
| Time: 45.2s           |
| Errors: 0             |
+-----------------------+
```

## CLI Commands / 命令行

| Command | Description |
|---------|-------------|
| `run <target>` | Full 4-agent pipeline on target directory |
| `collect <target>` | Metrics collector only (quick scan) |
| `config` | Show current LLM configuration |

### Options / 选项

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` | false | Run metrics collector only |
| `-o, --output` | monitorflow_report.json | Output report path |
| `--model` | deepseek-chat | LLM model override |
| `--temperature` | 0.3 | LLM temperature |

## Tech Stack / 技术栈

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| LLM API | DeepSeek via OpenAI SDK |
| CLI Framework | Click |
| Terminal UI | Rich |
| Multi-Agent | 4-agent sequential pipeline |
| Config Parsing | YAML, JSON, TOML, INI |

## Project Structure / 项目结构

```
monitorflow/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── pipeline.py           # Pipeline orchestrator
│   ├── utils.py              # File collection utilities
│   ├── llm/
│   │   ├── __init__.py
│   │   └── client.py         # OpenAI-compatible LLM client
│   └── agents/
│       ├── __init__.py
│       ├── metrics_collector.py    # Agent 1
│       ├── anomaly_detector.py     # Agent 2
│       ├── alert_correlator.py     # Agent 3
│       └── monitoring_advisor.py   # Agent 4
├── demo/
│   └── sample_project/       # Sample Prometheus/Grafana configs
├── tests/
│   └── test_pipeline.py      # Smoke tests
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── APPLICATION.md
```

## Token Consumption / Token 消耗

Single full pipeline run: ~200-400 万 Token

## License

MIT
