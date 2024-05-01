def convert_to_single_line(input_file, output_file):
    # خواندن محتوای فایل
    with open(input_file, 'r') as file:
        content = file.read().replace('\n', '')

    # نوشتن محتوای فایل تبدیل شده به فایل جدید
    with open(output_file, 'w') as file:
        file.write(content)

# تبدیل فایل JWT_PRIVATE_KEY.pem به تک‌خطی و ذخیره در JWT_PRIVATE_KEY.txt
convert_to_single_line('JWT_PRIVATE_KEY.pem', 'JWT_PRIVATE_KEY.txt')

# تبدیل فایل JWT_PUBLIC_KEY.pem به تک‌خطی و ذخیره در JWT_PUBLIC_KEY.txt
convert_to_single_line('JWT_PUBLIC_KEY.pem', 'JWT_PUBLIC_KEY.txt')
