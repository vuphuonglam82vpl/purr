from playwright.sync_api import sync_playwright
from handle_venom_wallet import handle_venom_wallet_window
from swapsl import swapsl
import time  # Import thêm module time

def mua_url_with_profile_and_extension():
    url = "https://web3.world/swap/0:77d36848bb159fa485628bc38dc37eadb74befa514395e09910f601b841f749e/0:3a26c7d83b44dcb80818898a0846411db1446071725de8d77c706f8a56ee45a8"
    user_data_dir = r"C:\Users\Administrator\Documents\github\purr\data"
    extension_path = r"C:\Users\Administrator\Documents\extension\ojggmchlghnjlapmfbnjholfjkiidbch"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=[
                "--headless=new",                
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}"
            ]
        )
        try:
            context = browser
            page = context.pages[0] if context.pages else context.new_page()
            processed_pages = []

            page.goto(url)
            print(f"Đã mở URL với profile và extension: {extension_path}")
            page.wait_for_load_state("networkidle")
            swapsl(page)
            page.wait_for_timeout(1000)

            for opened_page in context.pages:
                if opened_page not in processed_pages:
                    handle_venom_wallet_window(opened_page, processed_pages)
                    processed_pages.append(opened_page)

            print("Chờ 30 giây trước khi đóng trình duyệt...")
            time.sleep(30)
        finally:
            browser.close()
