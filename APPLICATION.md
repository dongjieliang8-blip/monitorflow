# MonitorFlow 申请材料

## 04 字段文本

我构建了一个名为 **MonitorFlow** 的多 Agent 协作智能监控告警优化系统，基于 Claude Code 开发、DeepSeek API 驱动。该项目解决的核心痛点是：监控系统（Prometheus、Grafana、Datadog 等）配置分散，告警规则缺乏基线定义，告警风暴和漏报并存，且监控盲区难以人工识别。MonitorFlow 通过 4 个角色分工明确的 AI Agent 实现指标收集→异常检测→告警关联→优化建议的完整自动化闭环。

核心逻辑流采用长链推理架构：第一层 Metrics Collector Agent 对目标项目的监控配置文件进行深度分析，识别已收集的指标类型、告警规则覆盖度和可观测性盲区，输出结构化 JSON 分析报告；第二层 Anomaly Detector Agent 消费分析报告进行二次推理，检测缺失基线、阈值漂移和配置异常，识别未监控的关键路径；第三层 Alert Correlator Agent 分析告警关联性，设计智能分组策略降低告警噪音，补充缺失告警并建立分级升级矩阵；第四层 Monitoring Advisor Agent 作为最终输出层，综合前三层分析生成全面的监控改进方案，包括 SLO 定义、仪表板推荐和 Runbook 建议。四个 Agent 间通信全部采用结构化 JSON，形成可追溯、可审计的优化链路。

项目使用 Python 构建，CLI 基于 Click + Rich 实现终端可视化。单次完整流水线运行消耗约 200-400 万 Token。该工具将监控运维从被动响应升级为主动预防，显著提升了系统的可观测性和稳定性。

项目地址：https://github.com/dongjieliang8-blip/monitorflow

## 05 截图上传建议

- 终端运行截图：`python -m src.main run ./demo/sample_project`
- 指标分析截图：Collector Agent 的监控覆盖度报告
- 优化建议截图：Advisor 的改进方案
