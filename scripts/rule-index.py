#!/usr/bin/env python3
"""Generate docs/spec/satin/rules.md, the list of every rule of the Satin section.

The script reads every page under docs/spec/satin/ (rules.md itself excepted), finds each rule
id written as the specification's writing rules require — inline code at the start of the
paragraph or list item that states the rule — and writes one table per page: the id, the rule's
first sentence, and a link to the page that is its home. Ids listed under a "Retired" heading, or
whose text starts with "Retired", are listed as retired. A page still marked as a stub lists
proposed ids, not rules, and is skipped.

It fails, writing nothing, when an id is defined on more than one line, when an id is both
active and retired, when a relative link on a Satin page names a file that does not exist, or
when a page has no title.

Usage:
    scripts/rule-index.py            write docs/spec/satin/rules.md
    scripts/rule-index.py --check    fail when docs/spec/satin/rules.md is not up to date
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SECTION = os.path.join(ROOT, "docs", "spec", "satin")
OUTPUT = os.path.join(SECTION, "rules.md")
INDEX = os.path.join(SECTION, "overview.md")

RULE = re.compile(r"^\s*(?:[-*] |\d+\. )?`(SATIN-[A-Z]+-\d{3})`\s+(\S.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
COMMENT = re.compile(r"<!--.*?-->")
SUMMARY_MAX = 220
STUB = "This page is a stub."


@dataclass
class Rule:
    rule_id: str
    summary: str
    retired: bool
    line: int


@dataclass
class Page:
    path: str  # relative to SECTION
    title: str
    rules: list[Rule] = field(default_factory=list)


def first_sentence(text: str) -> str:
    """The rule's first sentence, plain enough for one table cell."""
    text = COMMENT.sub("", text)
    text = MD_LINK.sub(r"\1", text).strip()
    # A sentence ends at a full stop followed by a space, outside inline code.
    out, in_code = [], False
    for i, ch in enumerate(text):
        if ch == "`":
            in_code = not in_code
        out.append(ch)
        if ch == "." and not in_code and (i + 1 == len(text) or text[i + 1] == " "):
            break
    sentence = "".join(out).strip()
    if len(sentence) > SUMMARY_MAX:
        cut = sentence[:SUMMARY_MAX].rsplit(" ", 1)[0]
        if cut.count("`") % 2:
            cut += "`"
        sentence = cut + " …"
    return sentence.replace("|", "\\|")


def read_page(path: str) -> tuple[Page, list[str]]:
    rel = os.path.relpath(path, SECTION).replace(os.sep, "/")
    errors: list[str] = []
    title = None
    rules: list[Rule] = []
    retired_section_level = None
    in_fence = False
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = HEADING.match(line)
        if heading:
            level, text = len(heading.group(1)), heading.group(2)
            if level == 1 and title is None:
                title = text
            if retired_section_level is not None and level <= retired_section_level:
                retired_section_level = None
            if "retired" in text.lower():
                retired_section_level = level
            continue
        for target in LINK.findall(line):
            if re.match(r"[a-z][a-z0-9+.-]*:", target):
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            # rules.md is this script's output: a link to it resolves once it is written.
            if not os.path.exists(resolved) and resolved != os.path.normpath(OUTPUT):
                errors.append(f"{rel}:{number}: link to a missing page: {target}")
        match = RULE.match(line)
        if match:
            rule_id, text = match.group(1), match.group(2)
            plain = COMMENT.sub("", text).strip()
            retired = retired_section_level is not None or plain.lower().startswith("retired")
            rules.append(Rule(rule_id, first_sentence(text), retired, number))
    if title is None:
        errors.append(f"{rel}: no title")
        title = rel
    return Page(rel, title, rules), errors


