<!-- regenerate: off -->

# Detecting AI-Driven Subscriber Advantage in Media over QUIC (MOQ)

This is the working area for the individual Internet-Draft, "Detecting AI-Driven Subscriber Advantage in Media over QUIC (MOQ)".

* [Editor's Copy](https://altanai.github.io/draft-altanai-moq-ai-subscriber-advantage/#go.draft-altanai-moq-ai-subscriber-advantage.html)
* [Datatracker Page](https://datatracker.ietf.org/doc/draft-altanai-moq-ai-subscriber-advantage)
* [Individual Draft](https://datatracker.ietf.org/doc/html/draft-altanai-moq-ai-subscriber-advantage)
* [Compare Editor's Copy to Individual Draft](https://altanai.github.io/draft-altanai-moq-ai-subscriber-advantage/#go.draft-altanai-moq-ai-subscriber-advantage.diff)


## Contributing

See the
[guidelines for contributions](https://github.com/altanai/draft-altanai-moq-ai-subscriber-advantage/blob/main/CONTRIBUTING.md).

The contributing file also has tips on how to make contributions, if you
don't already know how to do that.

## Command Line Usage

Formatted text and HTML versions of the draft can be built using `make`.

```sh
$ make
```

Command line usage requires that you have the necessary software installed.  See
[the instructions](https://github.com/martinthomson/i-d-template/blob/main/doc/SETUP.md).


## Scope of the first submission

The draft covers contextual comparison of subscriber resource use and
service outcomes, a six-step privacy process, and an exploratory extension
for authorization-bound resource budgets. The extension builds on MoQT,
Common Access Tokens for MoQT (C4M), Privacy Pass, and relay DoS work.
Budget claims, example limits, and response policies are design proposals,
not standardized protocol fields or evidence that a subscriber uses AI.

## Supporting material

- [Four-slide proposal deck](output/pdf/moq_ai_subscriber_advantage_4slides.pdf)
- [Background overview and component diagram](output/html/proposal-overview.html)
- [Illustrative comparison example](output/html/worked-example.html)

The HTML pages provide background on the detection work; the Markdown
source contains the expanded resource-budget proposal for submission.
Open the supporting HTML pages locally with the adjacent `site.css` file.
The PDF includes Altanai Bisht in each slide footer and links to the
underlying draft and related work.

The deck generator is `scripts/generate_deck.py`; it requires Python with
`reportlab`. The IETF logo is included as a presentation asset; its use
alongside an individual proposal does not indicate IETF endorsement.

## Building and submitting

`make` builds the editor's copy. `make next` generates the next numbered
submission under `versioned/`. `make check idnits_mode=submission` runs
the template's submission checks. The first numbered submission is `-00`.

Pushing a tag such as `draft-altanai-moq-ai-subscriber-advantage-00`
triggers `.github/workflows/publish.yml`, which builds the numbered draft
and uploads it to the IETF Datatracker. Complete any author confirmation
requested by Datatracker to finish formal posting.
