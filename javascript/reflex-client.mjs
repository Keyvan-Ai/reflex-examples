// Minimal JavaScript client for Mankei Reflex (System One wire format). Node 18+ or browser.
export class Reflex {
  constructor(baseUrl = "http://127.0.0.1:8088", token = "mankei") { this.url = baseUrl.replace(/\/$/, "") + "/v1/reflex"; this.token = token; }
  choice(instructions, options, descriptions = {}) { return { type: "choice", instructions, criteria: Object.fromEntries(options.map((o) => [o, descriptions[o] ?? null])) }; }
  score(instructions, levels) { return { type: "score", instructions, criteria: levels }; }
  yesNo(instructions) { return { type: "noul", instructions }; }
  async decide(state, questions) {
    const r = await fetch(this.url, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${this.token}` }, body: JSON.stringify({ model: "mankei-reflex", state, questions }) });
    if (!r.ok) throw new Error(`Reflex ${r.status}: ${await r.text()}`);
    return (await r.json()).answers;
  }
}
