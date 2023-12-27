import fitz
import re
import docx
import os
def preprocess(text):
    text = text.replace('\n', ' ')
    text = re.sub('\s+', ' ', text)
    return text

def pdf_to_text(path, start_page=1, end_page=None):
    doc = fitz.open(path)
    total_pages = doc.page_count

    if end_page is None:
        end_page = total_pages

    text_list = []

    for i in range(start_page - 1, end_page):
        text = doc.load_page(i).get_text("text")
        text = preprocess(text)
        text = text.replace("!", "")  # Remove exclamation marks
        text = text.replace("Ƣ", "Ư")
        text_list.append(text)

    doc.close()
    return text_list


def docx_to_text(path):
    doc = docx.Document(path)
    text_list = []
    
    for paragraph in doc.paragraphs:
        text = preprocess(paragraph.text)
        text = text.replace("!", "")
        text = text.replace("Ƣ", "Ư")
        text_list.append(text)
    
    return text_list

def txt_to_text(path):
    with open(path, 'r', encoding='utf-8') as file:
        text_list = [preprocess(line.strip()) for line in file]
    
    return text_list

def convert_dot(sentences):
    new_sentences = []
    for sentence in sentences:
        new_sentence = re.sub(r'(\d+\.\d+)(?!\.)', r'\1.', sentence)
        new_sentences.append(new_sentence)
    return new_sentences


def text_to_chunks(texts, word_length=10000, start_page=1):
    text_toks = [t.split(' ') for t in texts]
    chunks = []

    for idx, words in enumerate(text_toks):
        for i in range(0, len(words), word_length):
            chunk = words[i : i + word_length]
            if (
                (i + word_length) > len(words)
                and (len(chunk) < word_length)
                and (len(text_toks) != (idx + 1))
            ):
                text_toks[idx + 1] = chunk + text_toks[idx + 1]
                continue
            chunk = ' '.join(chunk).strip()
            chunk = f'[Page no. {idx+start_page}]' + ' ' + '"' + chunk + '"'
            chunks.append(chunk)
    return chunks

def save_chunks_to_files(chunks):
    for i, chunk in enumerate(chunks):
        filename = f"chunk_{i+1}.txt"  # Tạo tên tệp tin với số thứ tự
        with open(filename, "w") as file:
            file.write(chunk)
            break

def toc(content):
    start_index = content.find('MỞ ĐẦU')
    
    end_index_1 = content.find('TÀI LIỆU THAM KHẢO')
    
    # end_index_2 = content.find('TÀI LIỆU THAM KHẢO')
    end_index_2 = content.lower().find('tài liệu tham khảo')
    
    if start_index != -1:
        if end_index_1 != -1 and end_index_2 != -1:
            end_index = max(end_index_1, end_index_2)
        elif end_index_1 != -1:
            end_index = end_index_1
        elif end_index_2 != -1:
            end_index = end_index_2
        else:
            print("Không tìm thấy từ kết thúc cần trích xuất trong tệp đầu vào.")
            return None

        extracted_text = content[start_index:end_index]      
        return extracted_text
    else:
        print("Không tìm thấy văn bản cần trích xuất trong tệp đầu vào.")
        return None
                

def process_data(data):
    # Tìm các mục và số hiệu trong dữ liệu
    pattern = r'(\d+\.\s*)(.*)'
    matches = re.findall(pattern, data)
    
    # Lưu trữ dữ liệu đã xử lý
    processed_data = []
    stack = []
    
    for match in matches:
        number = match[0]
        title = match[1]
        
        # Tìm số lượng khoảng trắng đầu dòng để xác định mức thụt
        indentation = len(re.findall(r'\s', number))
        
        # Làm sạch tiêu đề bằng cách loại bỏ khoảng trắng và ký tự xuống dòng
        clean_title = title.strip()
        
        # Xác định mức thụt và xây dựng dòng định dạng
        indent = ' ' * 3 * (indentation - 1)
        formatted_line = f'{indent}{number}{clean_title}'
        
        # Xác định mức thụt tiếp theo
        next_indentation = indentation + 1
        
        # Kiểm tra xem mục hiện tại có thụt đầu dòng hay không
        if stack:
            current_indentation = stack[-1][0]
            if next_indentation > current_indentation:
                stack.append((next_indentation, formatted_line))
            else:
                while stack and next_indentation <= stack[-1][0]:
                    previous_indentation, previous_line = stack.pop()
                    processed_data.append(previous_line)
                stack.append((next_indentation, formatted_line))
        else:
            stack.append((next_indentation, formatted_line))
    
    # Xử lý phần tử còn lại trong stack
    while stack:
        indentation, line = stack.pop()
        processed_data.append(line)
    
    return processed_data

def find_matches(pattern, text):
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches


def find_sentence_in_pdf(result, file_path, sentence, end):
    # Mở tệp PDF
    pdf = fitz.open(file_path)
    count = 0
    count2 = 0
    count3 = 0
    load = False
    page_start = 0
    page_end = 0
    # Duyệt qua từng trang
    for page_num in range(pdf.page_count):
        # page = pdf.load_page(page_num)
        text = pdf.load_page(page_num).get_text("text")
        text = preprocess(text)
        text = text.replace("!", "")  # Remove exclamation marks
        text = text.replace("Ƣ", "Ư")
        

        # Tìm câu trong văn bản trang
        if load == False:
            if sentence in text:
                count += 1
                if count == 2:
                    load = True
                    page_start = page_num

        if end not in text:
            new_end = re.sub(r'(\d+\.\d+)(?!\.)', r'\1.', end)
            if new_end in text:
                count3 += 1
                page_end = page_num
                new_result = convert_dot(result)
                return new_result, page_start, page_end
        
            

        if end in text:
            count2 += 1
            if count2 == 2:
                page_end = page_num + 1
                return result, page_start, page_end
        
    # Đóng tệp PDF
    pdf.close()
    


def extract_toc(file_path):

        file_extension = os.path.splitext(file_path)[1]

        if file_extension.lower() == '.pdf':
            # Call the pdf_to_text function
            texts = pdf_to_text(file_path, start_page=1)
        elif file_extension.lower() == '.docx':
            # Call the docx_to_text function
            texts = docx_to_text(file_path)
        elif file_extension.lower() == '.txt':
            # Call the docx_to_text function
            texts = txt_to_text(file_path)
        else:
            print("Unsupported file type. Please provide a PDF or DOCX file.")

        chunks = text_to_chunks(texts, start_page=1)

        save_chunks_to_files(chunks) 
        text = toc(chunks[0])
        
        if text is None:      
            return 'None'

        processed_data = process_data(text)     

        elements = re.split(r'(?<!\.)\b\d+\b(?!\.)', str(processed_data))       
        # Xóa khoảng trắng thừa ở đầu và cuối mỗi phần tử, và loại bỏ chuỗi ".........." ở cuối mỗi dòng
        elements = [element.strip().rstrip('.') for element in elements if element.strip()]
        elements = [item.strip("[]\"'") for item in elements]
        if '' in elements:
            elements.remove('')
        filtered_lines = [line for line in elements if re.match(r'^\d', line)]
        
        result = []
        # In kết quả
        for line in filtered_lines:
            line = re.sub(r'(.*[^\W\d_])(.*)', r'\1', line)
            
            # print(line)
            result.append(line)
        
        sentence = result[0]
        end = result[-1]
        if sentence is None:
            sentence = 10
        
        number = find_sentence_in_pdf(result, file_path, sentence, end)
        return number


