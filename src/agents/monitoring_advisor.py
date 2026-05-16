"""Monitoring Advisor Agent — generates comprehensive monitoring recommendations."""

from src.llm.client import LLMClient

SYSTEM_PROMPT = """You are the **Monitoring Advisor Agent** in a multi-agent monitoring pipeline.
Your role: synthesize all previous analysis to produce a comprehensive monitoring improvement plan.

Output a JSON object with this exact structure:
{
  "strategy": "Overall monitoring improvement strategy",
  "action_items": [
    {
      "priority": "P0|P1|P2|P3",
      "category": "metrics|alerts|dashboards|runbooks|slo|tracing",
      "title": "Action item title",
      "description": "What to do",
      "effort": "low|medium|high",
      "impact": "Expected improvement",
      "implementation_steps": ["step1", "step2"]
    }
  ],
  "slo_recommendations": [
    {
      "service": "service name",
      "slo_type": "availability|latency|error_rate",
      "target": "99.9% or p99 < 200ms",
      "error_budget": "How much error budget",
      "alert_on": "What to alert on"
    }
  ],
  "dashboard_recommendations": [
    {
      "name": "Dashboard name",
      "purpose": "What it shows",
      "panels": ["panel1", "panel2"]
    }
  ],
  "summary": {
    "total_action_items": N,
    "estimated_effort": "low|medium|high",
    "expected_improvement": "Description of improvement"
  }
}

Be comprehensive but practical. Prioritize high-impact, low-effort items first."""


def run(collector_report: dict, anomaly_report: dict, alert_report: dict, client: LLMClient) -> dict:
    import json
    user_msg = json.dumps({
        "collector": collector_report,
        "anomalies": anomaly_report,
        "alerts": alert_report,
    }, ensure_ascii=False, indent=2)
    return client.chat_json(SYSTEM_PROMPT, user_msg)
