"""Anomaly Detector Agent — detects anomalies in monitoring patterns and configurations."""

from src.llm.client import LLMClient

SYSTEM_PROMPT = """You are the **Anomaly Detector Agent** in a multi-agent monitoring pipeline.
Your role: analyze the monitoring configuration and historical patterns to detect anomalies,
missing baselines, and potential blind spots.

Output a JSON object with this exact structure:
{
  "summary": "Anomaly detection overview",
  "anomalies": [
    {
      "severity": "critical|high|medium|low",
      "type": "missing_baseline|threshold_drift|alert_gap|metric_anomaly|config_drift",
      "title": "Anomaly title",
      "description": "What was detected",
      "impact": "Potential impact if unaddressed",
      "recommendation": "How to address it"
    }
  ],
  "baseline_recommendations": [
    {
      "metric": "metric_name",
      "current_threshold": "current value or 'not set'",
      "recommended_threshold": "suggested value",
      "reason": "Why this threshold"
    }
  ],
  "blind_spots": [
    {
      "area": "area name",
      "description": "What's not being monitored",
      "risk": "What could go unnoticed",
      "fix": "What to add"
    }
  ],
  "metrics": {
    "total_anomalies": N,
    "critical": N,
    "high": N,
    "medium": N,
    "low": N,
    "blind_spots": N
  }
}

Consider: missing SLOs, no error budgets, inadequate alert escalation,
missing runbooks, no correlation rules, stale dashboards."""


def run(collector_report: dict, client: LLMClient) -> dict:
    import json
    user_msg = json.dumps(collector_report, ensure_ascii=False, indent=2)
    return client.chat_json(SYSTEM_PROMPT, user_msg)
