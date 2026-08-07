#!/usr/bin/env python3
"""Verify canonical web resume, print source, and generated PDF content parity."""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB_PATH = ROOT / "index.html"
PRINT_PATH = ROOT / "casey-mathieson-resume.html"
PDF_PATH = ROOT / "casey-mathieson-resume.pdf"
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


@dataclass
class Node:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list[Node | str] = field(default_factory=list)

    def text(self) -> str:
        parts = [child.text() if isinstance(child, Node) else child for child in self.children]
        return " ".join(" ".join(parts).split())


class TreeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, {name: value or "" for name, value in attrs})
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data)


def parse(path: Path) -> Node:
    parser = TreeParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.root


def walk(node: Node):
    for child in node.children:
        if isinstance(child, Node):
            yield child
            yield from walk(child)


def has_class(node: Node, class_name: str) -> bool:
    return class_name in node.attrs.get("class", "").split()


def find_all(node: Node, *, tag: str | None = None, class_name: str | None = None) -> list[Node]:
    return [
        item
        for item in walk(node)
        if (tag is None or item.tag == tag) and (class_name is None or has_class(item, class_name))
    ]


def first(node: Node, *, tag: str | None = None, class_name: str | None = None) -> Node:
    matches = find_all(node, tag=tag, class_name=class_name)
    if not matches:
        raise ValueError(f"Missing element: tag={tag!r}, class={class_name!r}")
    return matches[0]


def tokens(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value).lower()
    return re.findall(r"[a-z0-9]+", normalized)


def same_content(left: str, right: str) -> bool:
    return tokens(left) == tokens(right)


def contains_tokens(haystack: list[str], needle: list[str]) -> bool:
    if not needle:
        return True
    size = len(needle)
    return any(haystack[index : index + size] == needle for index in range(len(haystack) - size + 1))


def role_nodes(job: Node) -> list[Node]:
    return [item for item in walk(job) if has_class(item, "role") or item.tag == "h4"]


def job_units(job: Node) -> dict[str, list[str]]:
    return {
        "company": [first(job, tag="h3").text()],
        "dates": [first(job, class_name="dates").text()],
        "roles": [item.text() for item in role_nodes(job)],
        "bullets": [item.text() for item in find_all(job, tag="li")],
    }


def compare_lists(label: str, canonical: list[str], print_values: list[str], failures: list[str]) -> int:
    checks = 1
    if len(canonical) != len(print_values):
        failures.append(f"{label}: item count differs ({len(canonical)} web, {len(print_values)} print)")
        return checks
    for index, (expected, actual) in enumerate(zip(canonical, print_values), start=1):
        checks += 1
        if not same_content(expected, actual):
            failures.append(f"{label} #{index}\n  web:   {expected}\n  print: {actual}")
    return checks


def main() -> int:
    web = parse(WEB_PATH)
    print_doc = parse(PRINT_PATH)
    failures: list[str] = []
    checks = 0

    scalar_pairs = [
        ("Name", first(web, tag="h1").text(), first(print_doc, tag="h1").text()),
        ("Headline", first(web, class_name="target").text(), first(print_doc, class_name="headline").text()),
        ("Summary", first(web, class_name="summary").text(), first(print_doc, class_name="summary").text()),
    ]
    for label, expected, actual in scalar_pairs:
        checks += 1
        if not same_content(expected, actual):
            failures.append(f"{label}\n  web:   {expected}\n  print: {actual}")

    web_skills = [item.text() for item in find_all(web, class_name="skill-card")]
    print_skills = [item.text() for item in find_all(print_doc, class_name="skill-group")]
    checks += compare_lists("Expertise", web_skills, print_skills, failures)

    web_jobs = find_all(web, class_name="job-card")
    print_jobs = find_all(print_doc, tag="article", class_name="job")
    checks += 1
    if len(web_jobs) != len(print_jobs):
        failures.append(f"Experience: job count differs ({len(web_jobs)} web, {len(print_jobs)} print)")
    else:
        for job_index, (web_job, print_job) in enumerate(zip(web_jobs, print_jobs), start=1):
            web_units = job_units(web_job)
            print_units = job_units(print_job)
            for unit_name in ("company", "dates", "roles", "bullets"):
                checks += compare_lists(
                    f"Job {job_index} {unit_name}", web_units[unit_name], print_units[unit_name], failures
                )

    web_credentials = [item.text() for item in find_all(web, class_name="credential")]
    print_credentials = [item.text() for item in find_all(print_doc, class_name="credential")]
    checks += compare_lists("Credentials", web_credentials, print_credentials, failures)

    if failures:
        print("Resume HTML parity check failed:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1

    try:
        from pypdf import PdfReader
    except ImportError:
        print("HTML parity passed, but PDF verification requires pypdf: py -m pip install pypdf", file=sys.stderr)
        return 2

    reader = PdfReader(PDF_PATH)
    pdf_tokens = tokens(" ".join(page.extract_text() or "" for page in reader.pages))
    print_units = [
        first(print_doc, tag="h1").text(),
        first(print_doc, class_name="headline").text(),
        first(print_doc, class_name="contact").text(),
        first(print_doc, class_name="summary").text(),
        *print_skills,
        *print_credentials,
    ]
    for job in print_jobs:
        units = job_units(job)
        print_units.extend(units["company"] + units["dates"] + units["roles"] + units["bullets"])

    pdf_missing = [unit for unit in print_units if not contains_tokens(pdf_tokens, tokens(unit))]
    if pdf_missing:
        print("PDF parity check failed; regenerate the PDF. Missing print-source units:")
        print("\n".join(f"- {unit}" for unit in pdf_missing))
        return 1

    print(
        f"Resume parity passed: {checks} HTML comparisons and {len(print_units)} PDF content units "
        f"across {len(reader.pages)} page(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
