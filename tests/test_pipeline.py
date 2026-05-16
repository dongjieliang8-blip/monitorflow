"""Basic smoke tests for MonitorFlow modules."""

import tempfile
from pathlib import Path


def test_collect_monitoring_files():
    from src.utils import collect_monitoring_files

    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "prometheus.yml").write_text("global:\n  scrape_interval: 15s\n")
        Path(tmp, "app.py").write_text("print('hello')")
        Path(tmp, ".git").mkdir()

        files = collect_monitoring_files(tmp)
        paths = [f["path"] for f in files]
        assert "prometheus.yml" in paths


def test_pipeline_imports():
    from src.pipeline import Pipeline
    from src.agents import metrics_collector, anomaly_detector, alert_correlator, monitoring_advisor
    assert Pipeline is not None
    assert metrics_collector.SYSTEM_PROMPT
    assert anomaly_detector.SYSTEM_PROMPT
    assert alert_correlator.SYSTEM_PROMPT
    assert monitoring_advisor.SYSTEM_PROMPT
