"""Main Observer CLI application."""

import time
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .ai import AIAnalyzer
from .capture import ScreenCapture
from .database import Database
from .models import ActivityRecord, ContextWindow

console = Console()
app = typer.Typer(no_args_is_help=True)


class Observer:
    """Main Observer application."""
    
    def __init__(self, data_dir: Path = Path("./data")):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        
        self.db = Database(data_dir / "observer.db")
        self.capture = ScreenCapture(data_dir / "screenshots")
        self.ai = AIAnalyzer()
    
    def run_cycle(self) -> ActivityRecord:
        """Single observation cycle."""
        # Capture screenshot
        screenshot_path, window_info = self.capture.capture()
        
        # Get context from recent activities
        recent = self.db.get_recent_activities(minutes=10)
        context = ContextWindow(
            recent_activities=recent,
            current_window=window_info
        )
        
        # Analyze with AI
        output = self.ai.analyze(screenshot_path, context)
        
        # Create database record
        record = ActivityRecord(
            timestamp=datetime.now(),
            window_title=window_info['title'],
            window_class=window_info['class'],
            project_name=output.project_name,
            project_type=output.project_type,
            details=output.details,
            confidence=output.confidence,
            screenshot_path=str(screenshot_path),
            context_summary=self._summarize_context(recent)
        )
        
        # Save to database
        self.db.save_activity(record, screenshot_path)
        
        # Display result
        self._display_activity(record)
        
        return record
    
    def _summarize_context(self, recent: list[ActivityRecord]) -> str:
        """Create summary of recent activities."""
        if not recent:
            return "Starting new session"
        
        projects = {}
        for act in recent:
            if act.project_name not in projects:
                projects[act.project_name] = []
            projects[act.project_name].append(act.details)
        
        summary = "Recent: " + ", ".join(
            f"{name} ({len(details)} activities)" 
            for name, details in projects.items()
        )
        return summary
    
    def _display_activity(self, record: ActivityRecord):
        """Pretty print activity."""
        table = Table(show_header=False, box=None)
        table.add_column("Field", style="cyan", width=12)
        table.add_column("Value", style="white")
        
        table.add_row("Time", record.timestamp.strftime("%H:%M:%S"))
        table.add_row("Project", record.project_name)
        table.add_row("Type", record.project_type.value.replace("_", " "))
        table.add_row("Details", record.details)
        table.add_row("Confidence", f"{record.confidence:.1%}")
        
        console.print(table)
        console.print()


@app.command()
def run(
    interval: int = typer.Option(1, help="Capture interval in seconds"),
    data_dir: str = typer.Option("./data", help="Data directory path")
):
    """Run observer with specified interval."""
    observer = Observer(Path(data_dir))
    console.print("[green]Starting Observer...[/green]")
    
    try:
        while True:
            observer.run_cycle()
            time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n[red]Observer stopped[/red]")


@app.command()
def history(
    minutes: int = typer.Option(60, help="Minutes of history to show"),
    data_dir: str = typer.Option("./data", help="Data directory path")
):
    """Show activity history."""
    observer = Observer(Path(data_dir))
    activities = observer.db.get_recent_activities(minutes)
    
    if not activities:
        console.print("[yellow]No recent activities found[/yellow]")
        return
    
    table = Table(title="Activity History")
    table.add_column("Time", style="cyan")
    table.add_column("Project", style="green")
    table.add_column("Details", style="white")
    table.add_column("Confidence", style="yellow")
    
    for act in reversed(activities):
        table.add_row(
            act.timestamp.strftime("%H:%M:%S"),
            act.project_name,
            act.details[:60] + "..." if len(act.details) > 60 else act.details,
            f"{act.confidence:.1%}"
        )
    
    console.print(table)


if __name__ == "__main__":
    app()
