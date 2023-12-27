import json
import io

# Đọc tệp văn bản và xử lý thành chuỗi JSON
with io.open('data.txt', 'r', encoding='utf-8') as file:
    json_str = '[' + file.read().replace('\n', ',')[:-1] + ']'

# Chuyển chuỗi JSON thành danh sách các phần tử
data = json.loads(json_str)

# Ghi tệp JSON đã cập nhật với mã hóa UTF-8
with io.open('updated_data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(data, ensure_ascii=False))