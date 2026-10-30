import unittest

from geaa_ai import (
    FALLBACK_MODEL,
    PRIMARY_MODEL,
    GeminiFallbackError,
    classify_gemini_error,
    generate_content_with_fallback,
)


class FakeAPIError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(f"HTTP {code}")


class FakeModels:
    def __init__(self, generation_results=None, verification_error=None):
        self.generation_results = list(generation_results or [])
        self.verification_error = verification_error
        self.generation_calls = []
        self.verification_calls = []

    def generate_content(self, **kwargs):
        self.generation_calls.append(kwargs)
        result = self.generation_results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    def get(self, **kwargs):
        self.verification_calls.append(kwargs)
        if self.verification_error:
            raise self.verification_error
        return {"name": f"models/{kwargs['model']}"}


class FakeClient:
    def __init__(self, models):
        self.models = models


class GeminiResilienceTests(unittest.TestCase):
    def test_primary_success_does_not_check_or_use_fallback(self):
        expected = object()
        models = FakeModels([expected])
        response, model = generate_content_with_fallback(
            FakeClient(models), "test prompt"
        )
        self.assertIs(response, expected)
        self.assertEqual(model, PRIMARY_MODEL)
        self.assertEqual(len(models.generation_calls), 1)
        self.assertEqual(models.verification_calls, [])

    def test_503_verifies_and_uses_fallback(self):
        expected = object()
        models = FakeModels([FakeAPIError(503), expected])
        response, model = generate_content_with_fallback(
            FakeClient(models), "test prompt"
        )
        self.assertIs(response, expected)
        self.assertEqual(model, FALLBACK_MODEL)
        self.assertEqual(
            models.verification_calls, [{"model": FALLBACK_MODEL}]
        )
        self.assertEqual(
            [call["model"] for call in models.generation_calls],
            [PRIMARY_MODEL, FALLBACK_MODEL],
        )

    def test_429_does_not_trigger_fallback(self):
        models = FakeModels([FakeAPIError(429)])
        with self.assertRaises(FakeAPIError):
            generate_content_with_fallback(
                FakeClient(models), "test prompt"
            )
        self.assertEqual(len(models.generation_calls), 1)
        self.assertEqual(models.verification_calls, [])

    def test_authentication_error_does_not_trigger_fallback(self):
        models = FakeModels([FakeAPIError(403)])
        with self.assertRaises(FakeAPIError):
            generate_content_with_fallback(
                FakeClient(models), "test prompt"
            )
        self.assertEqual(len(models.generation_calls), 1)
        self.assertEqual(models.verification_calls, [])

    def test_fallback_access_is_verified_before_generation(self):
        models = FakeModels(
            [FakeAPIError(503)],
            verification_error=FakeAPIError(403),
        )
        with self.assertRaises(GeminiFallbackError) as caught:
            generate_content_with_fallback(
                FakeClient(models), "test prompt"
            )
        self.assertEqual(caught.exception.stage, "verification")
        self.assertEqual(len(models.generation_calls), 1)
        self.assertEqual(len(models.verification_calls), 1)

    def test_error_classification(self):
        self.assertEqual(
            classify_gemini_error(FakeAPIError(503)),
            "service_unavailable",
        )
        self.assertEqual(
            classify_gemini_error(FakeAPIError(429)),
            "rate_limited",
        )
        self.assertEqual(
            classify_gemini_error(FakeAPIError(401)),
            "authentication",
        )


if __name__ == "__main__":
    unittest.main()
