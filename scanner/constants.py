# All fixed values the scanner uses

# WCAG 2.0 / 2.1 / 2.2, levels A and AA
# No wcag22aa: axe has no rules for the new 2.2 Level A criteria (manual testing only)
WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]

# Optional: WCAG 2.0 AAA (axe has no AAA tags for 2.1 and 2.2)
AAA_TAG = "wcag2aaa"

# Optional: axe rules that are good practice but not required by WCAG
BEST_PRACTICE_TAG = "best-practice"

# The four impact levels axe uses, and 3 that fail the test by default
ALLOWED_IMPACTS = ["critical", "serious", "moderate", "minor"]
DEFAULT_FAIL_ON = ["critical", "serious", "moderate"]

# modals: ARIA dialogs and the native <dialog> element
MODAL_SELECTOR = '[role="dialog"], [role="alertdialog"], [aria-modal="true"], dialog[open]'

# Temporary marker for the open modal, so axe scans only inside it
SCAN_TARGET_ATTRIBUTE = "data-ada-scan-target"