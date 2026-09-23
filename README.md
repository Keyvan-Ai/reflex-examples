# Mankei Reflex — client examples

Examples for calling **[Mankei Reflex](https://huggingface.co/keyvan-ai/Mankei-Reflex)**, the German System One decision model: typed decisions with calibrated probabilities, in one pass, on your own hardware.

This repository contains **clients and example requests only** — no model code. The model, the engine and the evaluation package are distributed via Hugging Face under the Mankei Reflex Evaluation License.

- Live demos: [Reflex Pilot](https://mankei.ai/reflex/) · [Reflex Browser](https://mankei.ai/reflex/browser/)
- Model card: https://huggingface.co/keyvan-ai/Mankei-Reflex (English / Deutsch)
- Website: https://mankei.ai

## The wire format

Reflex speaks the System One wire format. One state, many typed questions, one response:

```jsonc
POST /v1/reflex            // or /v1/systemone — same format, drop-in for Jev clients
{
  "state": { "szene": "Fußgänger 12 m voraus auf der Fahrbahn, quert. Stoppschild in 30 m.", "tempo_kmh": 28 },
  "questions": {
    "lage":     { "type": "choice", "instructions": "Was ist die Lage vor dem Fahrzeug?",
                  "criteria": { "freie Fahrt": null, "Person auf oder neben der Fahrbahn": null, "Hindernis auf der Fahrbahn": null, "Gefahr": null } },
    "person":   { "type": "noul",   "instructions": "Auf oder neben der Fahrbahn befindet sich eine Person." },
    "dringend": { "type": "score",  "instructions": "Wie dringend ist die Lage?", "criteria": ["keine", "gering", "mittel", "hoch", "kritisch"] }
  }
}
```

```jsonc
{
  "model": "mankei-reflex",
  "answers": {
    "lage":     { "type": "choice", "choice": "Person auf oder neben der Fahrbahn", "confidence": 0.99, "probabilities": { "...": 0.0 } },
    "person":   { "type": "noul",   "noul": 0.99 },
    "dringend": { "type": "score",  "score": 3.4, "confidence": 0.49, "probabilities": { "0": 0.0, "1": 0.01, "2": 0.1, "3": 0.4, "4": 0.49 } }
  },
  "usage": { "input_tokens": 41, "output_tokens": 0 }
}
```

German state, German questions: the public block is trained on German; English and French blocks are available to enterprise customers.

Three primitives: **choice** (2–255 options, optionally with descriptions as the criteria values), **score** (ordered levels, expected value), **noul** (probability of a statement). Answers do not depend on the order of questions or options.

## Python

```python
from reflex_client import Reflex
r = Reflex("http://127.0.0.1:8088")            # your Reflex server
a = r.decide(state={"aeusserung": "stell den Wecker auf sieben Uhr"},
             questions={"absicht": r.choice("Welche Absicht drückt die Äußerung aus?", ["alarm_set", "alarm_remove", "weather_query", "calendar_set"])})
print(a["absicht"]["choice"], a["absicht"]["confidence"])
```

See [`python/reflex_client.py`](python/reflex_client.py) and [`python/examples.py`](python/examples.py).

## JavaScript / Node

```js
import { Reflex } from "./javascript/reflex-client.mjs";
const r = new Reflex("http://127.0.0.1:8088");
const a = await r.decide({ szene: "…" }, { lage: r.choice("Was ist die Lage vor dem Fahrzeug?", ["freie Fahrt", "Gefahr"]) });
```

## Example states

`examples/` holds ready-to-send requests, in German (the language the public block is trained on):

| File | Use case |
|---|---|
| `fahrzeug.json` | vehicle scene: situation ahead, person on the road, danger |
| `drohne.json` | drone: obstacle on the route, overflyable, people below |
| `portal.json` | browser automation: next action and target element on a portal page |
| `absicht.json` | assistant intent routing (MASSIVE-style labels) |

Send any of them with:

```bash
curl -s http://127.0.0.1:8088/v1/reflex -H "Content-Type: application/json" --data-binary @examples/fahrzeug.json
```

## Many states in one call

`POST /v1/reflex/batch` takes a list of requests and answers them in one forward pass — for example every obstacle ahead of a drone, or several documents at once:

```jsonc
{ "requests": [ { "state": {…}, "questions": {…} }, { "state": {…}, "questions": {…} } ] }
// -> { "results": [ { "answers": {…} }, { "answers": {…} } ], "mankei": { "latenz_ms": 40, "anfragen": 2, "fragen": 6 } }
```

One decision takes about 30 ms on a workstation GPU, five questions about 33 ms, four states with three questions each about 40 ms, one hundred questions in one call about a quarter of a second.

## Drop-in for Jev clients

Any client that speaks the System One format can point at Reflex instead: set the base URL to `http://<host>:8088` and use `/v1/systemone`. Request and response fields (`choice`, `score`, `noul`, `confidence`, `probabilities`, `usage`) are the same.

## Licence

These examples are released under the MIT License. The model and engine are licensed separately (see the model card).
