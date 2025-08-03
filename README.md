# ManualScenarioGenerator

A tool for automatically generating manual test scenarios from real user interactions with Windows desktop applications.

## What it does

- Monitors and records all user actions performed within a target application (e.g., clicks, text entry)
- Captures before and after screenshots for each user action
- Extracts data about the interacted UI elements and performed operations
- Uses AI (OpenAI API) to generate detailed, natural language descriptions for every step
- Creates structured, step-by-step test scenarios in JSON format
- Exports finished scenarios to Excel templates for documentation, sharing, or validation

## How it works

1. User performs normal tasks in the application (no manual notes required)
2. Tool automatically logs each action, takes screenshots, and gathers all necessary metadata
3. Step data is sent to the AI API, which returns descriptive scenario steps
4. A complete, human-readable manual test scenario is exported to an Excel file

## Features

- Automatic action recording via Windows system hooks
- Full before/after screenshot capture and annotation
- Automated step description with OpenAI API
- Structured scenario output in JSON and Excel
- Minimal manual effort: start the tool, use your app as usual, get a ready test scenario

## Status

- Core automation and export features are fully functional and tested
- Prototype integration with SEEXP program
- Further improvements planned: web support, enhanced screenshot marking, macro-enabled Excel output, more flexible configuration

---

**Developed and maintained by Oskar Łypka**
