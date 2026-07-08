from typing import List
from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse, HTMLResponse, Response
import os
import time
import uuid

from src.agents.agent import run_agent
from src.utils.metrics import metrics_collector, get_metrics_output
from src.utils.diagram_generator import generate_html_diagram
from src.utils.document_converter import get_supported_extensions
from src.core.config import (
    OLLAMA_HOST,
    OLLAMA_MODEL,
    API_PORT,
    UI_PORT,
    LOG_LEVEL,
    get_config_summary,
    validate_config,
    TMP_INPUT_PATH,
    TMP_OUTPUT_PATH,
)
from src.clients.llm import check_ollama_connection

app = FastAPI(
    title="MarkToSkill Agent API",
    description="Document-to-skill conversion agent. Converts multi-format documents into structured skill.md files using LLM.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(TMP_INPUT_PATH, exist_ok=True)
os.makedirs(TMP_OUTPUT_PATH, exist_ok=True)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "MarkToSkill Agent",
        "version": "1.0.0"
    }


@app.get("/status")
async def status_check():
    ollama_status = check_ollama_connection()
    config_valid = validate_config()

    return {
        "status": "healthy" if ollama_status["connected"] else "degraded",
        "app": "MarkToSkill Agent",
        "version": "1.0.0",
        "ollama": ollama_status,
        "config_valid": config_valid,
    }


@app.post("/process-document/")
async def process_document(
    request: Request,
    files: List[UploadFile] = File(...),
    prompt: str = Form(""),
):
    start_time = time.time()
    status_code = 200

    try:
        input_paths = []
        for file in files:
            file_ext = os.path.splitext(file.filename)[1].lower() if file.filename else ".bin"
            unique_name = f"{uuid.uuid4().hex}{file_ext}"
            input_path = os.path.join(TMP_INPUT_PATH, unique_name)

            file_content = await file.read()
            file_size = len(file_content)

            with open(input_path, "wb") as f:
                f.write(file_content)

            metrics_collector.record_document(file_ext, file_size, "success")
            input_paths.append(input_path)

        output_path = run_agent(input_paths, prompt)

        if os.path.exists(output_path):
            output_size = os.path.getsize(output_path)
            metrics_collector.record_output_file("md", output_size, "success")

        return {"filename": os.path.basename(output_path)}

    except Exception as e:
        status_code = 500
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    finally:
        duration = time.time() - start_time
        metrics_collector.record_api_request("/process-document/", "POST", status_code, duration)


@app.get("/download/{filename}")
async def download_file(request: Request, filename: str):
    start_time = time.time()
    status_code = 200

    try:
        path = os.path.join(TMP_OUTPUT_PATH, filename)
        if os.path.exists(path):
            return FileResponse(
                path,
                media_type="text/markdown",
                filename=filename
            )
        status_code = 404
        return {"error": "File not found"}

    finally:
        duration = time.time() - start_time
        metrics_collector.record_api_request("/download/", "GET", status_code, duration)


@app.get("/metrics", response_class=PlainTextResponse)
async def get_metrics() -> Response:
    try:
        metrics_output = get_metrics_output()
        return Response(
            content=metrics_output,
            media_type="text/plain; version=0.0.4; charset=utf-8"
        )
    except Exception as e:
        return Response(
            content=f"# Error generating metrics: {str(e)}",
            media_type="text/plain",
            status_code=500
        )


@app.get("/workflow-diagram", response_class=HTMLResponse)
async def get_workflow_diagram() -> HTMLResponse:
    try:
        html_content = generate_html_diagram()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(
            content=f"<html><body><h1>Error generating diagram</h1><p>{str(e)}</p></body></html>",
            status_code=500
        )


@app.get("/config")
async def get_configuration():
    return {
        "app_name": "MarkToSkill Agent",
        "version": "1.0.0",
        "config": get_config_summary(),
        "endpoints": {
            "process_document": "/process-document/",
            "download": "/download/{filename}",
            "metrics": "/metrics",
            "workflow_diagram": "/workflow-diagram",
            "health": "/health",
            "status": "/status",
            "docs": "/docs"
        },
        "supported_formats": get_supported_extensions(),
    }


@app.get("/ollama/status")
async def get_ollama_status():
    return check_ollama_connection()
