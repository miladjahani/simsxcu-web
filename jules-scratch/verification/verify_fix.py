from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:5173/simsxcu-web/")
        page.locator('input[name="v_v_percent"]').fill("0")
        page.click('button:has-text("اجرای شبیه‌سازی")')
        page.wait_for_selector("text=نتایج شبیه‌سازی")
        page.screenshot(path="jules-scratch/verification/verification.png")
        browser.close()

if __name__ == "__main__":
    run()