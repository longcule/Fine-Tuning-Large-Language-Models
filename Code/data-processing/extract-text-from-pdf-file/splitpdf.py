from extract_toc import extract_toc, pdf_to_text
import os

import fitz



def cut_pdf(file_path,pdf_name, start_page, end_page):
    # Mở tệp PDF gốc
    pdf = fitz.open(file_path)

    # Kiểm tra số trang tổng cộng trong tệp PDF
    # num_total_pages = pdf.page_count
    if start_page >= end_page:
        print("Trang bắt đầu phải nhỏ hơn tổng số trang trong tệp PDF.")
        return

    # Tạo một tệp con mới
    output_pdf = fitz.open()

    # Cắt tệp PDF gốc từ trang bắt đầu
    for page in range(start_page, end_page):
        output_pdf.insert_pdf(pdf, from_page=page, to_page=page)

    # Lưu tệp con thành file PDF mới
    folder_path = os.path.join(os.getcwd(), f"./luanvan-split/{pdf_name}")
    if not os.path.exists(folder_path):
        # Tạo thư mục mới nếu chưa tồn tại
        os.mkdir(folder_path)

    output_file_path = f"{folder_path}/{pdf_name}.pdf"
    output_pdf.save(output_file_path, garbage=4, clean=True)

    # Đóng tệp PDF
    pdf.close()

    # In thông báo khi hoàn thành
    print(f"Tệp PDF {pdf_name} đã được cắt thành công từ trang {start_page} đến trang {end_page}.")
    return output_file_path

def split_text_by_sentences(text, keywords):
    split_text = []
    start_index = 0
    for i in range(len(keywords)-1):
        start_keyword = keywords[i]
        end_keyword = keywords[i+1]
        
        start_pos = text.find(start_keyword, start_index)
        end_pos = text.find(end_keyword, start_pos)
        
        if start_pos != -1 and end_pos != -1:
            split_text.append(text[start_pos:end_pos])
            start_index = end_pos

    # Add the remaining portion of the text
    split_text.append(text[start_index:])

    return split_text


def save_text_segments_to_files(pdf_name, text_segments):
    directory = f"./luanvan-split/{pdf_name}/"

    for i, segment in enumerate(text_segments):
        file_path = os.path.join(directory, f"{pdf_name}_{i+1}.txt")
        with open(file_path, "w") as file:
            file.write(segment)




def split_pdf(file_path, pdf_name):
    # print(texts)
    texts = extract_toc(file_path)
    start_page = texts[1] # Trang bắt đầu cắt
    end_page = texts[2]
    path_split = cut_pdf(file_path,pdf_name, start_page, end_page)
    
    text = pdf_to_text(path_split, start_page=1)
    
    text_segments = split_text_by_sentences(str(text), texts[0])
    save_text_segments_to_files(pdf_name, text_segments)
    

# split_pdf(file_path)

def split_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith('.pdf'):
            file_name = os.path.basename(file_path)
            # Lấy phần tên tệp (loại bỏ phần mở rộng)
            pdf_name = os.path.splitext(file_name)[0]
            split_pdf(file_path, pdf_name)


folder_path = './luanvan'  # Đường dẫn tới thư mục chứa các file PDF
split_folder(folder_path)

