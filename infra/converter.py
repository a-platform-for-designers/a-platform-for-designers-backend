import base64

# Путь к файлу изображения на вашем компьютере
file_path = 'C:\\11.jpeg'

with open(file_path, 'rb') as image_file:
    image_data = image_file.read()

base64_image = base64.b64encode(image_data).decode('utf-8')

print("Строка в формате base64:")
print(base64_image)

#ccc