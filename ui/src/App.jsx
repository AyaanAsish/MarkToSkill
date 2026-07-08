import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const UploadIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-8 h-8">
    <path fillRule="evenodd" d="M11.47 2.47a.75.75 0 011.06 0l4.5 4.5a.75.75 0 01-1.06 1.06l-3.22-3.22V16.5a.75.75 0 01-1.5 0V4.81L8.03 8.03a.75.75 0 01-1.06-1.06l4.5-4.5zM3 15.75a.75.75 0 01.75.75v2.25a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5V16.5a.75.75 0 011.5 0v2.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V16.5a.75.75 0 01.75-.75z" clipRule="evenodd" />
  </svg>
);

const SparklesIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path fillRule="evenodd" d="M9 4.5a.75.75 0 01.721.544l.813 2.846a3.75 3.75 0 002.576 2.576l2.846.813a.75.75 0 010 1.442l-2.846.813a3.75 3.75 0 00-2.576 2.576l-.813 2.846a.75.75 0 01-1.442 0l-.813-2.846a3.75 3.75 0 00-2.576-2.576l-2.846-.813a.75.75 0 010-1.442l2.846-.813A3.75 3.75 0 007.466 7.89l.813-2.846A.75.75 0 019 4.5zM18 1.5a.75.75 0 01.728.568l.258 1.036c.236.94.97 1.674 1.91 1.91l1.036.258a.75.75 0 010 1.456l-1.036.258c-.94.236-1.674.97-1.91 1.91l-.258 1.036a.75.75 0 01-1.456 0l-.258-1.036a2.625 2.625 0 00-1.91-1.91l-1.036-.258a.75.75 0 010-1.456l1.036-.258a2.625 2.625 0 001.91-1.91l.258-1.036A.75.75 0 0118 1.5zM16.5 15a.75.75 0 01.712.513l.394 1.183c.15.447.5.799.948.948l1.183.395a.75.75 0 010 1.422l-1.183.395c-.447.15-.799.5-.948.948l-.395 1.183a.75.75 0 01-1.422 0l-.395-1.183a1.5 1.5 0 00-.948-.948l-1.183-.395a.75.75 0 010-1.422l1.183-.395c.447-.15.799-.5.948-.948l.395-1.183A.75.75 0 0116.5 15z" clipRule="evenodd" />
  </svg>
);

const DownloadIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path fillRule="evenodd" d="M12 2.25a.75.75 0 01.75.75v11.69l3.22-3.22a.75.75 0 111.06 1.06l-4.5 4.5a.75.75 0 01-1.06 0l-4.5-4.5a.75.75 0 111.06-1.06l3.22 3.22V3a.75.75 0 01.75-.75zm-9 13.5a.75.75 0 01.75.75v2.25a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5V16.5a.75.75 0 011.5 0v2.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V16.5a.75.75 0 01.75-.75z" clipRule="evenodd" />
  </svg>
);

const DocumentIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0016.5 9h-1.875a1.875 1.875 0 01-1.875-1.875V5.25A3.75 3.75 0 009 1.5H5.625z" />
    <path d="M12.971 1.816A5.23 5.23 0 0114.25 5.25v1.875c0 .207.168.375.375.375h1.875a5.23 5.23 0 013.434 1.279 9.768 9.768 0 00-6.963-6.963z" />
  </svg>
);

const CloseIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
    <path fillRule="evenodd" d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z" clipRule="evenodd" />
  </svg>
);

