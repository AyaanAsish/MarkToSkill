def generate_ascii_diagram():
    return """
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║                      MARKTOSKILL AGENT - WORKFLOW DIAGRAM                                ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝

┌──────────┐
│   USER   │ ◄─────────────────────────────────────────────────────┐
└────┬─────┘                                                       │
     │ Multi-format Files (PDF, DOCX, XLSX, PPTX, etc.)           │
     │ + User Prompt                                               │ skill.md
     ▼                                                             │
══════════════════════════════════════════════════════════════════▼═══════════════
                              FASTAPI SERVER (API Gateway)
═══════════════════════════════════════════════════════════════════════════════════
     │
     ▼ Stage 1: FILE UPLOAD
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌────────────────────┐                                                                   │
│ │  FILE HANDLER      │  • Receive uploaded file (multi-format)                           │
│ │  /process-document/│  • Save to tmp/input/                                             │
│ └────────┬───────────┘  • Extract user prompt/goal                                       │
└──────────┼───────────────────────────────────────────────────────────────────────────────┘
           │ File Path + Prompt
           ▼ Stage 2: DOCUMENT INGESTION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│ │  BATCH QUEUE MANAGER                                                              │   │
│ │                                                                                   │   │
│ │  ┌────────────────────────────────────────────────────────────────────────────┐   │   │
│ │  │  Receives Raw Multi-format Files                                            │   │   │
│ │  │  Tracks File Counts                                                         │   │   │
│ │  │  Unpacks .zip Archives                                                      │   │   │
│ │  │  Routes Streams (Seq / Concurrent)                                          │   │   │
│ │  └────────────────────────────────────────────────────────────────────────────┘   │   │
│ └───────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
           │ Routed Files
           ├──────────────────────────────────┐
           ▼                                  ▼
 Stage 3a: TEXT CONVERSION           Stage 3b: IMAGE EXTRACTION
┌─────────────────────────┐   ┌──────────────────────────────────┐
│ MarkItDown Converter    │   │ Image & Asset Extractor ★       │
│                         │   │                                  │
│ • Evaluate Extensions   │   │ • Extract embedded images        │
│ • Multi-format → MD     │   │ • Save to temp asset store       │
│ • Text-only pipeline    │   │ • Return metadata + asset refs   │
└────────┬────────────────┘   └────────┬─────────────────────────┘
         │                             │
         └──────────┬──────────────────┘
                    ▼ Stage 4: MARKDOWN AGGREGATION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│ │  MARKDOWN STRUCTURE AGGREGATOR                                                    │   │
│ │                                                                                   │   │
│ │  • Normalize raw extracted content                                                │   │
│ │  • Preserve headings, tables, lists                                               │   │
│ │  • Token-efficient clean markdown                                                 │   │
│ │  • Inject image reference markers                                                 │   │
│ └───────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
           │ Aggregated Markdown + Image Refs
           ▼ Stage 5: LLM PROCESSING
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│ │  LLM AGENT - Ollama (qwen3.5:9b)                                                   │   │
│ │                                                                                   │   │
│ │  ┌─────────────────────────────────────────────────────────────────────────────┐  │   │
│ │  │ CONTEXT ASSEMBLY PIPELINE                                                   │  │   │
│ │  │ • Combine aggregated markdown datasets                                      │  │   │
│ │  │ • Merge user-defined custom prompt                                          │  │   │
│ │  │ • Merge image metadata                                                      │  │   │
│ │  └─────────────────────────────────────────────────────────────────────────────┘  │   │
│ │                                                                                   │   │
│ │  ┌─────────────────────────────────────────────────────────────────────────────┐  │   │
│ │  │ SYSTEM DIRECTIVE ENGINE                                                     │  │   │
│ │  │ • Output schema guardrails                                                  │  │   │
│ │  │ • skill.md format enforcement                                               │  │   │
│ │  └─────────────────────────────────────────────────────────────────────────────┘  │   │
│ │                                                                                   │   │
│ │  ┌─────────────────────────────────────────────────────────────────────────────┐  │   │
│ │  │ LLM GATEWAY (Ollama Client)                                                 │  │   │
│ │  │ • Token window management                                                   │  │   │
│ │  │ • Streaming response                                                        │  │   │
│ │  └─────────────────────────────────────────────────────────────────────────────┘  │   │
│ │                                                                                   │   │
│ │  Output: skill.md formatted content                                               │   │
│ └───────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
           │ Raw LLM Output
           ▼ Stage 6: OUTPUT GENERATION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│ │  VALIDATION & POST-PROCESSOR                                                      │   │
│ │                                                                                   │   │
│ │  • Sanitize raw LLM output                                                        │   │
│ │  • Strip accidental code fences                                                   │   │
│ │  • Structural validity check                                                      │   │
│ └───────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│ ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│ │  FILE GENERATION MODULE                                                           │   │
│ │                                                                                   │   │
│ │  • Compile custom skill.md assets                                                 │   │
│ │  • Auto-naming and versioning                                                     │   │
│ │  • Metadata header injection                                                      │   │
│ └───────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
           │ skill.md
           ▼ Stage 7: DOWNLOAD
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌────────────────────┐                                                                   │
│ │  DOWNLOAD API      │  • Serve generated skill.md file                                 │
│ │  /download/        │  • Return to user                                                │
│ └────────────────────┘                                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════════════

SUPPORTED FORMATS:
• PDF        - Portable Document Format
• DOCX       - Microsoft Word
• XLSX       - Microsoft Excel
• PPTX       - Microsoft PowerPoint
• TXT        - Plain Text
• MD         - Markdown
• CSV        - Comma Separated Values
• JSON       - JSON Data
• HTML       - Web Pages
• ZIP        - Archives (extracted and processed)

DATA FLOW:
Files ──► MarkItDown ──► Markdown ──► LLM ──► skill.md

LEGEND:
───── Sequential Flow          ═════ Component Boundary
┌────┐ Processing Unit         ──►── Data Flow Direction
"""


