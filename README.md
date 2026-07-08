# MarkToSkill Agent

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-powered document-to-skill conversion agent** that transforms multi-format documents (PDF, DOCX, XLSX, PPTX, and more) into structured, ready-to-use skill.md files using local LLM inference.

<p align="center">
  <img src="docs/workflow-preview.png" alt="MarkToSkill Agent Workflow" width="600">
</p>

---

## Overview

MarkToSkill Agent converts source documents into comprehensive skill documents through a multi-stage pipeline:

```
Files → MarkItDown → Markdown → LLM → skill.md
```

### Supported Input Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| **PDF** | `.pdf` | Portable Document Format |
| **Word** | `.docx` | Microsoft Word |
| **Excel** | `.xlsx` | Microsoft Excel |
| **PowerPoint** | `.pptx` | Microsoft PowerPoint |
| **Plain Text** | `.txt` | Plain text files |
| **Markdown** | `.md` | Markdown files |
| **CSV** | `.csv` | Comma Separated Values |
| **JSON** | `.json` | JSON Data |
| **HTML** | `.html` | Web pages |
| **ZIP** | `.zip` | Archives (extracted and processed) |

---

## Architecture

```
+-------------------------------------------------------------------------+
|                         MARKTOSKILL AGENT                               |
+-------------------------------------------------------------------------+
|                                                                         |
|  +-----------+      +--------------------------------------------+      |
|  |   User    |      |            FastAPI Backend                 |      |
|  | Interface |<---->|  +------------+ +---------+ +------------+ |      |
|  |  (React)  |      |  |MarkItDown  |>|   LLM   |>|  Output    | |      |
|  +-----------+      |  | Converter  | | (Ollama)| | Generator  | |      |
|    Port 3000        |  +------------+ +---------+ +------------+ |      |
|                     +--------------------------------------------+      |
|                                   Port 8000                             |
|                                                                         |
|  +-------------------------------------------------------------------+  |
|  |                       External Services                           |  |
|  |  +---------------+  +------------------------------------------+ |  |
|  |  | Ollama Server |  |  Document Processors (PyMuPDF, docx,     | |  |
|  |  | (Port 11434)  |  |  python-pptx, openpyxl, MarkItDown)     | |  |
|  |  +---------------+  +------------------------------------------+ |  |
|  +-------------------------------------------------------------------+  |
|                                                                         |
+-------------------------------------------------------------------------+
```

### Project Structure

```
MarkToSkill-agent/
├── src/                          # FastAPI backend application
│   ├── agents/
│   │   └── agent.py              # Main orchestration agent
│   ├── clients/
│   │   └── llm.py                # Ollama LLM client
│   ├── core/
│   │   └── config.py             # Configuration management
│   ├── utils/
│   │   ├── diagram_generator.py  # Workflow diagram generation
│   │   ├── document_converter.py # MarkItDown integration
│   │   ├── image_extractor.py    # Image extraction from docs
│   │   ├── markdown_aggregator.py# Content normalization
│   │   ├── metrics.py            # Prometheus metrics
│   │   └── output_generator.py   # skill.md file generation
│   └── main.py                   # FastAPI application
├── ui/                           # React frontend application
│   ├── src/
│   │   └── App.jsx               # Main UI component
│   ├── Dockerfile
│   └── nginx.conf
├── scripts/                      # Setup and utility scripts
│   └── setup-personal.sh.template
├── docker-compose.yml            # Container orchestration
├── Dockerfile                    # Backend container image
├── Makefile                      # Build automation
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── README.md
```

---

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Ollama](https://ollama.ai/) (for LLM inference)
- Pull the Qwen model: `ollama pull qwen3.5:9b`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MarkToSkill.git
   cd MarkToSkill/MarkToSkill-agent
   ```

2. **Run initial setup**
   ```bash
   make setup
   ```

3. **Start Ollama and pull the model**
   ```bash
   ollama serve                    # Start Ollama server
   ollama pull qwen3.5:9b          # Pull the default model
   ```

4. **Verify Ollama is accessible**
   ```bash
   make check-ollama
   ```

5. **Build and start services**
   ```bash
   make start
   ```

6. **Access the application**
   - **UI**: http://localhost:3000
   - **API Docs**: http://localhost:8000/docs
   - **Metrics**: http://localhost:8000/metrics
   - **Workflow Diagram**: http://localhost:8000/workflow-diagram

### Makefile Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make info` | Display project information and endpoints |
| `make setup` | Initial setup (create .env from template) |
| `make setup-full` | Interactive setup wizard |
| `make check-ollama` | Verify Ollama server status |
| `make start` | Build and start all services |
| `make stop` | Stop all services |
| `make restart` | Restart all services |
| `make logs` | View service logs |
| `make status` | Show detailed service status |
| `make health` | Check health of all services |
| `make clean` | Remove containers and volumes |
| `make clean-all` | Remove everything including images |

---

## Configuration

### Environment Variables

Configuration is managed through environment variables. Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://host.docker.internal:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `qwen3.5:9b` | LLM model for skill generation |
| `OLLAMA_API_KEY` | *(empty)* | Optional API key for Ollama Cloud |
| `API_PORT` | `8000` | Backend API port |
| `UI_PORT` | `3000` | Frontend UI port |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/process-document/` | Process document with AI skill generation |
| `GET` | `/download/{filename}` | Download generated skill.md file |
| `GET` | `/health` | Basic health check |
| `GET` | `/status` | Detailed status with Ollama connection |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/workflow-diagram` | Interactive workflow visualization |
| `GET` | `/config` | Current configuration |
| `GET` | `/ollama/status` | Ollama connection status |
| `GET` | `/docs` | Swagger API documentation |
| `GET` | `/redoc` | ReDoc API documentation |

### Process Document

**Request:**
```bash
curl -X POST "http://localhost:8000/process-document/" \
  -F "file=@document.pdf" \
  -F "prompt=Create a beginner-friendly skill document about Python programming"
```

**Response:**
```json
{
  "filename": "skill.md"
}
```

### Download Result

```bash
curl -O "http://localhost:8000/download/skill.md"
```

---

## Development

### Local Development (without Docker)

1. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start the backend**
   ```bash
   make dev
   ```

3. **Start the frontend**
   ```bash
   cd ui
   npm install
   npm run dev
   ```

---

## Monitoring

### Prometheus Metrics

The `/metrics` endpoint exposes comprehensive metrics in Prometheus format:

- **Workflow Metrics**: Execution counts, durations, active workflows
- **Document Processing**: Files processed, sizes, formats
- **Conversion**: MarkItDown conversion timings
- **LLM Requests**: Request counts, latencies, response sizes
- **Errors**: Error counts by stage and type

---

## Tech Stack

### Backend
- **Python 3.11** - Core runtime
- **FastAPI** - High-performance API framework
- **Uvicorn** - ASGI server
- **MarkItDown** - Multi-format to Markdown conversion
- **PyMuPDF** - PDF processing
- **python-docx** - Word document processing
- **python-pptx** - PowerPoint processing
- **openpyxl** - Excel processing
- **Ollama** - Local LLM inference (qwen3.5:9b)
- **Prometheus Client** - Metrics collection

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Nginx** - Static file serving

### Infrastructure
- **Docker Compose** - Container orchestration

---

<p align="center">
  Made with ♡ by Ayaan<br>
  <sub>AI-assisted document processing since 2025</sub>
</p>
