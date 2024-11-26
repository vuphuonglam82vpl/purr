import requests
import json
import time
import datetime
import winsound  # Dành cho Windows
import threading
from ban_url import ban_url_with_profile_and_extension
from mua_url import mua_url_with_profile_and_extension

# Đường dẫn tới tệp config
CONFIG_PATH = "config.json"

def load_config():
    """Tải cấu hình từ tệp JSON."""
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Không tìm thấy tệp {CONFIG_PATH}, sử dụng ngưỡng mặc định.")
        return {"sell_threshold": 0.0000001145, "buy_threshold": 0.0000001115}
    except json.JSONDecodeError:
        print(f"Tệp {CONFIG_PATH} không hợp lệ, kiểm tra lại định dạng JSON.")
        return {"sell_threshold": 0.0000001145, "buy_threshold": 0.0000001115}

def play_alert_sound_once(sound):
    """Phát âm thanh cảnh báo một lần."""
    winsound.PlaySound(sound, winsound.SND_FILENAME)

def check_price():
    """Kiểm tra giá từ API và phát âm thanh nếu vượt ngưỡng."""
    x = '{"ohlcvKind":"Price","timeframe":"D1","poolAddress":"0:e27485a418a227bd24fbecc466f806fba3d08b1ae6629a1b7d32a370313b2788","from":0,"to":0}'
    data = json.loads(x)

    last_action = None  # Lưu hành động cuối cùng
    last_config = {}  # Lưu cấu hình trước đó
    sound_file = "alert.wav"

    while True:
        # Tải cấu hình mới nhất
        config = load_config()
        sell_threshold = config["sell_threshold"]
        buy_threshold = config["buy_threshold"]

        # Kiểm tra xem config có thay đổi không
        if config != last_config:
            print(f"Sử dụng ngưỡng mới - BÁN: {sell_threshold}, MUA: {buy_threshold}")
            last_config = config  # Cập nhật config hiện tại
            last_action = None  # Đặt lại hành động

        now = datetime.datetime.utcnow()
        now_utc7 = now + datetime.timedelta(hours=7)
        today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(hours=7)

        today_midnight_ms = int(today_midnight.timestamp() * 1000)
        now_timestamp_ms = int(now_utc7.timestamp() * 1000)

        data["from"] = today_midnight_ms
        data["to"] = now_timestamp_ms

        try:
            r = requests.post('https://api.web3.world/v2/pools/ohlcv', json=data, timeout=10)
            r.raise_for_status()
            response_json = r.json()

            if response_json:
                first_item = response_json[0]
                close_price = float(first_item["close"])

                print(f"{now_utc7.strftime('%Y-%m-%d %H:%M:%S')}, Giá: {close_price}")

                # Kiểm tra giá trị để phát âm thanh
                if close_price > sell_threshold and last_action != "SELL":
                    print("BÁN PURR! Giá vượt ngưỡng.")
                    threading.Thread(target=play_alert_sound_once, args=(sound_file,)).start()
                    ban_url_with_profile_and_extension()
                    last_action = "SELL"

                elif close_price < buy_threshold and last_action != "BUY":
                    print("MUA PURR! Giá dưới ngưỡng.")
                    threading.Thread(target=play_alert_sound_once, args=(sound_file,)).start()
                    mua_url_with_profile_and_extension()
                    last_action = "BUY"

            else:
                print("Response trống hoặc không có dữ liệu")

        except requests.exceptions.RequestException as e:
            print(f"Đã xảy ra lỗi khi kết nối: {e}")

        except ValueError:
            print("Response không phải là JSON hoặc không hợp lệ:")
            print(r.text)

        # Thời gian chờ trước khi kiểm tra lần tiếp theo
        time.sleep(5)

# Chạy kiểm tra giá
if __name__ == "__main__":
    check_price()