def page_order() -> list[str]:
    """The pages in the reading order the section's overview links them in."""
    order = ["overview.md"]
    with open(INDEX, encoding="utf-8") as f:
        text = f.read()
    # The overview's "Specifications" section lists the pages in reading order.
    text = text.split("\n## Specifications", 1)[-1]
    for target in LINK.findall(text):
        if target.endswith(".md") and not re.match(r"[a-z]+:", target):
            rel = os.path.normpath(target).replace(os.sep, "/")
            if not rel.startswith("..") and rel not in order:
                order.append(rel)
    return order


def collect() -> tuple[list[Page], list[str]]:
    paths = []
    for directory, _, files in os.walk(SECTION):
        for name in files:
            full = os.path.join(directory, name)
            if name.endswith(".md") and os.path.abspath(full) != os.path.abspath(OUTPUT):
                paths.append(full)
    pages, errors = [], []
    for path in paths:
        with open(path, encoding="utf-8") as f:
            if STUB in f.read():
                # A stub lists proposed ids, not rules; it is skipped until its page is written.
                continue
        page, page_errors = read_page(path)
        pages.append(page)
        errors.extend(page_errors)
    order = page_order()
    rank = {p: i for i, p in enumerate(order)}
    pages.sort(key=lambda p: (rank.get(p.path, len(order)), p.path))

    homes: dict[str, list[str]] = {}
    for page in pages:
        for rule in page.rules:
            homes.setdefault(rule.rule_id, []).append(f"{page.path}:{rule.line}")
    for rule_id, places in sorted(homes.items()):
        if len(places) > 1:
            errors.append(f"{rule_id} is defined more than once: {', '.join(places)}")
    return pages, errors


def render(pages: list[Page]) -> str:
    active = sum(1 for p in pages for r in p.rules if not r.retired)
    retired = sum(1 for p in pages for r in p.rules if r.retired)
    out = [
        "---",
        "description: Satin (unstable) — Satin Rules. Every rule id of the Satin section, with a "
        "one-line summary and a link to the page that states it.",
        "spec: Satin",
        "maturity: unstable",
        "---",
        "",
        "# Satin Rules",
        "",
        '{% hint style="warning" %}',
        "**Unstable** — Satin is under active development: everything on this page may change "
        "before Satin is frozen.",
        "{% endhint %}",
        "",
        "Abstract: The list of every rule of the Satin section: its id, the first sentence of the "
        "rule, and the page that states it in full.",
        "",
        "This page is generated by `scripts/rule-index.py` from the pages of the section and is "
        "not edited by hand.",
        "A summary is the rule's first sentence only; the rule is the text on its page.",
        f"The section states {active} rules; {retired} ids are retired.",
        "",
    ]
    for page in pages:
        if not page.rules:
            continue
        out += [f"## {page.title}", "", f"Home: [{page.title}]({page.path})", ""]
        live = sorted((r for r in page.rules if not r.retired), key=lambda r: r.rule_id)
        gone = sorted((r for r in page.rules if r.retired), key=lambda r: r.rule_id)
        if live:
            out += ["| Id | Rule |", "| --- | --- |"]
            for rule in live:
                out.append(f"| [`{rule.rule_id}`]({page.path}) | {rule.summary} |")
            out.append("")
        if gone:
            out += ["Retired ids:", "", "| Id | Status |", "| --- | --- |"]
            for rule in gone:
                out.append(f"| `{rule.rule_id}` | {rule.summary} |")
            out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def main(argv: list[str]) -> int:
    check = "--check" in argv[1:]
    pages, errors = collect()
    if errors:
        for error in errors:
            print(f"rule-index: {error}", file=sys.stderr)
        return 1
    text = render(pages)
    # Every link this page writes is to a page that exists (collect() read each one).
    if check:
        try:
            with open(OUTPUT, encoding="utf-8") as f:
                current = f.read()
        except FileNotFoundError:
            current = ""
        if current != text:
            print("rule-index: docs/spec/satin/rules.md is not up to date", file=sys.stderr)
            return 1
        return 0
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(text)
    rules = sum(len(p.rules) for p in pages)
    print(f"rule-index: {rules} ids on {sum(1 for p in pages if p.rules)} pages -> "
          f"{os.path.relpath(OUTPUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
