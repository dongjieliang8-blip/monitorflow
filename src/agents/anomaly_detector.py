"""异常检测 Agent - 负责检测指标中的异常模式"""

import json
from typing import Any, Dict
from ..utils import call_llm


SYSTEM_PROMPT = """你是一个专业的异常检测分析专家。
你的任务是分析监控指标数据，识别潜在的异常和异常模式。
请返回 JSON 格式的结果。"""


def analyze(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    检测监控数据中的异常

    Args:
        data: 包含指标分析结果的字典

    Returns:
        异常检测结果字典
    """
    prompt = f"""请分析以下监控指标数据，检测异常和异常模式：

{json.dumps(data, ensure_ascii=False, indent=2)}

请返回 JSON 格式，包含以下字段：
- anomalies: 检测到的异常列表，每个异常包含：
  - metric_name: 指标名称
  - anomaly_type: 异常类型（spike/drop/sustained_high/sustained_low）
  - severity: 严重程度（critical/warning/info）
  - current_value: 当前值
  - expected_range: 期望范围
  - timestamp: 异常时间
  - description: 异常描述
- anomaly_count: 异常总数
- severity_summary: 各严重程度的统计
- overall_status: 整体状态（healthy/degraded/critical）
- recommendations: 建议采取的行动
"""

    response = call_llm(prompt, SYSTEM_PROMPT)

    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
            except json.JSONDecodeError:
                result = {
                    "raw_response": response,
                    "status": "parse_error",
                    "agent": "anomaly_detector"
                }
        else:
            result = {
                "raw_response": response,
                "status": "parse_error",
                "agent": "anomaly_detector"
            }

    result["agent"] = "anomaly_detector"
    return result
