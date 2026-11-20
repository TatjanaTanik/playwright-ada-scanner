# Runs axe on the current page, or only inside an open modal if one is showing
from dataclasses import dataclass

from axe_playwright_python.sync_playwright import Axe

from scanner.config import BEST_PRACTICE_TAG, DEFAULT_FAIL_ON, ScanConfig

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


@dataclass
class ScanResult:
    # Name the test gave this scan
    name: str
    # Address of the page that was scanned
    url: str
    # What was scanned: "page" or "modal"
    target: str
    # The settings this scan used
    config: ScanConfig
    # The raw list of violations axe returned
    violations: list

    @property
    def blocking(self):
        # Violations that fail the test: impact is in fail_on AND it's a real WCAG rule
        # (best-practice never blocks: it's advice, not WCAG requirement)
        return [
            v for v in self.violations
            if v["impact"] in self.config.fail_on and not is_best_practice(v)
        ]

    @property
    def warnings(self):
        # Everything that is not blocking: shown in the report, never fails the test
        blocking = self.blocking
        return [v for v in self.violations if v not in blocking]

def scan(page, name, fail_on=None, include_aaa=False, include_best_practice=False):
    # Settings for this one scan; no fail_on given means the defaults
    if fail_on is None:
        fail_on = DEFAULT_FAIL_ON
    config = ScanConfig(fail_on=fail_on, include_aaa=include_aaa, include_best_practice=include_best_practice)
    # Tell axe to run only the rules for chosen WCAG levels
    options = {"runOnly": {"type": "tag", "values": config.axe_tags()}}

    # Whole page: no context given, so axe scans everything on the page
    response = Axe().run(page, options=options).response

    # Pack everything into one result the test can check
    return ScanResult(name=name, url=page.url, target="page", config=config, violations=response["violations"])
