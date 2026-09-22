"""Minimal Python client for Mankei Reflex (System One wire format)."""
import json, urllib.request


class Reflex:
    def __init__(self, base_url="http://127.0.0.1:8088", token="mankei", timeout=60):
        self.url, self.token, self.timeout = base_url.rstrip("/") + "/v1/reflex", token, timeout

    @staticmethod
    def choice(instructions, options, descriptions=None):
        return {"type": "choice", "instructions": instructions,
                "criteria": {o: (descriptions or {}).get(o) for o in options}}

    @staticmethod
    def score(instructions, levels):
        return {"type": "score", "instructions": instructions, "criteria": list(levels)}

    @staticmethod
    def yes_no(instructions):
        return {"type": "noul", "instructions": instructions}

    def decide(self, state, questions):
        body = json.dumps({"model": "mankei-reflex", "state": state, "questions": questions}).encode()
        req = urllib.request.Request(self.url, body, {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.load(r)["answers"]
