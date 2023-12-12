import base64

# Путь к файлу изображения на вашем компьютере
file_path = 'C:\\11.jpeg'  # Используйте двойные обратные слеши

# Открытие файла изображения в бинарном режиме и чтение его содержимого
with open(file_path, 'rb') as image_file:
    image_data = image_file.read()

# Кодирование данных изображения в строку base64
base64_image = base64.b64encode(image_data).decode('utf-8')

print("Строка в формате base64:")
print(base64_image)
