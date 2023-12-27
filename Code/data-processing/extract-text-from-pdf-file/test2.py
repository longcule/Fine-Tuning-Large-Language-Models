import os
def split_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith('.pdf'):
            file_name = os.path.basename(file_path)
            # Lấy phần tên tệp (loại bỏ phần mở rộng)
            pdf_name = os.path.splitext(file_name)[0]
            print(file_path)
            print(pdf_name)

# file_name = os.path.basename(file_path)

# # Lấy phần tên tệp (loại bỏ phần mở rộng)
# pdf_name = os.path.splitext(file_name)[0]
folder_path = './luanvan-pdf'
split_folder(folder_path)