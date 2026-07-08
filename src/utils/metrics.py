from typing import Dict, Any
import time
from functools import wraps
from contextlib import contextmanager

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    Summary,
    Info,
    generate_latest,
    CollectorRegistry,
)

REGISTRY = CollectorRegistry()

system_info = Info(
    'marktoskill_info',
    'MarkToSkill Agent system information',
    registry=REGISTRY
)

workflow_total = Counter(
    'marktoskill_workflow_total',
    'Total number of workflow executions',
    ['status'],
    registry=REGISTRY
)

workflow_duration = Histogram(
    'marktoskill_workflow_duration_seconds',
    'Duration of complete workflow execution',
    buckets=(0.5, 1, 2, 5, 10, 30, 60, 120, 300),
    registry=REGISTRY
)

workflow_active = Gauge(
    'marktoskill_workflow_active',
    'Number of currently active workflows',
    registry=REGISTRY
)

api_requests_total = Counter(
    'marktoskill_api_requests_total',
    'Total number of API requests',
    ['endpoint', 'method', 'status_code'],
    registry=REGISTRY
)

api_request_duration = Histogram(
    'marktoskill_api_request_duration_seconds',
    'Duration of API request processing',
    ['endpoint', 'method'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1, 2.5, 5, 10, 30),
    registry=REGISTRY
)

documents_processed = Counter(
    'marktoskill_documents_processed_total',
    'Total number of documents processed',
    ['format', 'status'],
    registry=REGISTRY
)

document_size = Summary(
    'marktoskill_document_size_bytes',
    'Size of processed documents in bytes',
    registry=REGISTRY
)

conversion_duration = Histogram(
    'marktoskill_conversion_duration_seconds',
    'Duration of document to markdown conversion',
    buckets=(0.1, 0.5, 1, 2, 5, 10, 30, 60),
    registry=REGISTRY
)

images_extracted = Summary(
    'marktoskill_images_extracted',
    'Number of images extracted from documents',
    registry=REGISTRY
)

llm_requests_total = Counter(
    'marktoskill_llm_requests_total',
    'Total number of LLM requests',
    ['model', 'status'],
    registry=REGISTRY
)

llm_request_duration = Histogram(
    'marktoskill_llm_request_duration_seconds',
    'Duration of LLM requests',
    ['model'],
    buckets=(0.5, 1, 2, 5, 10, 30, 60, 120),
    registry=REGISTRY
)

llm_response_length = Summary(
    'marktoskill_llm_response_length_chars',
    'Length of LLM responses in characters',
    registry=REGISTRY
)

output_generation_total = Counter(
    'marktoskill_output_generation_total',
    'Total number of output file generations',
    ['format', 'status'],
    registry=REGISTRY
)

output_file_size = Summary(
    'marktoskill_output_file_size_bytes',
    'Size of generated output files in bytes',
    registry=REGISTRY
)

errors_total = Counter(
    'marktoskill_errors_total',
    'Total number of errors',
    ['stage', 'error_type'],
    registry=REGISTRY
)

memory_usage = Gauge(
    'marktoskill_memory_usage_bytes',
    'Current memory usage in bytes',
    registry=REGISTRY
)


class MetricsCollector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.start_time = time.time()

        system_info.info({
            'version': '1.0.0',
            'environment': 'production',
            'app_name': 'MarkToSkill Agent'
        })

    @contextmanager
    def track_duration(self, histogram: Histogram, labels: Dict[str, str] = None):
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            if labels:
                histogram.labels(**labels).observe(duration)
            else:
                histogram.observe(duration)

    def track_workflow(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                workflow_active.inc()
                status = "success"

                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    status = "error"
                    errors_total.labels(stage="workflow", error_type=type(e).__name__).inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    workflow_active.dec()
                    workflow_total.labels(status=status).inc()
                    workflow_duration.observe(duration)

            return wrapper
        return decorator

    def record_document(self, format: str, file_size: int, status: str = "success"):
        documents_processed.labels(format=format, status=status).inc()
        document_size.observe(file_size)

    def record_images_extracted(self, count: int):
        images_extracted.observe(count)

    def record_output_file(self, format: str, file_size: int, status: str = "success"):
        output_generation_total.labels(format=format, status=status).inc()
        output_file_size.observe(file_size)

    def record_api_request(self, endpoint: str, method: str, status_code: int, duration: float):
        api_requests_total.labels(
            endpoint=endpoint,
            method=method,
            status_code=str(status_code)
        ).inc()
        api_request_duration.labels(
            endpoint=endpoint,
            method=method
        ).observe(duration)

    def update_resource_metrics(self):
        try:
            import psutil
            process = psutil.Process()
            memory_usage.set(process.memory_info().rss)
        except ImportError:
            pass

    def get_metrics(self) -> bytes:
        self.update_resource_metrics()
        return generate_latest(REGISTRY)


metrics_collector = MetricsCollector()


def get_metrics_output() -> bytes:
    return metrics_collector.get_metrics()
