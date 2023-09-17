from flask import Flask, render_template, request
import qrcode
from io import BytesIO
from base64 import b64encode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer, RoundedModuleDrawer, CircleModuleDrawer, SquareModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generateQR():

    # Initiate BytesIO stream
    memory = BytesIO()

    # Get data from form
    data = request.form.get('link')

    # Generate QR Code
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)

    # Set QR Code size
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=GappedSquareModuleDrawer())

    img.save(memory, 'PNG')
    memory.seek(0)

    base64_img = "data:image/png;base64," + b64encode(memory.getvalue()).decode('ascii')
    text = "QR Code Generated Successfully!😎"

    return render_template('index.html', data=base64_img, text=text)

if __name__ == '__main__':
    app.run(debug=True)