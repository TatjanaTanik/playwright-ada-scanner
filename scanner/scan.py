# Runs axe on the current page, or only inside an open modal if one is showing
from axe_playwright_python.sync_playwright import Axe

from scanner.config import BEST_PRACTICE_TAG

# modals: ARIA dialogs and the native <dialog> element
MODAL_SELECTOR = '[role="dialog"], [role="alertdialog"], [aria-modal="true"], dialog[open]'

def is_best_practice(violation):
    # axe gives every rule a list of tags
    return BEST_PRACTICE_TAG in violation["tags"]

def find_open_modal(page):
    # Every modal-like element that is visible on screen right now
    modals = page.locator(MODAL_SELECTOR).filter(visible=True)
    # None visible: the caller scans the whole page
    if modals.count() == 0:
        return None
    #  Several stacked dialogs, the last one in the page is the one on top
    return modals.last

