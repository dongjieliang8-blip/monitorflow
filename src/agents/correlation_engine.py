"""告警关联 Agent - 负责关联多个告警事件，识别根本原因"""

import json
from typing import Any, Dict
from ..utils import call_llm


SYSTEM_PROMPT = """你是一个专业的告警关联分析专家。
你的任务是分析多个告警事件，识别它们之间的关联关系和共同模式。
请返回 JSON 格式的结果。"""


def analyze(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    关联分析多个告警事件

    Args:
        data: 包含异常检测结果的字典

    Returns:
        告警关联分析结果字典
    """
    prompt = f"""请分析以下异常检测结果，进行告警关联分析：

{json.dumps(data, ensure_ascii=False, indent=2)}

请返回 JSON 格式，包含以下字段：
- correlated_alerts: 关联的告警组列表，每组包含：
  - group_id: 告警组ID
  - alerts: 相关告警列表
  - correlation_type: 关联类型（temporal/dependency/resource）
  - confidence: 关联置信度（0-1）
  - description: 关联描述
- root_cause_candidates: 根本原因候选列表
- impact_assessment: 影响评估
- priority: 处理优先级（P0/P1/P2/P3）
- escalation_needed: 是否需要升级处理
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
                    "agent": "correlation_engine"
                }
        else:
            result = {
                "raw_response": response,
                "status": "parse_error",
                "agent": "correlation_engine"
            }

    result["agent"] = "correlation_engine"
    return result
