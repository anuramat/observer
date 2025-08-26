"""AI analysis functionality."""

import json
import subprocess
from pathlib import Path
from pydantic import ValidationError

from .models import ActivityOutput, ContextWindow, ProjectType


class AIAnalyzer:
    """AI-powered screenshot analysis."""
    
    def __init__(self, model: str = "llama-cpp"):
        self.model = model
    
    def analyze(self, screenshot_path: Path, context: ContextWindow) -> ActivityOutput:
        """Analyze screenshot with context."""
        prompt = self._build_prompt(context)
        schema = self._get_schema()
        
        cmd = [
            "mods", "--no-cache", "-q",
            "-i", str(screenshot_path),
            "-j", json.dumps(schema),
            "-a", self.model,
            "-m", "dummy",
            prompt
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        try:
            data = json.loads(result.stdout.strip())
            return ActivityOutput.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as e:
            return ActivityOutput(
                project_name="unknown",
                project_type=ProjectType.ENTERTAINMENT,
                details=f"Analysis failed: {str(e)}",
                confidence=0.0
            )
    
    def _build_prompt(self, context: ContextWindow) -> str:
        """Build context-aware prompt."""
        prompt = "Analyze the screenshot and describe what the user is doing.\n"
        
        if context.recent_activities:
            recent = context.recent_activities[:5]
            prompt += "\nRecent context:\n"
            for act in recent:
                prompt += f"- {act.project_name}: {act.details}\n"
        
        prompt += f"\nCurrent window: {context.current_window['title']}"
        prompt += "\n\nProvide structured output about the current activity."
        
        return prompt
    
    def _get_schema(self) -> dict:
        """Get Pydantic schema as JSON schema."""
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "user_activity",
                "schema": ActivityOutput.model_json_schema()
            }
        }