# MonitorFlow — 智能监控告警流水线

基于多 Agent 长链推理的智能监控告警系统。

## 安装

```bash
pip install -r requirements.txt
```

## 配置

在项目根目录创建 `.env` 文件：

```
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
DEEPSEEK_MODEL=mimo-v2.5
```

## 使用

```bash
# 运行监控分析
python -m src.main monitor --input ./demo/sample_data/sample_metrics.json

# 查看报告
python -m src.main report --input ./output/monitorflow_report.json
```

## 项目结构

```
monitorflow/
├── src/
│   ├── main.py
│   ├── pipeline.py
│   ├── utils.py
│   └── agents/
│       ├── metric_collector.py
│       ├── anomaly_detector.py
│       ├── correlation_engine.py
│       └── root_cause_advisor.py
├── demo/sample_data/
├── tests/
├── requirements.txt
└── APPLICATION.md
```
