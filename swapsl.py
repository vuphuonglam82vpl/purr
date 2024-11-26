def fill_input(page, selector, value, description, index=0):
    """
    Hàm hỗ trợ click và nhập giá trị vào ô input được chỉ định.
    :param page: Đối tượng trang (page) từ Playwright.
    :param selector: Selector của ô input.
    :param value: Giá trị cần nhập vào.
    :param description: Mô tả ô input để ghi log.
    :param index: Chỉ số của ô input cần thao tác (mặc định là 0 - ô đầu tiên).
    """
    try:
        element = page.locator(selector).nth(index)
        if element.is_visible():
            element.click()  # Click vào ô input trước
            print(f"Đã click vào {description} (ô thứ {index + 1}).")
            element.fill(value)  # Nhập giá trị vào ô input
            print(f"Đã nhập giá trị {value} vào {description} (ô thứ {index + 1}).")
        else:
            print(f"{description} (ô thứ {index + 1}) không hiển thị.")
    except Exception as e:
        print(f"Lỗi khi thao tác với {description} (ô thứ {index + 1}): {e}")

def click_button(page, selector, description, index=0):
    """
    Hàm hỗ trợ tìm và click vào nút được chỉ định.
    :param page: Đối tượng trang (page) từ Playwright.
    :param selector: Selector của nút cần click.
    :param description: Mô tả nút để ghi log.
    :param index: Chỉ số của nút cần thao tác (mặc định là 0 - nút đầu tiên).
    """
    try:
        element = page.locator(selector).nth(index)
        if element.is_visible():
            element.click()
            print(f"Đã click vào nút {description} (nút thứ {index + 1}).")
        else:
            print(f"Nút {description} (nút thứ {index + 1}) không hiển thị.")
    except Exception as e:
        print(f"Lỗi khi click vào nút {description} (nút thứ {index + 1}): {e}")

def swapsl(page):
    """
    Chức năng tự động thao tác trên trang Swap:
    1. Click và nhập giá trị vào ô input đầu tiên.
    2. Click vào nút Swap đầu tiên.
    3. Click vào nút Confirm.
    :param page: Đối tượng trang (page) từ Playwright.
    """
    # Bước 1: Click và nhập giá trị vào ô input đầu tiên
    fill_input(page, 'input[type="text"][placeholder="0"]', '500', 'ô input đầu tiên', index=0)

    # Bước 2: Click vào nút Swap đầu tiên
    click_button(page, 'button.swap-submit-button', 'nút Swap', index=0)

    # Bước 3: Click vào nút Confirm
    click_button(page, 'button.confirm', 'nút Confirm', index=0)
