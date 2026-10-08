<img src="https://raw.githubusercontent.com/mahimailabs/.github/main/profile/assets/banner.svg" alt="Mahimai: build voice products that keep working. From prototype to production." width="100%">

**Mahimai Labs builds open-source infrastructure for voice AI.** Cost tracking, multi-agent runtimes, long-term memory and open reference data for teams shipping voice agents on LiveKit and Pipecat.

We are the open-source side of [Mahimai AI](https://mahimai.ca). The tools here come out of seven years of putting voice systems into production for enterprises, founders and public-sector teams, and they are used every day by the builders who run them.

<!-- stats starts --><b>12</b> open-source projects · <b>113</b> stars · <b>7</b> packages on PyPI<!-- stats ends -->

### Products

<!-- projects_products starts -->
| Project | What it does | Latest | Stars |
|---|---|---|---|
| **[voicegateway](https://github.com/mahimailabs/voicegateway)** | Cost tracking, observability and inference routing for voice agents on LiveKit, Pipecat and OpenRTC. | [0.27.0](https://pypi.org/project/voicegateway/)<br><sub>Oct 2026</sub> | ★ 52 |
| **[openrtc-runtime](https://github.com/mahimailabs/openrtc-runtime)** | Runs many LiveKit voice agents in one Python worker, sharing heavy models instead of loading them per process. | [0.20.1](https://pypi.org/project/openrtc/)<br><sub>Sep 2026</sub> | ★ 11 |
| **[livekit-plugins-voicemem](https://github.com/mahimailabs/livekit-plugins-voicemem)** | Long-term memory for LiveKit voice agents, backed by PostgreSQL and pgvector. Remembers both what the caller said and what they are like. | [0.2.2](https://pypi.org/project/livekit-plugins-voicemem/)<br><sub>Sep 2026</sub> | ★ 2 |
| **[shipvoice](https://github.com/mahimailabs/shipvoice)** | Full-stack LiveKit voice agent starter: a Python voice worker, a FastAPI token server and a React frontend, each deployable on its own. | <sub>updated Oct 2026</sub> | ★ 30 |
| **[envoic](https://github.com/mahimailabs/envoic)** | Finds and reports the Python virtual environments on a machine, so they stop piling up. | [0.3.1](https://pypi.org/project/envoic/)<br><sub>Jul 2026</sub> | ★ 6 |
<!-- projects_products ends -->

### Open data and references

<!-- projects_data starts -->
| Project | What it does | Latest | Stars |
|---|---|---|---|
| **[voice-prices](https://github.com/mahimailabs/voice-prices)**<br><sub><a href="https://prices.mahimai.ca">prices.mahimai.ca</a></sub> | Open price database for voice AI APIs: STT, LLM, TTS, speech-to-speech and VAD. | [0.11.0](https://pypi.org/project/voice-prices/)<br><sub>Sep 2026</sub> | ★ 6 |
| **[voice-ai-skills](https://github.com/mahimailabs/voice-ai-skills)**<br><sub><a href="https://skills.mahimai.ca">skills.mahimai.ca</a></sub> | Vendor-neutral Agent Skills for people who build voice agents. Read by Claude Code, Cursor, Codex, Copilot, Gemini CLI. | <sub>updated Sep 2026</sub> | ★ 2 |
| **[voice-latency](https://github.com/mahimailabs/voice-latency)** | A per-hop latency budget for voice agents: cascaded and realtime (speech-to-speech), plus framework overhead. The numbers are the point, PR better ones. | [0.1.1](https://pypi.org/project/voice-latency/)<br><sub>Aug 2026</sub> | ★ 1 |
| **[handset-bench](https://github.com/mahimailabs/handset-bench)** | Benchmark text-to-speech on what survives a G.711 telephone line: 8kHz, mu-law, 300-3400 Hz, packet loss | [0.1.0](https://pypi.org/project/handset-bench/)<br><sub>Aug 2026</sub> | ★ 0 |
<!-- projects_data ends -->

### Examples and starters

<!-- projects_examples starts -->
| Project | What it does | Latest | Stars |
|---|---|---|---|
| **[gpt-live-voice-agent](https://github.com/mahimailabs/gpt-live-voice-agent)** | OpenAI GPT-Live full-duplex voice agent on LiveKit, side by side with a classic STT-LLM-TTS cascade. Run both, interrupt both, see what breaks. | <sub>updated Sep 2026</sub> | ★ 2 |
| **[voicemem-demo](https://github.com/mahimailabs/voicemem-demo)** | A LiveKit voice agent that remembers you between calls, in ~100 lines. Built on livekit-plugins-voicemem. | <sub>updated Sep 2026</sub> | ★ 1 |
| **[voicegateway-examples](https://github.com/mahimailabs/voicegateway-examples)** | Example projects that run on VoiceGateway. | <sub>updated Jun 2026</sub> | ★ 0 |
<!-- projects_examples ends -->

<table>
<tr>
<td valign="top" width="50%">

#### From the blog
<!-- writing starts -->
[Voice Agent Appointment Booking: Book by Slot ID](https://mahimai.ca/blog/voice-agent-appointment-booking)<br><sub>Oct 2026</sub>

[Voice Agent State: Let the Tool Own the Count](https://mahimai.ca/blog/voice-agent-state-water-tracker)<br><sub>Oct 2026</sub>

[FNOL Voice Agent: Validate Every Field in the Tool](https://mahimai.ca/blog/voice-claim-intake-fnol-agent)<br><sub>Oct 2026</sub>

[Voice Agent RAG: Show the Source, Admit the Miss](https://mahimai.ca/blog/voice-rag-tenant-rights-sources)<br><sub>Oct 2026</sub>

[GPT-Live with LiveKit: Beyond the First Working Call](https://mahimai.ca/blog/gpt-live-livekit-beyond-first-call)<br><sub>Oct 2026</sub>
<!-- writing ends -->

More on [mahimai.ca/blog](https://mahimai.ca/blog)
</td>
<td valign="top" width="50%">

#### Recently merged
<!-- merged starts -->
[feat: meter GPT-Live duration and realtime audio separately](https://github.com/mahimailabs/voicegateway/pull/311)<br><sub>voicegateway · Oct 2026 · @mahimairaja</sub>

[feat: add private call summaries and normalize usage metering](https://github.com/mahimailabs/voicegateway/pull/310)<br><sub>voicegateway · Oct 2026 · @mahimairaja</sub>

[docs(readme): put the badges and cover in one palette, with a light variant](https://github.com/mahimailabs/openrtc-runtime/pull/149)<br><sub>openrtc-runtime · Sep 2026 · @mahimairaja</sub>

[refactor(security): remove the Wave 0 contracts for planned telemetry work](https://github.com/mahimailabs/voicegateway/pull/304)<br><sub>voicegateway · Sep 2026 · @mahimairaja</sub>

[fix(tests): wait on conditions instead of fixed sleeps](https://github.com/mahimailabs/voicegateway/pull/305)<br><sub>voicegateway · Sep 2026 · @mahimairaja</sub>

[ci: run the test suite in parallel with pytest-xdist](https://github.com/mahimailabs/voicegateway/pull/303)<br><sub>voicegateway · Sep 2026 · @mahimairaja</sub>
<!-- merged ends -->

Contributions are welcome in every repository.
</td>
</tr>
</table>

### Work with us

Mahimai AI takes voice agents from prototype to production: architecture, latency and cost, telephony, and evaluation. [mahimai.ca](https://mahimai.ca) · [Book a call](https://cal.com/mahimairaja/consulting)

If our open-source work saves your team time, you can support it through [GitHub Sponsors](https://github.com/sponsors/mahimairaja).

<p align="center"><sub>This page rebuilds itself every six hours. <a href="https://github.com/mahimailabs/.github/blob/main/build_profile.py">How this works</a></sub></p>
