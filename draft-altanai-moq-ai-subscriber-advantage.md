---
title: "Detecting AI-Driven Subscriber Advantage in Media over QUIC (MOQ)"
abbrev: "MOQ AI Subscriber Advantage"
category: info
docname: draft-altanai-moq-ai-subscriber-advantage-00
submissiontype: IETF
date: 2026-02-10
consensus: false
v: 1
area: "Web and Internet Transport"
keyword:
  - MOQ
  - fairness
  - AI
  - media transport

author:
  -
    fullname: "Altanai Bisht"
    organization: "Cisco"
    email: "altanai@outlook.com"

normative:
  RFC2119:
  RFC8174:

informative:
  MoQTransport:
    title: "Media over QUIC Transport"
    author:
      org: "IETF MOQ WG"
    date: 2026
    target: "https://datatracker.ietf.org/doc/draft-ietf-moq-transport/"
  MoQMetrics:
    title: "Metrics over MOQT"
    author:
      name: "C. Jennings"
    date: 2025
    target: "https://datatracker.ietf.org/doc/draft-jennings-moq-metrics/"
  AIPrefNetwork:
    title: "AI Preferences for Privacy-Preserving Network Traffic Analysis"
    author:
      name: "A. Bisht"
      org: "Cisco"
    date: 2025
    target: "https://datatracker.ietf.org/doc/draft-aipref-network-privacy-control/"
---

--- abstract

This document describes the problem of unfair advantage that AI-driven participants may obtain in Media over QUIC (MOQ) groups, and outlines a scope for detecting such behavior in a privacy-preserving manner. It defines no protocol changes and is intended to inform future work in the MOQ and AI Preferences (AIPREF) working groups.

--- middle

# Introduction

Media over QUIC Transport (MOQT) [MoQTransport] enables publish/subscribe distribution of media over QUIC with relays, multiple subscribers, and prioritization. As endpoints may use AI to optimize subscription strategy, track selection, or join/leave timing, the possibility arises that AI-driven behavior obtains systematically better quality of experience or relay resources than non-AI or less aggressive endpoints — an "unfair AI advantage."

Operators and relay providers may wish to **detect** when observed behavior is consistent with such advantage, for capacity planning, fairness policy, or transparency, while respecting privacy. This document provides a short problem statement and scope for that detection, and relates it to existing MOQ and AI preference work.

# Motivation

Beyond unfairness to other subscribers, AI-enabled subscribers can harm or stress CDN relay servers in several ways. Detection of such behavior benefits relay operators for capacity planning, abuse mitigation, and service assurance.

- **Resource exhaustion**: AI can learn to maximize cache hits, bandwidth, or priority allocation. When many AI subscribers optimize selfishly, relay memory, CPU, and bandwidth can be exhausted by a subset of subscribers.

- **Subscription churn abuse**: AI can drive high rates of SUBSCRIBE, UNSUBSCRIBE, and REQUEST_UPDATE to exploit cache warming, scheduling, or priority handling. Excessive churn increases relay processing load and degrades scheduling effectiveness.

- **Priority abuse**: AI can learn relay prioritization behavior and time requests to consistently obtain higher priority. At scale, this forces the relay to process disproportionate high-priority traffic and complicates fair scheduling.

- **Cache exploitation**: AI can time requests to maximize cache hits for itself while causing cache thrashing or eviction for others, increasing cache load and bandwidth usage.

- **Bandwidth monopolization**: AI can optimize the mix and timing of FETCH vs SUBSCRIBE to consume a disproportionate share of relay bandwidth, overloading egress capacity and degrading service for all subscribers.

- **Probing and discovery**: AI can probe relay behavior (scheduling, cache, rate limits) to discover optimizations or weaknesses, leading to patterns that stress the relay or exploit its design.

These harms motivate relay operators to detect behavior consistent with unfair AI advantage, in addition to fairness concerns among subscribers.

# Problem Statement

In MOQ, subscribers subscribe to tracks and receive objects; they may use REQUEST_UPDATE, priorities, and subscription filters. Relays forward objects based on subscription state and metadata. If some subscribers use AI to:

- optimize which tracks they subscribe to and when they switch (e.g., ABR),
- time subscriptions and fetches to obtain lower latency or better cache hit behavior, or
- exploit prioritization or relay scheduling in ways that disadvantage other subscribers,

then those subscribers may receive systematically better service. That creates an **unfair AI advantage** relative to subscribers that do not use such optimization.

