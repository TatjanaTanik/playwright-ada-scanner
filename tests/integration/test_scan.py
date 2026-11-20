# Integration tests: our scanner against real public W3C example pages (needs internet)
import pytest

from scanner.scan import find_open_modal, scan
from scanner.constants import *

# W3C "bad" demo page: an ordinary page with no modals at all
NO_MODAL_PAGE = "https://www.w3.org/WAI/demos/bad/before/home.html"

# W3C's official modal dialog example (ARIA Authoring Practices Guide)
MODAL_EXAMPLE_PAGE = "https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/"

# Button on the example page that opens its first modal
OPEN_MODAL_BUTTON = "Add Delivery Address"

# The id W3C gives that first modal, so we know we found the right one
FIRST_MODAL_ID = "dialog1"


def test_no_modal_returns_none(page):
    # Arrange: a page with no modal
    page.goto(NO_MODAL_PAGE)

    # Assert: nothing found, so the whole page would be scanned
    assert find_open_modal(page) is None


def test_closed_modals_are_ignored(page):
    # Arrange: open the example page; its modals are in the page but closed
    page.goto(MODAL_EXAMPLE_PAGE)

    # Assert: the closed modals really exist in the page code
    assert page.locator(MODAL_SELECTOR).count() > 0
    # but none is visible, so "no open modal"
    assert find_open_modal(page) is None


def test_open_modal_is_found(page):
    # Arrange: open the example page
    page.goto(MODAL_EXAMPLE_PAGE)

    # Act: click the button like a user, then look for the open modal
    page.get_by_role("button", name=OPEN_MODAL_BUTTON).click()
    modal = find_open_modal(page)

    # Assert: found, and its the modal that button opens
    assert modal is not None
    assert modal.get_attribute("id") == FIRST_MODAL_ID


def test_scan_whole_page_finds_violations(page):
    # Arrange: the W3C demo page, which is broken on purpose
    page.goto(NO_MODAL_PAGE)

    # scan the whole page with default settings
    result = scan(page, "W3C bad demo home")

    # scans the page and looks for problems
    assert result.target == "page"
    assert result.url == NO_MODAL_PAGE
    assert len(result.violations) > 0

def test_scan_modal_scans_only_the_open_modal(page):
    # Arrange: open the W3C example page and click the button that opens the modal
    page.goto(MODAL_EXAMPLE_PAGE)
    page.get_by_role("button", name=OPEN_MODAL_BUTTON).click()

    # scans only open modal
    result = scan(page, "Add Delivery Address modal", modal=True)

    # Assert: the modal was scanned, and sticker is off
    assert result.target == "modal"
    assert page.locator(f"[{SCAN_TARGET_ATTRIBUTE}]").count() == 0

def test_modal_true_without_open_modal_fails_clearly(page):
    # Arrange: the example page with no open modal
    page.goto(MODAL_EXAMPLE_PAGE)

    # Assert: asking for a modal that isn't open stops with our clear message
    with pytest.raises(AssertionError, match="no open modal"):
            scan(page, "Missing modal", modal=True)

