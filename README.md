[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23706057&assignment_repo_type=AssignmentRepo)

# Data Pipeline Multi-Modal Minefield

## Overview

A robust data ingestion pipeline that processes multiple data sources (PDF, CSV, HTML, Video Transcript, Legacy Code) into a unified Knowledge Base.

## Project Structure

```
.
├── raw_data/                  # Source data files (DO NOT MODIFY)
│   ├── lecture_notes.pdf      # PDF document for Gemini API extraction
│   ├── sales_records.csv       # Sales data with dirty values
│   ├── product_catalog.html    # Product catalog in HTML format
│   ├── demo_transcript.txt    # Video transcript with timestamps
│   └── legacy_pipeline.py     # Python code with docstrings
├── starter_code/              # Your implementation starts here
│   ├── schema.py              # UnifiedDocument Pydantic model
│   ├── orchestrator.py        # Main pipeline orchestrator (DONE)
│   ├── quality_check.py       # Quality gates implementation (DONE)
│   ├── process_pdf.py         # PDF processing with Gemini API (DONE)
│   ├── process_csv.py         # CSV cleaning and parsing (DONE)
│   ├── process_html.py        # HTML table extraction (DONE)
│   ├── process_transcript.py  # Transcript cleaning (DONE)
│   └── process_legacy_code.py # Code docstring extraction (DONE)
├── forensic_agent/            # Grading agent
│   └── agent_forensic.py
├── processed_knowledge_base.json  # Output (generated after run)
├── requirements.txt
├── .env                       # GEMINI_API_KEY required
└── STUDENT_GUIDE_VN.md        # Vietnamese student guide
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Running the Pipeline

```bash
python starter_code/orchestrator.py
```

## Output

- `processed_knowledge_base.json` - Final unified knowledge base
- Console output shows processing progress and summary

## Testing

```bash
python forensic_agent/agent_forensic.py
```

Expected output: `Final Forensic Score: 3/3`

## Implementation Details

### Role 1: Lead Data Architect (`schema.py`)
- UnifiedDocument Pydantic model with flexible schema for v2 migration
- Supports aliases and extra fields

### Role 2: ETL/ELT Builder (all `process_*.py`)
- **PDF**: Uses Gemini 2.0 Flash API for structured extraction
- **CSV**: Handles duplicates, dirty prices ($1200, "five dollars"), ordinal dates
- **HTML**: Parses product table, handles "N/A" prices
- **Transcript**: Removes timestamps, music/noise tokens
- **Code**: Extracts docstrings using Python AST module

### Role 3: Observability & QA (`quality_check.py`)
Quality gates implemented:
1. Content length >= 20 characters
2. Rejects toxic/error strings
3. Validates code documents with docstrings

### Role 4: DevOps (`orchestrator.py`)
- Orchestrates all processing steps
- Tracks SLA with timing
- Saves output to JSON
- Reports processing summary

## Dependencies

- `google-generativeai` (deprecated, still functional)
- `beautifulsoup4`
- `pandas`
- `python-dotenv`
- `pydantic`
