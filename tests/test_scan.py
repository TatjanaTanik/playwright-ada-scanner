# Integration tests: our scanner against real public W3C example pages (needs internet)

from scanner.scan import MODAL_SELECTOR, find_open_modal

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
    page.goto(MODAL_EXAMPLE_PAGE)

    # Act: click the button like a user, then look for the open modal
    page.get_by_role("button", name=OPEN_MODAL_BUTTON).click()
    modal = find_open_modal(page)

    # Assert: found, and its the modal that button opens
    assert modal is not None
    assert modal.get_attribute("id") == FIRST_MODAL_ID

