---
title: "Detecting AI-Driven Subscriber Advantage in Media over QUIC (MOQ)"
abbrev: "MOQ Subscriber Advantage"
category: info
docname: draft-altanai-moq-ai-subscriber-advantage-latest
submissiontype: IETF
date: 2026-11-15
consensus: false
v: 3
area: "Web and Internet Transport"
keyword:
  - MOQ
  - fairness
  - AI
  - authorization
  - resource budgets

author:
  - fullname: "Altanai Bisht"
    organization: "Cisco"
    email: "altanai@outlook.com"

informative:
  MoQTransport: I-D.ietf-moq-transport
  MoQMetrics: I-D.jennings-moq-metrics
  RelayDoS: I-D.englishm-moq-relay-dos
  C4M: I-D.ietf-moq-c4m
  PrivacyPass: I-D.ietf-moq-privacy-pass-auth
  AIPrefRealtime: I-D.altanai-aipref-realtime-protocol-bindings
  RFC9000:
  RFC6973:
  RFC6357:
  RFC7339:
  RFC7415:
  RFC4412:
  RFC8836:
  RFC8888:
--- abstract

This document describes subscriber behavior that may produce sustained
advantages in service outcomes or disproportionate resource consumption
at shared Media over QUIC (MoQ) relays. AI-assisted optimization is a
motivating scenario; observations alone cannot establish whether AI was
used or caused a disparity. The document outlines contextual measurement,
privacy safeguards, and a proposed extension for authorization-bound
resource budgets with explicit accounting and recovery behavior. It
builds on existing MoQ authorization and relay denial-of-service work.
This informational document defines no new MoQ messages, token claims,
registries, or standardized detection algorithm.

--- middle

# Introduction

Media over QUIC Transport (MoQT) {{MoQTransport}} supports delivery of
tracks through relays that serve multiple subscribers. Endpoints can
optimize track selection, request timing, subscription filters, and
relative priority. These choices may be made by an AI model, a
conventional adaptive algorithm, or fixed application rules.

Operators may wish to identify sustained differences in resource use
or service outcomes among comparable subscribers. A disparity can be
useful for capacity planning, service assurance, or a review of relay
policy. It is not by itself evidence of misconduct, an unfair policy,
or use of AI. Higher quality can be a legitimate result of a better path,
authorized service treatment, or more efficient application behavior.

This document develops two related questions: how to observe such
patterns while limiting subscriber data exposure, and how a future
resource-budget profile could associate explicit usage limits with
existing authorization mechanisms. The latter extends the original
detection scope and is presented as design considerations for further
work, rather than a completed token or enforcement specification.

# Terminology and Scope

A subscriber endpoint can hold multiple subscriptions. A subscription
is a relationship for receiving one track; it is distinct from a MoQT
session, which can carry multiple subscriptions and fetches. Separate
subscriber endpoints commonly use separate sessions. The object and
session model is defined by {{MoQTransport}}.

For this document, a *comparison cohort* is a group of observations
matched for content, service policy, observation interval, and relevant
path conditions. A *candidate advantage* is a sustained disparity in
resource use or delivery outcomes within such a cohort. The designation
identifies a measurement for review and does not establish its cause.

A *resource budget* is a proposed policy describing an allowed amount,
rate, or concurrency of a defined resource. An *accounting domain* is the
set of sessions and relay instances over which that budget applies.
An *accounting reference* identifies the shared usage state within that
domain and validity period; it need not expose an account identity to an
analytics system.

In scope are observable signals, interpretation of those signals,
privacy-conscious processing, resource-budget design considerations,
and relationships to existing MoQ and SIP mechanisms. Out of scope are
AI-versus-human attestation, universal definitions of fairness, monetary
penalties, standardized machine-learning algorithms or thresholds, and
new token encodings or protocol error codes. The illustrative policies
below are not interoperability requirements.

# Motivation and Problem Statement

Shared relay resources include CPU, subscription state, buffer memory,
cache capacity, backend services, and upstream and downstream bandwidth.
The incremental cost of a request depends on the implementation and
whether suitable upstream subscriptions or cached objects already exist.
Subscription aggregation can reduce upstream work. Substantial media
delivery following a small request is normal protocol operation and is
not sufficient evidence of abuse or harmful amplification.

Candidate concerns include:

- Repeated creation and cancellation of subscriptions, or frequent
  updates, causing processing and state-management costs.
- Request patterns that increase fetch work, cache turnover, or egress,
  subject to the relay's caching and aggregation behavior.