def generate_mermaid_diagram():
    return """
graph LR
    classDef containerA fill:#D6E8FA,stroke:#6C8EBF,stroke-width:2px,stroke-dasharray:8 4,color:#2A4A7F
    classDef containerB fill:#B2CCCC,stroke:#4D7C7C,stroke-width:2px,stroke-dasharray:8 4,color:#2A4A4A
    classDef containerC fill:#E1D5E7,stroke:#9673A6,stroke-width:2px,stroke-dasharray:8 4,color:#5B2C6F
    classDef containerD fill:#D5E8D4,stroke:#82B366,stroke-width:2px,stroke-dasharray:8 4,color:#2A6B2A

    classDef nodeUI fill:#BCCDE8,stroke:#6C8EBF,stroke-width:2px,color:#000
    classDef nodeCore fill:#8FB3B3,stroke:#4D7C7C,stroke-width:2px,color:#FFF
    classDef nodeLLM fill:#C9A9D9,stroke:#9673A6,stroke-width:2px,color:#000
    classDef nodeOut fill:#A8D8A8,stroke:#82B366,stroke-width:2px,color:#000

    subgraph ContainerA["Container A: User Interface (UI) Layer"]
        direction TB
        UI_1["UI_1: File Ingestion Interface<br/>Drag and Drop | Multi-format<br/>.pdf .docx .xlsx .pptx .csv .json .zip"]
        UI_2["UI_2: Prompt Configuration Panel<br/>Prompt + specific instructions"]
        UI_3["UI_3: Execution and Monitor Console<br/>Progress bars, stats, etc."]
    end

    subgraph ContainerB["Container B: Ingestion and Conversion Engine (MarkItDown Core)"]
        direction TB
        Core_1["Core_1: Batch Queue Manager<br/>Receives Raw Multi-format Files<br/>Tracks File Counts | Unpacks .zip<br/>Routes Streams (Seq / Concurrent)"]
        Core_2["Core_2: MarkItDown Converter (Text)<br/>Evaluates File Extensions<br/>Multi-format to Markdown Conversion<br/>Text-Only Pipeline"]
        Core_3["Core_3: Image and Asset Extractor<br/>Extracts Embedded Images from Docs<br/>(PDF/DOCX/PPTX)<br/>Saves to Temp Asset Store"]
        Core_4["Core_4: Markdown Structure Aggregator<br/>Normalizes Raw Extracted Content<br/>Preserves Headings, Tables, Lists<br/>+ Injects Image Reference Markers"]
    end

    subgraph ContainerC["Container C: LLM Processing and Prompt Orchestration"]
        direction TB
        LLM_1["LLM_1: Context Assembly Pipeline<br/>Combines Aggregated Markdown Datasets<br/>Merges User-Defined Custom Prompt<br/>+ Receives Image Metadata"]
        LLM_2["LLM_2: System Directive Engine<br/>Output Schema Guardrails"]
        LLM_3["LLM_3: LLM Gateway / API Client<br/>Ollama qwen3.5:9b inference<br/>Token Window Management | Streaming"]
    end

    subgraph ContainerD["Container D: Output and Target Destination Layer"]
        direction TB
        Out_1["Out_1: Validation and Post-Processor<br/>Sanitizes Raw LLM Output<br/>Strips Accidental Code Fences<br/>Structural Validity Check"]
        Out_2["Out_2: File Generation Module<br/>Compiles Custom skill.md Assets<br/>Auto-Naming and Versioning<br/>Metadata Header Injection"]
        Out_3[("Out_3: Project Target Directory<br/>Local / Remote Repository<br/>Generated skill.md Files")]
    end

    UI_1  -->|"1. Raw Mixed Files / Streams"| Core_1
    UI_2  -->|"2. User Prompt and Context String"| LLM_1
    Core_1 -->|"3. Routed Files to Text"| Core_2
    Core_1 -->|"3a. Routed Files to Images"| Core_3
    Core_2 -->|"4. MarkItDown Conversion to Clean Markdown"| Core_4
    Core_3 -->|"4a. Extracted Image Metadata + Asset Refs"| Core_4
    Core_4 -->|"5. Token-Optimized Markdown + Image Markers"| LLM_1
    LLM_1 -->|"6. Combined Content String + Image Refs"| LLM_2
    LLM_2 -->|"7. Assembled Payload + System Directives"| LLM_3
    LLM_3 -->|"8. LLM Stream Response"| Out_1
    Out_1 -->|"9. Cleaned Markdown Structure"| Out_2
    Out_2 -->|"10. Writes Final skill.md Asset"| Out_3
    Out_1 -.->|"11. Live Status and Content Buffers (Feedback)"| UI_3

    class ContainerA containerA
    class ContainerB containerB
    class ContainerC containerC
    class ContainerD containerD
    class UI_1,UI_2,UI_3 nodeUI
    class Core_1,Core_2,Core_4 nodeCore
    class Core_3 nodeCore
    class LLM_1,LLM_2,LLM_3 nodeLLM
    class Out_1,Out_2 nodeOut
    class Out_3 nodeOut
"""


