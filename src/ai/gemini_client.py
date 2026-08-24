import requests


class GeminiRESTClient:
    """Small dependency-free Gemini client using the official REST endpoint."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, model: str, system: str, prompt: str, json_mode: bool) -> str:
        payload = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }
        if json_mode:
            payload["generationConfig"]["responseMimeType"] = "application/json"
        response = None
        last_error = ""
        model_candidates = [model]
        if model == "gemini-2.5-flash":
            model_candidates.append("gemini-3.6-flash")
        for candidate_model in model_candidates:
            for version in ("v1beta", "v1"):
                candidate = None
                for attempt in range(2):
                    try:
                        candidate = requests.post(
                            f"https://generativelanguage.googleapis.com/{version}/models/{candidate_model}:generateContent",
                            headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
                            json=payload,
                            timeout=120,
                        )
                        break
                    except requests.exceptions.ReadTimeout:
                        if attempt == 1:
                            raise TimeoutError("Gemini took too long to generate the tailored CV.") from None
                assert candidate is not None
                if candidate.ok:
                    response = candidate
                    break
                last_error = f"HTTP {candidate.status_code}: {candidate.text[:500]}"
                if candidate.status_code != 404:
                    candidate.raise_for_status()
            if response is not None:
                break
        if response is None:
            raise ValueError(
                f"Gemini could not find a usable model for '{model}'. {last_error}"
            )
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError(f"Gemini returned no text: {data}") from exc
