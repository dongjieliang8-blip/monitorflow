"""Pipeline orchestrator — wires 4 agents together."""

import json
import time
from dataclasses import dataclass, field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.llm.client import LLMClient, LLMConfig
from src.agents import metrics_collector, anomaly_detector, alert_correlator, monitoring_advisor
from src.utils import collect_monitoring_files, format_files_for_prompt

console = Console()


@dataclass
class PipelineResult:
    collector_report: dict = field(default_factory=dict)
    anomaly_report: dict = field(default_factory=dict)
    alert_report: dict = field(default_factory=dict)
    advisor_report: dict = field(default_factory=dict)
    elapsed_seconds: float = 0.0
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0


class Pipeline:
    def __init__(self, config: LLMConfig | None = None):
        self.client = LLMClient(config)
        self.result = PipelineResult()

    def run(self, target_dir: str, dry_run: bool = False) -> PipelineResult:
        t0 = time.time()

        console.print(Panel.fit("[bold blue]STAGE 1/4: Metrics Collector Agent[/] — collecting metrics config", border_style="blue"))
        files = collect_monitoring_files(target_dir)
        if not files:
            self.result.errors.append("No monitoring config files found in target directory")
            return self.result
        monitoring_text = format_files_for_prompt(files)
        self.result.collector_report = metrics_collector.run(monitoring_text, self.client)
        self._print_collector_summary()

        if dry_run:
            self.result.elapsed_seconds = time.time() - t0
            return self.result

        console.print(Panel.fit("[bold yellow]STAGE 2/4: Anomaly Detector Agent[/] — detecting anomalies", border_style="yellow"))
        self.result.anomaly_report = anomaly_detector.run(self.result.collector_report, self.client)
        self._print_anomaly_summary()

        console.print(Panel.fit("[bold green]STAGE 3/4: Alert Correlator Agent[/] — correlating alerts", border_style="green"))
        self.result.alert_report = alert_correlator.run(self.result.anomaly_report, self.client)
        self._print_alert_summary()

        console.print(Panel.fit("[bold red]STAGE 4/4: Monitoring Advisor Agent[/] — generating recommendations", border_style="red"))
        self.result.advisor_report = monitoring_advisor.run(
            self.result.collector_report,
            self.result.anomaly_report,
            self.result.alert_report,
            self.client,
        )
        self._print_advisor_summary()

        self.result.elapsed_seconds = time.time() - t0
        self._print_final_summary()
        return self.result

    def _print_collector_summary(self):
        m = self.result.collector_report.get("metrics", {})
        table = Table(title="Metrics Collection Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta")
        for key in ["total_configs", "total_metrics", "total_alerts", "coverage_gaps", "critical_issues"]:
            table.add_row(key.replace("_", " ").title(), str(m.get(key, "?")))
        console.print(table)

    def _print_anomaly_summary(self):
        m = self.result.anomaly_report.get("metrics", {})
        console.print(f"[yellow]Anomalies:[/] {m.get('total_anomalies', '?')} "
                       f"(Critical: {m.get('critical', 0)}, High: {m.get('high', 0)})")
        console.print(f"[yellow]Blind spots:[/] {m.get('blind_spots', 0)}")

    def _print_alert_summary(self):
        m = self.result.alert_report.get("metrics", {})
        console.print(f"[green]Alert groups:[/] {m.get('alert_groups', 0)}")
        console.print(f"[green]Noise issues:[/] {m.get('noise_issues', 0)}")
        console.print(f"[green]Missing alerts:[/] {m.get('missing_alerts', 0)}")

    def _print_advisor_summary(self):
        items = self.result.advisor_report.get("action_items", [])
        console.print(f"[red]Action items:[/] {len(items)}")
        for item in items[:5]:
            console.print(f"  • [bold]{item.get('priority', '?')}[/] {item.get('title', 'Untitled')}")

    def _print_final_summary(self):
        console.print()
        console.print(Panel.fit(
            f"[bold]Pipeline Complete[/]\n"
            f"Time: {self.result.elapsed_seconds:.1f}s\n"
            f"Errors: {len(self.result.errors)}",
            border_style="green" if self.result.success else "red"
        ))

    def save_report(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "collector_report": self.result.collector_report,
                "anomaly_report": self.result.anomaly_report,
                "alert_report": self.result.alert_report,
                "advisor_report": self.result.advisor_report,
                "elapsed_seconds": self.result.elapsed_seconds,
                "errors": self.result.errors,
            }, f, ensure_ascii=False, indent=2)
        console.print(f"[green]Report saved to {path}[/]")
