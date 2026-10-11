"""Check a response against explicit instructions such as length, format and required content."""
import json
from dataclasses import dataclass


@dataclass
class Constraints:
    min_words: int | None = None
    max_words: int | None = None
    bullet_count: int | None = None  # exact number of lines starting with "- " or "* "
    must_include: tuple = ()
    must_avoid: tuple = ()
    must_be_json: bool = False


def check(response, constraints):
    """Return a list of failure messages. An empty list means every constraint passed."""
    failures = []
    words = len(response.split())

    if constraints.min_words is not None and words < constraints.min_words:
        failures.append(f"too short: {words} words, needs at least {constraints.min_words}")
    if constraints.max_words is not None and words > constraints.max_words:
        failures.append(f"too long: {words} words, allowed at most {constraints.max_words}")

    if constraints.bullet_count is not None:
        bullets = sum(1 for line in response.splitlines() if line.lstrip().startswith(("- ", "* ")))
        if bullets != constraints.bullet_count:
            failures.append(f"expected {constraints.bullet_count} bullets, found {bullets}")

    lowered = response.lower()
    for term in constraints.must_include:
        if term.lower() not in lowered:
            failures.append(f"missing required text: {term!r}")
    for term in constraints.must_avoid:
        if term.lower() in lowered:
            failures.append(f"contains forbidden text: {term!r}")

    if constraints.must_be_json:
        try:
            json.loads(response)
        except json.JSONDecodeError as err:
            failures.append(f"invalid JSON: {err.msg}")

    return failures