def generate_html_diagram():
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarkToSkill Agent - Workflow Diagram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1, h2, h3 {{ color: #333; }}
        .diagram-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .ascii-diagram {{
            background: #1e1e1e;
            color: #00ff00;
            padding: 20px;
            border-radius: 4px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            line-height: 1.3;
        }}
        .execution-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .detail-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }}
        .stage-indicator {{
            background: #28a745;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        code {{
            background: #f1f1f1;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{ background-color: #f8f9fa; }}
    </style>
</head>
<body>
    <h1> MarkToSkill Agent - Workflow Diagram</h1>

    <div class="diagram-container">
        <h2>Interactive Mermaid Diagram</h2>
        <div class="mermaid">
{generate_mermaid_diagram()}
        </div>
    </div>

    <div class="diagram-container">
        <h2>ASCII Flow Diagram</h2>
        <pre class="ascii-diagram">{generate_ascii_diagram()}</pre>
    </div>

    <div class="diagram-container">
        <h2>Processing Stages</h2>
        <div class="execution-details">
            <div class="detail-card">
                <h3> Stage 1: File Upload</h3>
                <span class="stage-indicator">INPUT</span>
                <ul>
                    <li><b>Endpoint:</b> POST /process-document/</li>
                    <li><b>Input:</b> Multi-format file + text prompt</li>
                    <li><b>Storage:</b> tmp/input/</li>
                </ul>
            </div>

            <div class="detail-card">
                <h3> Stage 2: Document Ingestion</h3>
                <span class="stage-indicator">QUEUE</span>
                <ul>
                    <li><b>Process:</b> Batch queue management</li>
                    <li><b>Features:</b> ZIP unpack, file routing</li>
                    <li><b>Modes:</b> Sequential / Concurrent</li>
                </ul>
            </div>

            <div class="detail-card">
                <h3> Stage 3a: MarkItDown Conversion</h3>
                <span class="stage-indicator">CONVERT</span>
                <ul>
                    <li><b>Library:</b> MarkItDown</li>
                    <li><b>Input:</b> PDF, DOCX, XLSX, PPTX, etc.</li>
                    <li><b>Output:</b> Clean markdown text</li>
                </ul>
            </div>

            <div class="detail-card">
                <h3> Stage 3b: Image Extraction ★</h3>
                <span class="stage-indicator">EXTRACT</span>
                <ul>
                    <li><b>Sources:</b> PDF, DOCX, PPTX</li>
                    <li><b>Storage:</b> Temp asset store</li>
                    <li><b>Output:</b> Image metadata + refs</li>
                </ul>
            </div>

            <div class="detail-card">
                <h3> Stage 4: Markdown Aggregation</h3>
                <span class="stage-indicator">NORMALIZE</span>
                <ul>
                    <li><b>Process:</b> Content normalization</li>
                    <li><b>Preserves:</b> Headings, tables, lists</li>
                    <li><b>Output:</b> Token-efficient clean MD</li>
                </ul>
            </div>

            <div class="detail-card">
                <h3> Stage 5: LLM Processing</h3>
                <span class="stage-indicator">AI</span>
                <ul>
                    <li><b>Model:</b> Ollama qwen3.5:9b</li>
                    <li><b>Role:</b> Skill document generator</li>
                    <li><b>Context:</b> Markdown + prompt + images</li>
                </ul>
            </div>

            <div class="detail-card">
                <h3> Stage 6: Output Generation</h3>
                <span class="stage-indicator">BUILD</span>
                <ul>
                    <li><b>Validation:</b> Sanitize LLM output</li>
                    <li><b>Generation:</b> Compile skill.md</li>
                    <li><b>Output:</b> Ready-to-use skill document</li>
                </ul>
            </div>

            <div class="detail-card">
                <h3> Stage 7: Download</h3>
                <span class="stage-indicator">OUTPUT</span>
                <ul>
                    <li><b>Endpoint:</b> GET /download/{{filename}}</li>
                    <li><b>Format:</b> text/markdown</li>
                    <li><b>Location:</b> tmp/output/</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="diagram-container">
        <h2>Supported Input Formats</h2>
        <table>
            <thead>
                <tr>
                    <th>Format</th>
                    <th>Extension</th>
                    <th>Conversion Method</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>PDF</strong></td><td>.pdf</td><td>MarkItDown</td></tr>
                <tr><td><strong>Word</strong></td><td>.docx</td><td>MarkItDown</td></tr>
                <tr><td><strong>Excel</strong></td><td>.xlsx</td><td>MarkItDown</td></tr>
                <tr><td><strong>PowerPoint</strong></td><td>.pptx</td><td>MarkItDown</td></tr>
                <tr><td><strong>Plain Text</strong></td><td>.txt</td><td>Direct read</td></tr>
                <tr><td><strong>Markdown</strong></td><td>.md</td><td>Direct read</td></tr>
                <tr><td><strong>CSV</strong></td><td>.csv</td><td>CSV parser</td></tr>
                <tr><td><strong>JSON</strong></td><td>.json</td><td>JSON parser</td></tr>
                <tr><td><strong>ZIP Archive</strong></td><td>.zip</td><td>Extract and process</td></tr>
            </tbody>
        </table>
    </div>

    <div class="diagram-container">
        <h2>API Endpoints</h2>
        <table>
            <thead>
                <tr>
                    <th>Endpoint</th>
                    <th>Method</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>/process-document/</code></td><td>POST</td><td>Process document with AI skill generation</td></tr>
                <tr><td><code>/download/{{filename}}</code></td><td>GET</td><td>Download generated skill.md file</td></tr>
                <tr><td><code>/metrics</code></td><td>GET</td><td>Prometheus-compatible metrics</td></tr>
                <tr><td><code>/workflow-diagram</code></td><td>GET</td><td>Interactive workflow diagram</td></tr>
                <tr><td><code>/health</code></td><td>GET</td><td>Health check endpoint</td></tr>
                <tr><td><code>/status</code></td><td>GET</td><td>Detailed status check</td></tr>
                <tr><td><code>/config</code></td><td>GET</td><td>System configuration</td></tr>
                <tr><td><code>/ollama/status</code></td><td>GET</td><td>Ollama connection status</td></tr>
            </tbody>
        </table>
    </div>

    <div class="diagram-container">
        <h2>Data Flow Summary</h2>
        <p style="font-size: 18px; text-align: center; font-family: monospace;">
            Files ──► MarkItDown ──► Markdown ──► LLM ──► skill.md
        </p>
    </div>
</body>
</html>"""
    return html_content


if __name__ == "__main__":
    with open("workflow_diagram.txt", "w", encoding="utf-8") as f:
        f.write(generate_ascii_diagram())

    with open("workflow_diagram.mmd", "w", encoding="utf-8") as f:
        f.write(generate_mermaid_diagram())

    with open("workflow_diagram.html", "w", encoding="utf-8") as f:
        f.write(generate_html_diagram())

    print("Workflow diagrams generated:")
    print("  - workflow_diagram.txt (ASCII)")
    print("  - workflow_diagram.mmd (Mermaid)")
    print("  - workflow_diagram.html (Interactive HTML)")
