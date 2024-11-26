def click_button(page, selector, description, index=0):
    """
    Hàm hỗ trợ tìm và click vào nút, có thể chọn nút theo vị trí (index).
    :param page: Đối tượng trang (page) từ Playwright.
    :param selector: Selector của nút cần click.
    :param description: Mô tả nút để ghi log.
    :param index: Vị trí của nút (mặc định là 0 - nút đầu tiên).
    """
    try:
        button = page.locator(selector).nth(index)
        if button.is_visible():
            button.click()
            print(f"Đã click vào nút {description} (vị trí {index + 1}).")
        else:
            print(f"Nút {description} (vị trí {index + 1}) không hiển thị.")
    except Exception as e:
        print(f"Lỗi khi click vào nút {description} (vị trí {index + 1}): {e}")

def swap(page):
    """
    Chức năng tự động click vào nút Swap (đầu tiên), Max, và Confirm trên trang Swap.
    :param page: Đối tượng trang (page) từ Playwright.
    """

    # Click vào nút Max
    click_button(page, 'button.max-button', 'Max', index=0)

    # Click vào nút Swap (đầu tiên)
    click_button(page, 'button.swap-submit-button', 'Swap', index=0)

    # Click vào nút Confirm
    click_button(page, 'button.confirm', 'Confirm', index=0)
