import requests
import json
from urllib.parse import urlencode

# URL cơ bản của API Sendo
base_url = "https://searchlist-api.sendo.vn/web/products"

# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.sendo.vn/",
    "Origin": "https://www.sendo.vn",
    "X-Requested-With": "XMLHttpRequest"
}

# Danh sách từ khóa danh mục sản phẩm
# keywords = ["may-co-khi-va-che-tao,trang-tri-ban","set-trang-phuc","quan-shorts-nam","bep-dien-am-dun","tro-choi","sim-card-dung-cu-chuyen-doi-sim","kinh-mat-nam"]

# Các danh mục sản phẩm cơ bản
categories = [
    "smartphone", "laptop", "tai nghe", "tủ lạnh", "máy giặt", 
    "máy lạnh", "nồi chiên không dầu", "bếp điện", "loa bluetooth", 
    "đèn trang trí", "chăn ga gối đệm", "giày thể thao", "váy", 
    "túi xách", "nước hoa", "kem dưỡng da", "thực phẩm chức năng"
]

# Các thương hiệu hoặc từ khóa bổ sung
brands = [
    "samsung", "apple", "xiaomi", "asus", "dell", "sony", "panasonic", 
    "lg", "philips", "toshiba", "realme", "oppo", "vivo", "hp", "lenovo"
]

# Các thuộc tính bổ sung
attributes = [
    "giá rẻ", "cao cấp", "tốt nhất", "mới nhất", "giảm giá", "hàng mới", 
    "hàng chính hãng", "giá ưu đãi", "trả góp"
]


keywords = []
for category in categories:
    for brand in brands:
        for attribute in attributes:
            keywords.append(f"{category} {brand} {attribute}")
            if len(keywords) >= 1000:  # Dừng khi đủ 1,000 từ khóa
                break
        if len(keywords) >= 1000:
            break
    if len(keywords) >= 1000:
        break
  
# Hàm thu thập sản phẩm từ một từ khóa
def collect_products(keyword):
    page = 1  # Bắt đầu từ trang đầu tiên
    total_products_collected = 0
    all_products = []  # Danh sách để lưu tất cả sản phẩm

    print(f"--- Đang thu thập sản phẩm cho từ khóa: {keyword} ---")

    while True:
        # Tham số yêu cầu
        params = {
            "q": keyword,
            "redirect": 1,
            "platform": "web",
            "page": page,
            "size": 60,  # Số sản phẩm trên mỗi trang
            "sortType": "vasup_desc",
            "search_type": "",
            "app_ver": "2.43.0",
            "track_id": "fa93d7d6-89ab-4fe2-b962-a1e8a7c33c41"
        }

        # Gửi yêu cầu GET tới API
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                products = data.get("data") or data.get("async_data", {}).get("products", [])
                total_products = len(products)  # Tổng số sản phẩm trong trang hiện tại

                if total_products == 0:  # Không còn sản phẩm nào để lấy
                    print(f"Không tìm thấy sản phẩm nào trên trang {page}. Dừng lặp.")
                    break

                # Thêm sản phẩm vào danh sách tổng
                all_products.extend(products)
                total_products_collected += total_products

                print(f"Trang {page}: Đã thu thập {total_products} sản phẩm.")
                page += 1  # Tăng trang lên để lấy dữ liệu tiếp theo
            except Exception as e:
                print(f"Lỗi khi phân tích JSON trên trang {page}: {e}")
                print("Nội dung phản hồi:", response.text)
                break
        else:
            print(f"Lỗi: Server trả về mã trạng thái {response.status_code} trên trang {page}")
            print("Nội dung phản hồi:", response.text)
            break

    # Lưu tất cả sản phẩm vào một tệp JSON duy nhất
    if total_products_collected != 0:
        file_name = f"sendo_{keyword.replace(' ', '_')}_{total_products_collected}.json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump({"total_products": total_products_collected, "products": all_products}, f, ensure_ascii=False, indent=4)
        print(f"--- Đã thu thập tổng cộng {total_products_collected} sản phẩm cho từ khóa '{keyword}' và lưu vào {file_name} ---")

# Lặp qua danh sách từ khóa
for keyword in keywords:
    collect_products(keyword)
