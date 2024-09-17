from PIL import Image
import base64
import io

def image_to_base64(image_file):
    image = Image.open(image_file)
    buffer = io.BytesIO()
    image.save(buffer, format=image.format)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str





