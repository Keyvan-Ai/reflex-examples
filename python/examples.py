"""Run every example request in ../examples against a Reflex server and print the typed answers."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from reflex_client import Reflex

r = Reflex(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8088")
for p in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "examples", "*.json"))):
    req = json.load(open(p, encoding="utf-8"))  # "_comment" is ignored by the server
    a = r.decide(req["state"], req["questions"])
    print(f"== {os.path.basename(p)}")
    for name, ans in a.items():
        value = ans.get("choice") if ans["type"] == "choice" else ans.get("score") if ans["type"] == "score" else round(ans["noul"], 3)
        print(f"   {name:14s} {value!s:34s} {ans.get('confidence', '')}")
