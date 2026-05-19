"""根因定位 Agent - 负责分析并定位问题的根本原因"""

import json
from typing import Any, Dict
from ..utils import call_llm


SYSTEM_PROMPT = """你是一个专业的根因分析专家。
你的任务是基于告警关联分析结果，深入分析并定位问题的根本原因，提供修复建议。
请返回 JSON 格式的结果。"""


def analyze(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    根因分析和定位

    Args:
        data: 包含告警关联分析结果的字典

    Returns:
        根因分析结果字典
    """
    prompt = f"""请基于以下告警关联分析结果，进行根因分析和定位：

{json.dumps(data, ensure_ascii=False, indent=2)}

请返回 JSON 格式，包含以下字段：
- root_cause_analysis: 根因分析结果，包含：
  - primary_root_cause: 主要根因
  - contributing_factors: 诱因列表
  - evidence: 支撑证据
  - confidence_score: 置信度（0-1）
- fix_recommendations: 修复建议列表，每条包含：
  - action: 建议操作
  - priority: 优先级
  - estimated_impact: 预期影响
  - owner: 建议负责人
- prevention_measures: 预防措施
- similar_incidents: 类似事件参考
- resolution_steps: 解决步骤
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
                    "agent": "root_cause_advisor"
                }
        else:
            result = {
                "raw_response": response,
                "status": "parse_error",
                "agent": "root_cause_advisor"
            }

    result["agent"] = "root_cause_advisor"
    return result
