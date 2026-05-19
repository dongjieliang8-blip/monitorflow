"""指标采集 Agent - 负责收集和整理监控指标数据"""

import json
from typing import Any, Dict, List
from ..utils import call_llm


SYSTEM_PROMPT = """你是一个专业的监控指标采集分析专家。
你的任务是分析原始监控指标数据，提取关键信息并生成结构化的指标报告。
请返回 JSON 格式的结果。"""


def analyze(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析监控指标数据

    Args:
        data: 包含监控指标数据的字典

    Returns:
        分析结果字典
    """
    prompt = f"""请分析以下监控指标数据，提取关键指标并生成报告：

监控数据：
{json.dumps(data, ensure_ascii=False, indent=2)}

请返回 JSON 格式，包含以下字段：
- total_metrics: 指标总数
- collected_metrics: 已采集的有效指标列表
- metric_summary: 各指标摘要（名称、当前值、单位）
- time_range: 数据时间范围
- data_quality: 数据质量评估
- issues: 发现的问题列表
"""

    response = call_llm(prompt, SYSTEM_PROMPT)

    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        # 尝试提取 JSON 部分
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
            except json.JSONDecodeError:
                result = {
                    "raw_response": response,
                    "status": "parse_error",
                    "agent": "metric_collector"
                }
        else:
            result = {
                "raw_response": response,
                "status": "parse_error",
                "agent": "metric_collector"
            }

    result["agent"] = "metric_collector"
    return result
