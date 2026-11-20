# Unit tests for ScanConfig: fast checks, no browser needed

import pytest
from scanner.constants import *
from scanner.config import ScanConfig

def test_default_settings():
    # Arrange: a config with no values, uses default
    config = ScanConfig()

    # Assert: defaults are critical/serious/moderate, AAA off, best-practice off
    assert config.fail_on == ["critical", "serious", "moderate"]
    assert config.include_aaa is False
    assert config.include_best_practice is False

def test_custom_fail_on_is_lowercased():
    # Arrange: list written with capital letters
    config = ScanConfig(fail_on=["Critical", "SERIOUS"])

    # Assert: the list is kept, converts to lowercase
    assert config.fail_on == ["critical", "serious"]

def test_unknown_impact_raises_error():
    # A typo must stop the scan with a clear error
    # pytest.raises: the test PASSES only if this ValueError happens,
    # and match = checks the message names the bad word
    with pytest.raises(ValueError, match="critcal"):
        ScanConfig(fail_on=["critcal"])

def test_aaa_and_best_practice_add_tags_without_changing_wcag_tags():
    # Arrange: both optional switches on
    config = ScanConfig(include_aaa=True, include_best_practice=True)

    # Assert: both extra tags are added after A/AA tags
    assert config.axe_tags() == WCAG_TAGS + [AAA_TAG, BEST_PRACTICE_TAG]
    # Assert: the shared constant did not changed
    assert AAA_TAG not in WCAG_TAGS

def test_scope_label_lists_what_was_scanned():
    # Arrange: one config with defaults, one with both switches
    default_config = ScanConfig()
    full_config = ScanConfig(include_aaa=True, include_best_practice=True)

    # Assert: the report header text matches the switches
    assert default_config.scope_label() == "A/AA"
    assert full_config.scope_label() == "A/AA + AAA + best-practice"
