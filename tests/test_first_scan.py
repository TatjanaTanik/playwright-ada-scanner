from axe_playwright_python.sync_playwright import Axe

def test_home_page_accessibility(page):
    # open the page
    page.goto("https://www.w3.org/WAI/demos/bad/before/home.html")
    # create the Axe object
    axe = Axe()
    # run the scan
    results = axe.run(page)
    #print how many violations
    print("Violations found:", results.violations_count)
