def handle_venom_wallet_window(page, processed_pages):
    """
    Chuyển sang cửa sổ của Venom Wallet và thực hiện các thao tác.
    :param page: Đối tượng page từ Playwright.
    :param processed_pages: Danh sách các cửa sổ đã xử lý để tránh xử lý lại.
    """
    try:
        # Chờ trang tải và kiểm tra tiêu đề
        page.wait_for_load_state("load")
        if "Venom Wallet" in page.title() and page not in processed_pages:
            print("Cửa sổ Venom Wallet đã được bật.")
            processed_pages.append(page)  # Thêm trang vào danh sách đã xử lý

            page.bring_to_front()  # Đưa cửa sổ lên trước

            # Chờ trường nhập mật khẩu sẵn sàng
            password_input = page.locator('input[placeholder="Password..."]')
            password_input.wait_for(state="visible", timeout=5000)
            
            # Nhập mật khẩu
            password_input.click()  # Click vào trường trước khi nhập
            password_input.fill("Lam123aa@")  # Nhập mật khẩu vào trường
            print("Đã nhập mật khẩu vào Venom Wallet.")

            # Tìm và click nút "Confirm transaction"
            confirm_button = page.locator('button:has-text("Confirm transaction")')
            confirm_button.wait_for(state="visible", timeout=5000)
            confirm_button.click()
            print("Đã click vào nút Confirm transaction.")
    except Exception as e:
        print(f"Lỗi khi xử lý Venom Wallet: {e}")
