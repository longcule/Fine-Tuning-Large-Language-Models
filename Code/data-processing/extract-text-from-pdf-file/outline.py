input_file = 'chunk_1.txt'
output_file = 'output.txt'

with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()



start_index = content.find('MỞ ĐẦU')
end_index = content.find('TÀI ', start_index + 1)

if start_index != -1 and end_index != -1:
    extracted_text = content[start_index:end_index]
        
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(extracted_text)
        print("Đã tạo thành công tệp văn bản mới.")
else:
    print("Không tìm thấy văn bản cần trích xuất trong tệp đầu vào.")


