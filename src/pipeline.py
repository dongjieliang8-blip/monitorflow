"""MonitorFlow 流水线编排模块"""

import json
import os
from typing import Any, Dict, Optional
from datetime import datetime

from .agents import metric_collector, anomaly_detector, correlation_engine, root_cause_advisor


class MonitorFlowPipeline:
    """
    MonitorFlow 智能监控告警流水线

    流程：指标采集 -> 异常检测 -> 告警关联 -> 根因定位
    """

    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None

    def run(self, input_path: str) -> Dict[str, Any]:
        """
        运行监控分析流水线

        Args:
            input_path: 输入数据文件路径

        Returns:
            汇总分析结果
        """
        self.start_time = datetime.now()
        print(f"[MonitorFlow] 开始监控分析流水线 - {self.start_time}")

        # 读取输入数据
        input_data = self._load_input(input_path)

        # Step 1: 指标采集
        print("[MonitorFlow] Step 1/4 - 指标采集中...")
        self.results["metric_collector"] = metric_collector.analyze(input_data)
        print("[MonitorFlow] Step 1 完成")

        # Step 2: 异常检测
        print("[MonitorFlow] Step 2/4 - 异常检测中...")
        self.results["anomaly_detector"] = anomaly_detector.analyze(
            self.results["metric_collector"]
        )
        print("[MonitorFlow] Step 2 完成")

        # Step 3: 告警关联
        print("[MonitorFlow] Step 3/4 - 告警关联分析中...")
        self.results["correlation_engine"] = correlation_engine.analyze(
            self.results["anomaly_detector"]
        )
        print("[MonitorFlow] Step 3 完成")

        # Step 4: 根因定位
        print("[MonitorFlow] Step 4/4 - 根因定位分析中...")
        self.results["root_cause_advisor"] = root_cause_advisor.analyze(
            self.results["correlation_engine"]
        )
        print("[MonitorFlow] Step 4 完成")

        self.end_time = datetime.now()

        # 生成汇总报告
        summary = self._generate_summary()
        print(f"[MonitorFlow] 流水线完成 - 耗时 {(self.end_time - self.start_time).total_seconds():.2f}s")

        return summary

    def _load_input(self, input_path: str) -> Dict[str, Any]:
        """加载输入数据"""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入文件不存在: {input_path}")

        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _generate_summary(self) -> Dict[str, Any]:
        """生成汇总分析报告"""
        summary = {
            "pipeline": "MonitorFlow",
            "version": "1.0.0",
            "execution_time": {
                "start": self.start_time.isoformat() if self.start_time else None,
                "end": self.end_time.isoformat() if self.end_time else None,
                "duration_seconds": (
                    (self.end_time - self.start_time).total_seconds()
                    if self.start_time and self.end_time
                    else None
                )
            },
            "agent_results": self.results,
            "summary": self._extract_key_findings()
        }
        return summary

    def _extract_key_findings(self) -> Dict[str, Any]:
        """提取关键发现"""
        findings = {
            "total_anomalies": 0,
            "severity_summary": {},
            "root_causes": [],
            "recommendations": [],
            "priority": "P3"
        }

        # 从异常检测结果提取信息
        anomaly_result = self.results.get("anomaly_detector", {})
        if "anomaly_count" in anomaly_result:
            findings["total_anomalies"] = anomaly_result["anomaly_count"]
        if "severity_summary" in anomaly_result:
            findings["severity_summary"] = anomaly_result["severity_summary"]

        # 从根因分析提取信息
        root_cause_result = self.results.get("root_cause_advisor", {})
        if "root_cause_analysis" in root_cause_result:
            rca = root_cause_result["root_cause_analysis"]
            if "primary_root_cause" in rca:
                findings["root_causes"].append(rca["primary_root_cause"])
        if "fix_recommendations" in root_cause_result:
            findings["recommendations"] = root_cause_result["fix_recommendations"]

        # 从关联分析提取优先级
        correlation_result = self.results.get("correlation_engine", {})
        if "priority" in correlation_result:
            findings["priority"] = correlation_result["priority"]

        return findings
