from prometheus_client import CollectorRegistry, make_asgi_app

collector_registry = CollectorRegistry()
metrics_app = make_asgi_app(registry=collector_registry)
