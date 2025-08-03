# ManualScenarioGenerator (Proof of Concept)

A proof-of-concept tool for automatically generating manual test scenarios from real user interactions with Windows desktop applications.

## What it does

- Monitors and records user actions in a target application (clicks, text entry, etc.)
- Captures before and after screenshots for each action
- Extracts data about interacted UI elements and performed operations
- Uses AI (OpenAI API) to generate detailed, natural language step descriptions
- Creates structured test scenarios (JSON + Excel export)

## How it works

1. Start the tool and work with the application as usual.
2. The tool logs every action, captures relevant screenshots, and collects metadata.
3. Action data is sent to the AI API, which returns descriptive steps.
4. A complete, human-readable manual test scenario is exported to an Excel file.

## Features

- Fully automatic action recording (system hooks for Windows)
- Automated screenshot capture and annotation
- Step description generation via OpenAI API
- Scenario export to JSON and Excel formats
- Minimal user involvement required

## Status

- **Proof of Concept:** Core automation and export are functional and demonstrated with SEEXP program.
- Not production-ready; further improvements and refactoring needed for general use.
- Future plans: web app support, improved screenshot features, macro-enabled Excel output, and more configuration options.

---