- Buffer accumulation from slow consumption or join-time delivery.
- A session consuming a disproportionate share of a constrained relay
  resource under the operator's allocation policy.

These concerns overlap with the threat analysis and operational guidance
in {{RelayDoS}}. This document emphasizes contextual comparison and
privacy considerations, together with an exploratory connection between
usage measurement and explicit resource authorization.

## Priority Scope

Subscriber priority influences transmission ordering among subscriptions
and fetch responses within the same MoQT session. A subscriber requesting
priority 0 does not thereby acquire a protocol-defined rank above a
subscriber in another session. Relays are advised not to copy downstream
subscriber priorities directly to upstream subscriptions; upstream
priorities depend on relay policy {{MoQTransport}}.

Frequent priority updates may consume parsing and scheduling resources.
Effects on other subscribers depend on shared-resource contention and
implementation policy. A priority value, a priority change, or an improved
delivery outcome alone does not demonstrate an unfair advantage. A
subscriber priority adjustment also does not implement a relay-wide
resource restriction across independent sessions.

# Observable Signals and Context

The following signals are candidates rather than mandatory metrics.
They are available only where a deployment can measure or attribute them.
Content or timing metadata can itself be sensitive even when media
payloads remain encrypted.

| Signal | Interpretation and context |
|--------|----------------------------|
| Subscription lifecycle activity | Count creations, cancellations, and updates over a defined interval; distinguish useful adaptation, retries, and pathological churn. |
| Track and filter changes | Compare changes relative to available content and group boundaries without retaining unnecessary viewing histories. |
| Priority updates | Measure update frequency and work; priority values are relative within a session. |
| FETCH and SUBSCRIBE mix | Account for historical delivery, repair, and duplicate requests; define what the byte count includes. |
| Resource consumption | Measure attributable egress, buffered bytes, or control-processing work; identify shared costs that cannot be assigned to one subscriber. |
| Delivery outcomes | Measure request-to-first-object or relay-observed delivery delay using defined endpoints and clocks; do not equate these with playback quality. |
| Cache and upstream effects | Use available hit, miss, eviction, and upstream-work counters while accounting for sharing among subscribers. |

{{MoQMetrics}} provides related measurement work. This document does not
redefine its metrics or assume that every candidate signal is already
standardized.

## Contextual Comparison

Choose a cohort and a measurement interval before interpreting a
disparity. Relevant context includes track variant and bitrate,
subscription duration, publisher timing, authorized service class,
cache state, path latency, congestion, and the relay's allocation policy.
Normalize measurements by active time or useful delivered content where
appropriate, and state the limits of attribution and sampling.

Persistence over several intervals can distinguish a sustained pattern
from a short transition, but does not demonstrate causality. An analyzer
should be able to return an inconclusive result when the cohort is too
small or required context is missing. Controlled experiments with known
client implementations can study AI-assisted behavior; relay telemetry
alone cannot reliably label arbitrary endpoints as AI or non-AI.

# Deployment Components

A possible deployment separates forwarding, budget accounting, and
privacy-limited analysis. These are logical components and may be
co-located. Existing token schemes provide the authorization foundation;
resource-budget interpretation and accounting require further design.

~~~
  Grant issuer -- authorization --> Subscriber
                                      |
                               token + request
                                      |
                                      v
  Publisher ---- media objects ---> Relay
                                      |
                           resource-use measurements
                                      |
                                      v
                                Budget ledger
                               /             \
                    limited signals       limit decision
                           /                   \
                    Privacy guard          Relay policy
                          |                 response
                          v
                   Authorized review
~~~

The issuer grants permissions. The relay validates the presented
authorization and maintains or consults usage state. The analytics path
receives the minimum information needed for comparison and review,
subject to the privacy process below. A comparison flag and a verified
budget violation are separate inputs to operator decisions.

# Privacy Process

The following deployment safeguards elaborate aggregation and minimal
retention. They are design guidance and do not establish a formal
anonymity guarantee. General privacy considerations are discussed in
{{RFC6973}}. Related AI-preference binding work {{AIPrefRealtime}} can
inform treatment of expressed processing preferences; a preference
signal does not itself anonymize data or authorize unrelated use.

1. **Define purpose and permitted processing.** Identify the measurement
   purpose, permitted fields, applicable preferences, and authorized
   recipients. Relay visibility of a field does not establish permission
   to retain or disclose it for every analytics purpose.
