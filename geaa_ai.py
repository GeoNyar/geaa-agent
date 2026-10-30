"""Resilient Gemini generation helpers for GEAA.

The Google Gen AI SDK handles bounded exponential-backoff retries.
GEAA only switches models after the primary model ultimately returns HTTP 503.
"""
PRIMARY_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODEL = "gemini-3.8-flash"


def get_http_status(error):
    """Extract an HTTP status from common Google SDK/API error shapes."""
    for attribute in ("code", "status_code"):
        value = getattr(error, attribute, None)
        if value is not None:
            try:
                return int(value)
            except (TypeError, ValueError):
                pass

    response = getattr(error, "response", None)
    value = getattr(response, "status_code", None)
    if value is not None:
        try:
            return int(value)
        except (TypeError, ValueError):
            pass
    return None


def classify_gemini_error(error):
    """Return a stable category for user-facing error handling."""
    status = get_http_status(error)
    if status == 503:
        return "service_unavailable"
    if status == 429:
        return "rate_limited"
    if status in (401, 403):
        return "authentication"
    if status == 404:
        return "model_unavailable"
    if status is not None and 500 <= status <= 599:
        return "server_error"
    return "other"


class GeminiFallbackError(Exception):
    """Both the primary request and its fallback path failed."""

    def __init__(self, primary_error, fallback_error, stage):
        self.primary_error = primary_error
        self.fallback_error = fallback_error
        self.stage = stage
        super().__init__(
            "Primary Gemini model failed with HTTP "
            f"{get_http_status(primary_error)}; fallback {stage} failed with HTTP "
            f"{get_http_status(fallback_error)}."
        )


def generate_content_with_fallback(client, contents, config=None):
    """Generate with the primary model, falling back only after a final 503.

    Before using the fallback model, verify that the current API key can
    retrieve its model metadata. This does not prove generation quota, but
    confirms model visibility/access for this key.
    """
    request = {"contents": contents}
    if config is not None:
        request["config"] = config

    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL, **request
        )
        return response, PRIMARY_MODEL
    except Exception as primary_error:
        if get_http_status(primary_error) != 503:
            raise

    try:
        client.models.get(model=FALLBACK_MODEL)
    except Exception as verification_error:
        raise GeminiFallbackError(
            primary_error, verification_error, "verification"
        ) from verification_error

    try:
        response = client.models.generate_content(
            model=FALLBACK_MODEL, **request
        )
        return response, FALLBACK_MODEL
    except Exception as fallback_error:
        raise GeminiFallbackError(
            primary_error, fallback_error, "generation"
        ) from fallback_error
