<img src="https://raw.githubusercontent.com/mahimailabs/.github/main/profile/assets/banner.svg" alt="Mahimai: build voice products that keep working. From prototype to production." width="100%">

**Mahimai Labs builds open-source infrastructure for voice AI.** Cost tracking, multi-agent runtimes, long-term memory and open reference data for teams shipping voice agents on LiveKit and Pipecat.

We are the open-source side of [Mahimai AI](https://mahimai.ca). The tools here come out of seven years of putting voice systems into production for enterprises, founders and public-sector teams, and they are used every day by the builders who run them.

<!-- stats starts --><b>12</b> open-source projects · <b>109</b> stars · <b>7</b> packages on PyPI<!-- stats ends -->

### Products

<!-- projects_products starts -->
| Project | What it does | Latest | Stars |
|---|---|---|---|
| **[voicegateway](https://github.com/mahimailabs/voicegateway)** | Cost tracking, observability and inference routing for voice agents on LiveKit, Pipecat and OpenRTC. | [0.26.1](https://pypi.org/project/voicegateway/)<br><sub>Sep 2026</sub> | ★ 51 |
| **[openrtc-runtime](https://github.com/mahimailabs/openrtc-runtime)** | Runs many LiveKit voice agents in one Python worker, sharing heavy models instead of loading them per process. | [0.20.0](https://pypi.org/project/openrtc/)<br><sub>Sep 2026</sub> | ★ 11 |
| **[livekit-plugins-voicemem](https://github.com/mahimailabs/livekit-plugins-voicemem)** | Long-term memory for LiveKit voice agents, backed by PostgreSQL and pgvector. Remembers both what the caller said and what they are like. | [0.2.2](https://pypi.org/project/livekit-plugins-voicemem/)<br><sub>Sep 2026</sub> | ★ 2 |
| **[shipvoice](https://github.com/mahimailabs/shipvoice)** | Full-stack LiveKit voice agent starter: a Python voice worker, a FastAPI token server and a React frontend, each deployable on its own. | <sub>updated Aug 2026</sub> | ★ 30 |
| **[envoic](https://github.com/mahimailabs/envoic)** | Finds and reports the Python virtual environments on a machine, so they stop piling up. | [0.3.1](https://pypi.org/project/envoic/)<br><sub>Jul 2026</sub> | ★ 6 |
<!-- projects_products ends -->

### Open data and references

<!-- projects_data starts -->
| Project | What it does | Latest | Stars |
|---|---|---|---|
| **[voice-prices](https://github.com/mahimailabs/voice-prices)**<br><sub><a href="https://prices.mahimai.ca">prices.mahimai.ca</a></sub> | Open price database for voice AI APIs: STT, LLM, TTS, speech-to-speech and VAD. | [0.11.0](https://pypi.org/project/voice-prices/)<br><sub>Sep 2026</sub> | ★ 4 |
| **[voice-ai-skills](https://github.com/mahimailabs/voice-ai-skills)**<br><sub><a href="https://skills.mahimai.ca">skills.mahimai.ca</a></sub> | Vendor-neutral Agent Skills for people who build voice agents. Read by Claude Code, Cursor, Codex, Copilot, Gemini CLI. | <sub>updated Sep 2026</sub> | ★ 2 |
| **[voice-latency](https://github.com/mahimailabs/voice-latency)** | A per-hop latency budget for voice agents: cascaded and realtime (speech-to-speech), plus framework overhead. The numbers are the point, PR better ones. | [0.1.1](https://pypi.org/project/voice-latency/)<br><sub>Aug 2026</sub> | ★ 1 |
| **[handset-bench](https://github.com/mahimailabs/handset-bench)** | Benchmark text-to-speech on what survives a G.711 telephone line: 8kHz, mu-law, 300-3400 Hz, packet loss | [0.1.0](https://pypi.org/project/handset-bench/)<br><sub>Aug 2026</sub> | ★ 0 |
<!-- projects_data ends -->

### Examples and starters

<!-- projects_examples starts -->
| Project | What it does | Latest | Stars |
|---|---|---|---|
| **[gpt-live-voice-agent](https://github.com/mahimailabs/gpt-live-voice-agent)** | OpenAI GPT-Live full-duplex voice agent on LiveKit, side by side with a classic STT-LLM-TTS cascade. Run both, interrupt both, see what breaks. | <sub>updated Sep 2026</sub> | ★ 1 |
| **[voicemem-demo](https://github.com/mahimailabs/voicemem-demo)** | A LiveKit voice agent that remembers you between calls, in ~100 lines. Built on livekit-plugins-voicemem. | <sub>updated Sep 2026</sub> | ★ 1 |
| **[voicegateway-examples](https://github.com/mahimailabs/voicegateway-examples)** | Example projects that run on VoiceGateway. | <sub>updated Jun 2026</sub> | ★ 0 |
<!-- projects_examples ends -->

<table>
<tr>
<td valign="top" width="50%">

#### From the blog
<!-- writing starts -->
[How your voice travels through WebRTC: Voice AI agents edition](https://mahimai.ca/blog/how-your-voice-travels-through-webrtc)<br><sub>Sep 2026</sub>

[Your smoke run is lying to you](https://mahimai.ca/blog/your-smoke-run-is-lying-to-you)<br><sub>Aug 2026</sub>

[Building a phone line in PyTorch](https://mahimai.ca/blog/building-a-phone-line-in-pytorch)<br><sub>Aug 2026</sub>

[The normaliser that scored itself](https://mahimai.ca/blog/the-normaliser-that-scored-itself)<br><sub>Aug 2026</sub>
<!-- writing ends -->

More on [mahimai.ca/blog](https://mahimai.ca/blog)
</td>
<td valign="top" width="50%">

#### Recently merged
<!-- merged starts -->
[feat(brand): the split gauge mark](https://github.com/mahimailabs/voicegateway/pull/297)<br><sub>voicegateway · Sep 2026 · @mahimairaja</sub>

[feat(cli): add --port to the worker commands; stop leaking runtime flags to livekit](https://github.com/mahimailabs/openrtc-runtime/pull/146)<br><sub>openrtc-runtime · Sep 2026 · @mahimairaja</sub>

[chore(assets): remove the old brand artwork](https://github.com/mahimailabs/openrtc-runtime/pull/145)<br><sub>openrtc-runtime · Sep 2026 · @mahimairaja</sub>

[feat(site): bring the landing page into the repo as site/web, in the house style](https://github.com/mahimailabs/voicegateway/pull/294)<br><sub>voicegateway · Sep 2026 · @mahimairaja</sub>

[docs(readme): a lean README that leads with the problem and invites contributors](https://github.com/mahimailabs/openrtc-runtime/pull/138)<br><sub>openrtc-runtime · Sep 2026 · @mahimairaja</sub>

[docs(claude): no AI attribution in commits, PRs or comments](https://github.com/mahimailabs/openrtc-runtime/pull/137)<br><sub>openrtc-runtime · Sep 2026 · @mahimairaja</sub>
<!-- merged ends -->

Contributions are welcome in every repository.
</td>
</tr>
</table>

### Work with us

Mahimai AI takes voice agents from prototype to production: architecture, latency and cost, telephony, and evaluation. [mahimai.ca](https://mahimai.ca) · [Book a call](https://cal.com/mahimairaja/consulting)

If our open-source work saves your team time, you can support it through [GitHub Sponsors](https://github.com/sponsors/mahimairaja).

<p align="center"><sub>This page rebuilds itself every six hours. <a href="https://github.com/mahimailabs/.github/blob/main/build_profile.py">How this works</a></sub></p>
