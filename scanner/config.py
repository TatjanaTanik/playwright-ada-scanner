from dataclasses import dataclass, field

# WCAG 2.0 / 2.1 / 2.2, levels A and AA
WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]

# Optional: WCAG 2.0 AAA (axe has no AAA tags for 2.1 and 2.2)
AAA_TAG = "wcag2aaa"

# Optional: axe rules that are good practice but not required by WCAG
BEST_PRACTICE_TAG = "best-practice"

ALLOWED_IMPACTS = ["critical", "serious", "moderate", "minor"]
DEFAULT_FAIL_ON = ["critical", "serious", "moderate"]


@dataclass
class ScanConfig:
    fail_on: list[str] = field(default_factory=DEFAULT_FAIL_ON.copy)
    include_aaa: bool = False
    include_best_practice: bool = False

    def __post_init__(self):
        self.fail_on = [impact.lower() for impact in self.fail_on]
        unknown = [impact for impact in self.fail_on if impact not in ALLOWED_IMPACTS]
        if unknown:
            raise ValueError(f"Unknown impacts: {unknown}. Use {', '.join(ALLOWED_IMPACTS)}")

    def axe_tags(self):
        # Start with A/AA tags every scan uses
        tags = WCAG_TAGS
        if self.include_aaa:
            # + makes a NEW list, so WCAG_TAGS itself never changes
            tags = tags + [AAA_TAG]
        if self.include_best_practice:
            # Same: new list, the constant stays untouched
            tags = tags + [BEST_PRACTICE_TAG]
        return tags

    def scope_label(self):
        # Short text for the report header, for example "A/AA + AAA"
        scope = "A/AA"
        if self.include_aaa:
            scope += " + AAA"
        if self.include_best_practice:
            scope += " + best-practice"
        return scope