2. **Minimize collection.** Prefer counters and necessary control
   metadata. Avoid media-payload inspection, direct account identifiers
   in analytics, and AI-versus-human labels inferred from traffic.
3. **Scope pseudonyms.** Use short-lived identifiers specific to an
   analysis domain and interval. If a re-identification mapping is
   needed, keep it separately protected. A linkable token is pseudonymous,
   not anonymous, even if it does not contain a subscriber's name.
4. **Aggregate with context.** Prefer interval and cohort statistics.
   Coarsen or suppress small groups or detailed combinations that could
   reveal an individual. Minimum cohort sizes and any stronger privacy
   guarantees need to be defined by the deployment or a future profile.
5. **Limit and audit review.** Report the interval, cohort size, disparity,
   and measurement caveats. Restrict detailed inspection to authorized
   reviewers and record that access. A comparison flag alone does not
   establish a policy violation or justify automatic punishment.
6. **Expire detailed records.** Define retention periods for events,
   pseudonym mappings, usage state, and review records according to their
   respective purposes. Delete or aggregate records when those purposes
   end. A future profile needs explicit retention and deletion behavior.

Budget accounting may require continuity across sessions or token
renewals. That continuity should remain within the stated accounting
domain and budget period. Analytics pseudonym rotation does not reset
usage counters. Conversely, maintaining a budget does not justify a
permanent identifier shared across unrelated operators. Privacy Pass
work {{PrivacyPass}} is relevant to privacy-conscious authorization;
maintaining shared quotas and preventing repeated issuance from resetting
usage require an explicit design under the chosen token scheme.

# Authorization-Bound Resource Budgets

MoQT already carries authorization tokens {{MoQTransport}}. {{C4M}}
defines action and content scopes for Common Access Tokens and supports
revalidation of ongoing authorization. The proposed direction is to
specify how an authorized resource policy would be interpreted and
accounted for, reusing existing token capabilities where suitable.

The following are conceptual policy elements, not registered claims:

| Policy element | Design question |
|----------------|-----------------|
| Service class or policy reference | Which agreed policy does this label select, and which version applies? |
| Content and operation scope | Which tracks, namespaces, and actions are permitted under existing authorization rules? |
| Resource allowance | What concurrency, rate, bytes, or other measurable quantity is allowed? |
| Measurement window | Is the allowance instantaneous, rolling, or tied to an explicit interval; what burst behavior is permitted? |
| Accounting scope | Which sessions, relays, and issuer or operator domain share usage state? |
| Accounting reference | How are related authorizations associated with one budget without revealing unnecessary identity? |
| Validity and renewal | When does the grant expire, and how does renewal interact with remaining or already-used budget? |

A subscriber cannot grant itself a more generous policy by modifying a
trusted authorization. The issuer and verifier need integrity-protected
claims and an agreed interpretation. Adding an arbitrary field is not
sufficient: an implementation that does not understand a resource
restriction must not silently treat it as an unrestricted grant.
Any future encoding needs to follow the chosen token scheme's extension
and validation rules. This document does not allocate such an encoding.

## Usage State and Multiple Sessions

An authorization expresses a grant; it is not a mutable usage counter.
For example, four authorized concurrent subscriptions require the relay
to track admission and release of those subscriptions. Multiple tokens
or sessions associated with the same budget must share the intended
accounting state rather than each receiving the full allowance again.

A future profile needs to define atomic admission decisions, treatment
of pending and paused subscriptions, cancellation, disconnects, expiry,
and reclamation of abandoned reservations. If several relays enforce a
shared budget, the design needs to state its consistency model and how
it handles partitions or accounting-service failures. Partitioned
allowances or leases are possible approaches requiring further analysis.

Revalidating an unchanged signature does not by itself reveal a quota
change or update shared counters. Changes to authorization require a
specified mechanism such as a stateful policy check, a replacement grant,
expiry, or a supported revocation mechanism. Fresh token issuance and
renewal need explicit rules so that they cannot unintentionally reset an
exhausted allowance. These requirements must be reconciled with privacy
and unlinkability objectives of the selected authorization scheme.

## Policy Response and Recovery

A relay can enforce a clear admission or rate rule without inferring AI
use, intent, or moral fault. Possible responses include rejecting an
excess request, applying a temporary request-rate limit, or requiring
renewed authorization where appropriate to the token scheme. Operators
choose policy and thresholds; this document defines no universal penalty.

A future profile needs to describe protocol feedback, recovery conditions,
restriction duration, and review of disputed measurements. It should
distinguish exhausted resources or quotas from invalid authorization and
use existing protocol errors according to their defined meanings. This
document assigns no new error codes and does not redefine subscriber
priority as a cross-session enforcement mechanism.

