# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Observer is an AI-powered activity monitoring tool that continuously captures screenshots of the focused window, uses AI to describe user activities in structured format, and stores the data with context for analysis. It's designed to track project context and user behavior patterns over time.

## Dependencies

**System Dependencies:**
- `swaymsg` - Wayland compositor command interface (Sway)
- `grim` - Screenshot utility for Wayland
- `mods` - AI model interface with llama-cpp backend
- `uv` - Python package manager

**Python Dependencies** (managed by uv):
- `pydantic>=2.0` - Type-safe data validation and schemas
- `sqlalchemy>=2.0` - Database ORM
- `python-i3ipc>=2.2` - Native Sway/i3 window manager interface
- `pillow>=10.0` - Image processing
- `rich>=13.0` - Rich terminal output
- `typer>=0.9` - CLI framework

## Development Commands

### Installation

```bash
# Create virtual environment and install dependencies
uv venv
uv pip install -e .
```

### Running Observer

```bash
# Start activity monitoring (default 1-second interval)
uv run observer run

# Run with custom interval
uv run observer run --interval 2

# View activity history
uv run observer history --minutes 30
```

### Development

```bash
# Run linter
uv run ruff check

# Run type checker
uv run mypy src/

# Run tests
uv run pytest
```

## Architecture

The project uses a modular Python architecture with persistent storage and context awareness:

### Core Components

- **`src/observer/main.py`** - CLI interface and main observation loop
- **`src/observer/models.py`** - Pydantic schemas for type-safe data handling
- **`src/observer/database.py`** - SQLAlchemy models and database operations
- **`src/observer/capture.py`** - Screenshot capture using i3ipc and grim
- **`src/observer/ai.py`** - Context-aware AI analysis using mods

### Data Flow

1. **Capture**: Screenshot focused window and extract window metadata
2. **Context**: Retrieve recent activities from database for AI context
3. **Analyze**: Send screenshot + context to AI model with Pydantic schema
4. **Store**: Save structured output and screenshot to SQLite database
5. **Display**: Show activity summary in terminal

### Storage Structure

- **`data/observer.db`** - SQLite database with activity records
- **`data/screenshots/`** - Compressed PNG screenshots with timestamps
- **Activity Categories**: system_configuration, entertainment_and_procrastination, machine_learning_research

### Schema-Driven Output

The AI model receives a JSON schema generated from Pydantic models (`ActivityOutput`) ensuring structured, type-safe responses with fields:
- `project_name` - Current project identifier
- `project_type` - Category enum
- `details` - Activity description  
- `confidence` - Analysis confidence score

Context awareness provides recent activity history to the AI model for better continuity and project tracking.