# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Observer is an activity monitoring tool that continuously captures screenshots of the focused window and uses AI to describe user activities in structured format. It's designed to track project context and user behavior patterns.

## Dependencies

Required system tools:
- `swaymsg` - Wayland compositor command interface (Sway)
- `grim` - Screenshot utility for Wayland
- `jq` - JSON processor
- `yq` - YAML/JSON processor
- `quicktype` - JSON Schema generator
- `mods` - AI model interface with llama-cpp backend

## Development Commands

### Schema Management

Generate JSON schema from example YAML:
```bash
./schema_from_example.sh
```

Convert YAML schema to JSON format for mods:
```bash
./json_from_schema.sh
```

### Running Observer

Start activity monitoring:
```bash
./observer.sh
```

## Architecture

The project uses a schema-driven approach for structured AI output:

1. **Example-based Schema Definition**: `example.yaml` contains sample output structure
2. **Schema Generation**: Uses quicktype to generate JSON schema from example
3. **Constrained Generation**: The AI model uses JSON schema to ensure structured output
4. **Activity Categories**: Three main project types - system configuration, entertainment, and ML research

### Key Files

- `observer.sh` - Main monitoring loop with screenshot capture and AI analysis
- `schema.yaml` - Human-readable schema definition
- `schema.json` - JSON schema for AI model constraints
- `example.yaml` - Output format example
- Helper scripts for schema conversion and generation

The observer captures focused window screenshots every second and generates structured descriptions of user activity context.