# Worked Examples

All values in this section are illustrative. They are neither measured
results nor standardized thresholds.

## A Comparison Signal

Consider seven subscriptions to the same live track, active for ten
minutes, under the same service policy and similar measured path
conditions. Suppose subscriber A has 88 MB/min of relay egress compared
with a peer median of 37 MB/min, and a median relay-observed delivery
delay of 104 ms compared with 181 ms. The egress counter includes repeat
and historical delivery as well as live objects; it does not count
unique content alone.

An analyzer could report the sustained difference for review. It would
still need to examine fetches, duplicate delivery, caching, publisher
behavior, and measurement quality. Higher egress and lower delay do not
prove that A caused another subscriber's delay, used AI, or exceeded an
authorized budget. An explicit policy violation requires separate
evidence against that policy.

## Four Authorized Active Subscriptions

Suppose an issuer grants access to an event namespace with a policy
allowing four active subscriptions across the sessions sharing one
budget. The grant is valid for ten minutes. These are conceptual policy
values; this document defines no claim names or serialization for them.

The relay admits four subscriptions and records four reservations. A
fifth active subscription would exceed the allowance, so the relay
rejects that request with appropriate existing feedback under its policy.
The four admitted subscriptions remain governed by their existing terms.
Repeated excess requests may trigger a documented temporary request-rate
restriction. Admission can resume when a reservation is released and any
temporary restriction has ended, subject to valid authorization.

The accounting reference is scoped to the operator and budget period.
Detailed review is access-controlled, and retention follows the purposes
specified above. Opening another session or obtaining another token for
the same budget does not create another four reservations. How that
association is securely established remains part of the future profile.

# Relationship to Other Work

- **MoQ transport and metrics:** {{MoQTransport}} supplies the object,
  subscription, priority, and authorization framework. {{MoQMetrics}}
  provides related measurement work. This document does not replace
  transport flow control or congestion control {{RFC9000}}.
- **MoQ relay DoS:** {{RelayDoS}} already discusses cost tracking,
  per-client or per-identity limits, buffering, and resource isolation.
  The comparative measurement and privacy guidance here complements
  that work. Authorization and budget semantics should be developed in
  coordination with the relevant MoQ authorization work.
- **Common Access Tokens and Privacy Pass:** {{C4M}} and {{PrivacyPass}}
  provide existing authorization approaches. The resource-budget design
  needs further comparison with their capabilities, including the
  underlying Common Access Token specification. Token-based permission
  alone is not claimed as a new contribution.
- **SIP overload and authorized priority:** {{RFC6357}}, {{RFC7339}}, and
  {{RFC7415}} address SIP signaling overload; {{RFC6357}} discusses
  capacity allocation among upstream neighbors. {{RFC4412}} permits
  policy-authorized resource priority. These are useful precedents but
  operate at different scopes from per-subscriber MoQ relay analysis.
- **RTP congestion control:** {{RFC8836}} and {{RFC8888}} concern media
  congestion-control requirements and feedback. They do not themselves
  define the cohort comparison or authorization-bound relay budget
  considered here.

SIP deployments may face related questions around shared call-control
or media resources. A SIP proxy and a media relay do not necessarily
observe the same events. A SIP-specific design would require a separate
measurement model and is not specified by this document.

# Security and Privacy Considerations

Behavioral metadata can expose viewing patterns, correlate sessions,
and support identity inference. Pseudonyms and aggregates do not
eliminate those risks. Cohort size, granularity, retention, recipient
access, and correlation across purposes all affect exposure. The privacy
process above describes proposed safeguards, not a proof of anonymity.

A malicious client could distribute requests across sessions or tokens
to avoid isolated limits. A malicious or faulty accounting component
could overstate consumption and deny legitimate service. Shared ledgers
and revalidation endpoints can themselves become overload targets.
Budget enforcement therefore needs explicit trust boundaries, protected
accounting state, bounded processing, recovery behavior, and auditable
operator decisions. Local operator controls may still be needed during
accounting failures or legitimate flash crowds.

An advantage signal is not an authorization credential and does not
establish AI use or intent. A service-class claim does not reserve
physical capacity unless the deployment separately provides such a
service. This document does not change MoQT or QUIC security properties,
and its examples do not authorize disclosure of subscriber identity or
cross-operator reputation records.

# IANA Considerations

This document has no IANA actions.

--- back
