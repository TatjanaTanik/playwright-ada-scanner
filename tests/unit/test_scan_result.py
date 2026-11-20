# Unit tests for ScanResult: fake axe violations, no browser needed
from scanner.config import ScanConfig
from scanner.scan import ScanResult


def make_violation(rule_id, impact, tags):
    # A tiny fake violation with only the keys ScanResult reads
    return {"id": rule_id, "impact": impact, "tags": tags, "nodes": [{}]}


# One violation of each kind we care about
CRITICAL_WCAG = make_violation("image-alt", "critical", ["wcag2a"])
MINOR_WCAG = make_violation("some-minor-rule", "minor", ["wcag2aa"])
MODERATE_BEST_PRACTICE = make_violation("region", "moderate", ["best-practice"])
ALL_VIOLATIONS = [CRITICAL_WCAG, MINOR_WCAG, MODERATE_BEST_PRACTICE]


def make_result(config):
    # A ScanResult with all three fake violations and the given settings
    return ScanResult(name="Test page", url="https://example.com", target="page",
                      config=config, violations=ALL_VIOLATIONS)


def test_default_settings_block_only_critical_to_moderate_wcag():
    # Arrange + Act: default settings (critical, serious, moderate)
    result = make_result(ScanConfig())

    # Assert: critical blocks; minor and best-practice are only warnings
    assert result.blocking == [CRITICAL_WCAG]
    assert result.warnings == [MINOR_WCAG, MODERATE_BEST_PRACTICE]


def test_minor_blocks_when_team_asks_for_it():
    # Arrange + Act: this team wants all four impacts to fail
    result = make_result(ScanConfig(fail_on=["critical", "serious", "moderate", "minor"]))

    # Assert: minor now blocks too; best-practice still never blocks
    assert result.blocking == [CRITICAL_WCAG, MINOR_WCAG]
    assert result.warnings == [MODERATE_BEST_PRACTICE]


def test_critical_only_team():
    # Arrange + Act: this team only cares about critical
    result = make_result(ScanConfig(fail_on=["critical"]))

    # Assert: only the critical one blocks
    assert result.blocking == [CRITICAL_WCAG]
