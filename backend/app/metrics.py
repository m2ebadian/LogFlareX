from prometheus_client import Counter, REGISTRY


def get_or_create_counter(name: str, documentation: str) -> Counter:
    """
    Safely retrieves an existing Prometheus Counter if already registered,
    or creates and registers a new one.

    Args:
        name (str): The unique name of the counter metric.
        documentation (str): A description of what the metric tracks.

    Returns:
        Counter: A Prometheus Counter object ready to be incremented.
    """
    # Check if the metric already exists in the global registry
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]

    # Register a new counter if not already present
    return Counter(name, documentation)


# Define all custom LogflareX metrics here

error_log_counter: Counter = get_or_create_counter(
    "logflarex_error_logs_total",
    "Total number of ERROR logs ingested"
)