Detection in this context means: identifying behavior patterns (from relay- or transport-observable signals) that are consistent with such advantage, without requiring access to payload or to whether an endpoint is "AI" or "human." This document does not define what constitutes "fair" or "unfair" in a policy or legal sense.

# Scope

## In Scope

- Problem statement for unfair AI advantage in MOQ groups (as above).
- **Observable signals** that could support detection: e.g., subscription rate, track-switch rate, join/leave timing relative to group boundaries, use of priorities, and object-request patterns. These can be derived from relay-visible metadata (MOQT does not encrypt metadata from relays).
- **Privacy-preserving detection**: using aggregates, anonymized identifiers, or preference-bound data exposure, consistent with frameworks such as [AIPrefNetwork] (e.g., "Detecting Unfair Bandwidth Usage" with limited identity and retention).
- Relationship to MOQT (tracks, namespaces, subscribe/fetch, relay behavior) and to metrics work (e.g., [MoQMetrics]).

## Out of Scope

- Defining legal or policy meaning of "fair" or "unfair."
- Standardizing specific ML algorithms or detection logic.
- Protocol changes to MOQT for enforcement or remediation.
- Authentication or attestation of "AI" vs "non-AI" endpoints.

# Observable Signals for Detection

The following are candidate signals that relays or analysis systems could use (in aggregate and with appropriate privacy controls) to detect behavior consistent with unfair advantage. They are informative only.

| Signal | Description | Privacy consideration |
|--------|-------------|------------------------|
| Subscription churn | Rate of SUBSCRIBE / UNSUBSCRIBE / REQUEST_UPDATE per endpoint or per track | Aggregate by namespace or anonymized ID |
| Track-switch timing | Timing of subscription changes relative to group boundaries or catalog updates | No payload; metadata only |
| Priority distribution | Use of priority values across subscriptions per endpoint | Aggregate |
| Object request pattern | FETCH vs SUBSCRIBE mix, and request timing | Relay already has this; restrict retention and identity |
| Join latency | Time from track availability to first subscription from an endpoint | Per-endpoint only with consent or anonymized |

Detection mechanisms SHOULD respect preference frameworks (e.g., AIPREF) for what data is exposed to AI or analytics systems and at what granularity.

# Relationship to Other Work

- **MOQ Transport** [MoQTransport]: Provides the data model (tracks, groups, objects), subscription lifecycle, and relay behavior. Detection builds on relay-visible metadata and existing control messages.
- **Metrics over MOQT** [MoQMetrics]: Defines metrics for MOQT; extension for fairness-related metrics (e.g., per-subscriber or per-namespace aggregates) could align with this problem.
- **AI Preferences (AIPREF)** [AIPrefNetwork]: Defines preferences for AI processing of network traffic, including "unfair usage patterns" and "Detecting Unfair Bandwidth Usage." MOQ traffic is one application; preferences for what MOQ metadata AI may use for fairness detection could be expressed with the same vocabulary.

# Security and Privacy Considerations

Detection that uses per-endpoint or per-subscription data can reveal behavior patterns and potentially identity. Implementations SHOULD use aggregation, anonymization, and minimal retention. Preference expression (e.g., AIPREF) allows users and operators to bound what data is exposed to AI systems. This document does not introduce new protocol mechanisms and does not change MOQT or QUIC security properties.

# IANA Considerations

This document has no IANA actions.

--- back

# References

## Normative References

\[RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119, March 1997, <https://www.rfc-editor.org/rfc/rfc2119>.

\[RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174, May 2017, <https://www.rfc-editor.org/rfc/rfc8174>.

## Informative References

\[MoQTransport] Nandakumar, S., Vasiliev, V., Swett, I., and A. Frindell, "Media over QUIC Transport", Work in Progress, Internet-Draft, draft-ietf-moq-transport-16, January 2026, <https://datatracker.ietf.org/doc/draft-ietf-moq-transport/>.

\[MoQMetrics] Jennings, C., "Metrics over MOQT", Work in Progress, Internet-Draft, draft-jennings-moq-metrics-02, October 2025, <https://datatracker.ietf.org/doc/draft-jennings-moq-metrics/>.

\[AIPrefNetwork] Bisht, A., "AI Preferences for Privacy-Preserving Network Traffic Analysis", Work in Progress, Internet-Draft, draft-aipref-network-privacy-control-00, <https://datatracker.ietf.org/doc/draft-aipref-network-privacy-control/>.