export default function App() {
  const [files, setFiles] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [outputContent, setOutputContent] = useState(null);
  const [outputFilename, setOutputFilename] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [processingStep, setProcessingStep] = useState("");
  const [errorDetails, setErrorDetails] = useState("");

  const handleFileSelect = (e) => {
    if (e.target.files?.length) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files?.length) {
      setFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const removeFile = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const getAcceptedExtensions = () => {
    return ".pdf,.docx,.xlsx,.pptx,.txt,.md,.csv,.json,.html,.zip";
  };

  const formatSize = (bytes) => {
    const mb = bytes / 1024 / 1024;
    return mb >= 1 ? `${mb.toFixed(2)} MB` : `${(bytes / 1024).toFixed(1)} KB`;
  };

  const processDocument = async () => {
    if (!files.length) return alert("Please select at least one file");
    if (!prompt.trim()) return alert("Please enter instructions for the skill generation");

    setErrorDetails("");

    const formData = new FormData();
    files.forEach((f) => formData.append("files", f));
    formData.append("prompt", prompt);

    setLoading(true);
    setProcessingStep("Uploading documents...");

    try {
      setProcessingStep("Checking API connection...");
      const healthResp = await fetch(`${API_URL}/health`, { method: "GET" });
      if (!healthResp.ok) {
        throw new Error(`API is not responding (HTTP ${healthResp.status})`);
      }
      const healthData = await healthResp.json();
      if (healthData.status !== "healthy") {
        throw new Error("API reports unhealthy status");
      }

      setProcessingStep("Converting documents to markdown...");

      const resp = await fetch(`${API_URL}/process-document/`, {
        method: "POST",
        body: formData,
      });

      const data = await resp.json();

      if (!resp.ok) {
        throw new Error(data.detail || data.error || `Server error (HTTP ${resp.status})`);
      }

      setProcessingStep("Generating skill document...");
      const filename = data.filename;

      const contentResp = await fetch(`${API_URL}/download/${filename}`);
      if (!contentResp.ok) {
        throw new Error("Failed to download generated skill file");
      }
      const text = await contentResp.text();

      setOutputContent(text);
      setOutputFilename(filename);
      setProcessingStep("");
    } catch (err) {
      const msg = err.message || "Unknown error";
      alert("Processing failed: " + msg);
      setErrorDetails(msg);
    } finally {
      setLoading(false);
      setProcessingStep("");
    }
  };

  const downloadSkill = () => {
    if (!outputContent) return;
    const blob = new Blob([outputContent], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = outputFilename || "skill.md";
    a.click();
    URL.revokeObjectURL(url);
  };

  const clearAll = () => {
    setFiles([]);
    setPrompt("");
    setOutputContent(null);
    setOutputFilename(null);
    setErrorDetails("");
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="fixed inset-0 bg-gradient-to-br from-blue-950/20 via-slate-950 to-indigo-950/20 pointer-events-none" />

      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-6xl">
        <header className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/10 rounded-full border border-blue-500/20 mb-6">
            <SparklesIcon />
            <span className="text-sm text-blue-300">AI-Powered Document-to-Skill Conversion</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-white via-blue-200 to-indigo-200 bg-clip-text text-transparent">
            MarkToSkill Agent
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Upload documents in any format, describe the skill you want to create, and let AI generate a structured, ready-to-use skill document.
          </p>
        </header>

        <div className="max-w-3xl mx-auto space-y-6">
          {/* Upload Area */}
          <div
            onDrop={handleDrop}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            className={`relative bg-slate-900/50 backdrop-blur-sm rounded-2xl p-8 border-2 border-dashed transition-all duration-200 ${
              dragActive
                ? "border-blue-500 bg-blue-500/10"
                : files.length
                ? "border-green-500/50 bg-green-500/5"
                : "border-slate-700 hover:border-slate-600"
            }`}
          >
            <input
              type="file"
              multiple
              accept={getAcceptedExtensions()}
              onChange={handleFileSelect}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />

            <div className="text-center">
              <div className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-4 ${
                files.length ? "bg-green-500/20 text-green-400" : "bg-slate-800 text-slate-400"
              }`}>
                <UploadIcon />
              </div>

              {files.length > 0 ? (
                <div className="space-y-2">
                  <p className="text-sm font-medium text-green-400 mb-3">
                    {files.length} file{files.length > 1 ? "s" : ""} selected
                  </p>
                  <div className="max-h-40 overflow-y-auto space-y-1.5">
                    {files.map((f, i) => (
                      <div key={i} className="flex items-center justify-between bg-slate-800/50 rounded-lg px-3 py-2 group">
                        <div className="flex items-center gap-2 min-w-0">
                          <DocumentIcon />
                          <span className="text-sm text-slate-200 truncate">{f.name}</span>
                          <span className="text-xs text-slate-500 shrink-0">{formatSize(f.size)}</span>
                        </div>
                        <button
                          onClick={(e) => { e.stopPropagation(); removeFile(i); }}
                          className="text-slate-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-all shrink-0 ml-2"
                        >
                          <CloseIcon />
                        </button>
                      </div>
                    ))}
                  </div>
                  <p className="text-xs text-slate-500 mt-2">Click or drop more files to add</p>
                </div>
              ) : (
                <div>
                  <p className="text-lg font-medium text-slate-300 mb-1">
                    Drop your documents here
                  </p>
                  <p className="text-sm text-slate-500">
                    or click to browse • Select multiple files at once
                  </p>
                  <p className="text-xs text-slate-600 mt-2">
                    PDF, DOCX, XLSX, PPTX, TXT, MD, CSV, JSON, ZIP
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Prompt Input */}
          <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50">
            <label className="block text-sm font-medium text-slate-400 mb-3">
              Describe the skill you want to create
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g., Create a beginner-friendly skill document that teaches the basics of Python programming with examples..."
              rows={3}
              className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all resize-none"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={processDocument}
              disabled={loading || !files.length || !prompt.trim()}
              className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white font-semibold py-4 px-6 rounded-xl shadow-lg shadow-blue-500/25 transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>{processingStep || "Processing..."}</span>
                </>
              ) : (
                <>
                  <SparklesIcon />
                  <span>Generate Skill Document</span>
                </>
              )}
            </button>

            {(files.length || outputContent) && (
              <button
                onClick={clearAll}
                className="px-6 py-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium rounded-xl transition-all"
              >
                Clear
              </button>
            )}
          </div>

          {/* Error Details */}
          {errorDetails && !loading && (
            <div className="bg-red-900/30 border border-red-800/50 rounded-2xl p-4">
              <p className="text-sm text-red-300 font-medium mb-1">Error details:</p>
              <p className="text-xs text-red-400 font-mono">{errorDetails}</p>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50">
              <div className="flex items-center gap-4">
                <div className="relative w-12 h-12">
                  <div className="absolute inset-0 rounded-full border-4 border-slate-700" />
                  <div className="absolute inset-0 rounded-full border-4 border-blue-500 border-t-transparent animate-spin" />
                </div>
                <div>
                  <p className="font-medium text-white">{processingStep}</p>
                  <p className="text-sm text-slate-400">This may take a moment...</p>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-4 gap-2">
                {["Check", "Convert", "Analyze", "Generate"].map((step, i) => (
                  <div key={step} className="text-center">
                    <div className={`h-1 rounded-full mb-2 ${
                      i <= ["Checking", "Converting", "Analyzing", "Generating"].findIndex(s => processingStep.includes(s))
                        ? "bg-blue-500"
                        : "bg-slate-700"
                    }`} />
                    <span className="text-xs text-slate-500">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Output Section */}
          {outputContent && !loading && (
            <div className="space-y-4">
              <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50">
                <div className="flex items-center gap-2 mb-4">
                  <DocumentIcon />
                  <span className="text-sm font-medium text-slate-300">Generated Skill Document</span>
                </div>

                <div className="bg-slate-950 rounded-xl p-4 max-h-96 overflow-y-auto border border-slate-800">
                  <pre className="text-sm text-slate-300 whitespace-pre-wrap font-mono leading-relaxed">
                    {outputContent.length > 3000
                      ? outputContent.slice(0, 3000) + "\n\n... (truncated)"
                      : outputContent}
                  </pre>
                </div>
              </div>

              <div className="flex gap-4">
                <button
                  onClick={downloadSkill}
                  className="flex-1 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-medium py-3 px-6 rounded-xl shadow-lg shadow-emerald-500/25 transition-all flex items-center justify-center gap-2"
                >
                  <DownloadIcon />
                  <span>Download skill.md</span>
                </button>
              </div>
            </div>
          )}
        </div>

        <footer className="mt-16 text-center text-slate-500 text-sm">
          <p>Powered by AI • Ollama qwen3.5:9b</p>
        </footer>
      </div>
    </div>
  );
}
