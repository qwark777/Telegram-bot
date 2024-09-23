from PIL import Image
filename = "leha.jpg"
with Image.open(filename) as img:
    img.load()
    img.show()