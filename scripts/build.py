#!/usr/bin/env python3
"""Regenerate the static homepage using only the Python standard library."""
import html
import json
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
PAPERS = json.loads((ROOT / "data/publications.json").read_text())


def escape(value):
    return html.escape(str(value), quote=True)


def article(paper):
    authors = ", ".join(
        f'<strong>{escape(name)}</strong>' if name == "Langzhang Liang" else escape(name)
        for name in paper["authors"]
    )
    links = [f'<a href="{escape(paper[key])}"{external}> {label}<span aria-hidden="true">↗</span></a>'
             for key, label in [("paper", "Paper"), ("pdf", "PDF"), ("code", "Code")]
             if key in paper
             for external in [' target="_blank" rel="noopener noreferrer"']]
    if paper.get("image"):
        figure = f'''<button class="paper-figure" type="button" data-figure="{escape(paper['image'])}"
            data-title="{escape(paper['title'])}" aria-label="Enlarge figure for {escape(paper['title'])}">
          <img src="{escape(paper['image'])}" alt="{escape(paper['image_alt'])}" width="720" height="440" loading="lazy">
          <span class="enlarge" aria-hidden="true">↗</span>
        </button>'''
    else:
        # A text treatment is used when the paper has no available figure.
        label = paper.get("visual_label", ["LEARNING THEORY", "Regret bounds", "Online sparse linear regression"])
        figure = f'<div class="theory-figure" aria-hidden="true"><span>{escape(label[0])}</span><i>{escape(label[1])}</i><span class="theory-rule"></span><small>{escape(label[2])}</small></div>'
    return f'''<article class="paper" id="{escape(paper['id'])}" data-topic="{escape(paper['topic'])}">
      {figure}
      <div class="paper-body">
        <div class="paper-meta"><span class="venue{' preprint-venue' if paper['status'] == 'preprint' else ''}" title="{escape(paper['venue_full'])}">{escape(paper['venue'])}</span></div>
        <h3><a href="{escape(paper['paper'])}" target="_blank" rel="noopener noreferrer">{escape(paper['title'])}</a></h3>
        <p class="authors">{authors}</p>
        <p class="paper-summary">{escape(paper['summary'])}</p>
        <div class="paper-links">{''.join(links)}</div>
      </div>
    </article>'''


def group(status):
    output, previous_year = [], None
    for paper in PAPERS:
        if paper["status"] != status:
            continue
        if paper["year"] != previous_year and status == "published":
            output.append(f'<h3 class="year-heading" data-year="{paper["year"]}"><span>{paper["year"]}</span></h3>')
            previous_year = paper["year"]
        output.append(article(paper))
    return "\n".join(output)


assert len({paper["id"] for paper in PAPERS}) == len(PAPERS), "Duplicate publication ID"
assert all(paper["status"] in ("published", "preprint") for paper in PAPERS)
for paper in PAPERS:
    if paper.get("image"):
        assert (ROOT / paper["image"]).is_file(), f'Missing figure: {paper["image"]}'
template = Template((ROOT / "scripts/homepage.template.html").read_text())
output = template.substitute(
    publications=group("published"),
    preprints=group("preprint"),
    publication_count=sum(p["status"] == "published" for p in PAPERS),
    preprint_count=sum(p["status"] == "preprint" for p in PAPERS),
)
(ROOT / "index.html").write_text(output)
print(f"Built index.html: {len(PAPERS)} papers")
