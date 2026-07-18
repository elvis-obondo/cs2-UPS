"""Visit the deployed Streamlit app to reset its inactivity timer.

Streamlit Community Cloud hibernates apps after 12 hours without traffic. A
plain HTTP GET only fetches the static shell -- Streamlit counts traffic
through a live WebSocket session, which only a real browser opens. This
loads the app in headless Chromium and clicks through the wake screen if
the app was already asleep.
"""
import os
import sys

from playwright.sync_api import sync_playwright

APP_URL = os.environ["APP_URL"]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL, wait_until="networkidle", timeout=60_000)

        wake_button = page.get_by_role("button", name="Yes, get this app back up")
        try:
            wake_button.wait_for(state="visible", timeout=15_000)
        except Exception:
            print(f"{APP_URL} is already awake.")
            browser.close()
            return

        print("App was asleep, clicking wake button...")
        wake_button.click()
        wake_button.wait_for(state="hidden", timeout=60_000)
        browser.close()
        print(f"Woke {APP_URL} successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Failed to keep app awake: {exc}")
        sys.exit(1)
