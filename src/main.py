"""MonitorFlow CLI 入口"""

import json
import os
import click
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from .pipeline import MonitorFlowPipeline


console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="MonitorFlow")
def cli():
    """MonitorFlow - 智能监控告警流水线"""
    pass


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="输出报告文件路径")
@click.option("--verbose", "-v", is_flag=True, help="显示详细信息")
def monitor(input_path: str, output: str, verbose: bool):
    """运行监控分析流水线"""
    console.print(Panel.fit(
        "[bold green]MonitorFlow 智能监控告警流水线[/bold green]",
        subtitle=f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ))

    try:
        pipeline = MonitorFlowPipeline()
        result = pipeline.run(input_path)

        # 显示关键发现
        _display_summary(result)

        # 保存报告
        if output:
            _save_report(result, output)
            console.print(f"\n[green]报告已保存到: {output}[/green]")
        else:
            # 默认保存到 demo/output 目录
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "demo", "output")
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_output = os.path.join(output_dir, f"report_{timestamp}.json")
            _save_report(result, default_output)
            console.print(f"\n[green]报告已保存到: {default_output}[/green]")

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        raise click.Abort()


@cli.command()
@click.argument("report_path", type=click.Path(exists=True))
def report(report_path: str):
    """查看分析报告"""
    console.print(Panel.fit(
        "[bold blue]MonitorFlow 分析报告[/bold blue]",
        subtitle=f"报告文件: {report_path}"
    ))

    try:
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 显示基本信息
        if "execution_time" in data:
            time_info = data["execution_time"]
            table = Table(title="执行信息")
            table.add_column("字段", style="cyan")
            table.add_column("值", style="green")
            table.add_row("开始时间", time_info.get("start", "N/A"))
            table.add_row("结束时间", time_info.get("end", "N/A"))
            table.add_row("耗时(秒)", str(time_info.get("duration_seconds", "N/A")))
            console.print(table)

        # 显示关键发现
        if "summary" in data:
            _display_summary(data)

        # 显示详细结果
        if "agent_results" in data:
            for agent_name, agent_result in data["agent_results"].items():
                console.print(f"\n[bold cyan]--- {agent_name} ---[/bold cyan]")
                if isinstance(agent_result, dict):
                    for key, value in agent_result.items():
                        if key != "agent":
                            console.print(f"  {key}: {value}")

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        raise click.Abort()


def _display_summary(result: dict):
    """显示汇总信息"""
    if "summary" in result:
        summary = result["summary"]

        # 异常统计表
        if "total_anomalies" in summary:
            table = Table(title="监控分析汇总")
            table.add_column("指标", style="cyan")
            table.add_column("值", style="green")
            table.add_row("检测到的异常数", str(summary.get("total_anomalies", 0)))
            table.add_row("处理优先级", str(summary.get("priority", "N/A")))

            if "root_causes" in summary:
                for i, rc in enumerate(summary["root_causes"][:3], 1):
                    table.add_row(f"根因 {i}", str(rc)[:50])

            console.print(table)

        # 推荐操作
        if "recommendations" in summary and summary["recommendations"]:
            console.print("\n[bold yellow]推荐操作:[/bold yellow]")
            for i, rec in enumerate(summary["recommendations"][:5], 1):
                if isinstance(rec, dict):
                    action = rec.get("action", "N/A")
                    priority = rec.get("priority", "N/A")
                    console.print(f"  {i}. [{priority}] {action}")
                else:
                    console.print(f"  {i}. {rec}")


def _save_report(result: dict, path: str):
    """保存报告到文件"""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    cli()
