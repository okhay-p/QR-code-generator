from flask import Flask, render_template, request
import qrcode
from io import BytesIO
from base64 import b64encode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    RoundedModuleDrawer,
    CircleModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def generateQR():
    # Initiate BytesIO stream
    memory = BytesIO()

    # Get data from form
    data = request.form.get("link")

    # Get design selection from form
    design = request.form.get("design")

    # Generate QR Code
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)

    # Set QR Code size
    qr.make(fit=True)

    # Create an image from the QR Code instance
    if design == "design-1":
        img = qr.make_image(
            image_factory=StyledPilImage, module_drawer=SquareModuleDrawer()
        )
    elif design == "design-2":
        img = qr.make_image(
            image_factory=StyledPilImage, module_drawer=GappedSquareModuleDrawer()
        )
    elif design == "design-3":
        img = qr.make_image(
            image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()
        )
    elif design == "design-4":
        img = qr.make_image(
            image_factory=StyledPilImage, module_drawer=CircleModuleDrawer()
        )
    elif design == "design-5":
        img = qr.make_image(
            image_factory=StyledPilImage, module_drawer=VerticalBarsDrawer()
        )
    elif design == "design-6":
        img = qr.make_image(
            image_factory=StyledPilImage, module_drawer=HorizontalBarsDrawer()
        )


    img.save(memory, "PNG")
    memory.seek(0)

    base64_img = "data:image/png;base64," + b64encode(memory.getvalue()).decode("ascii")
    text = f"QR code generated successfully for {data}!🥳"
    selected = "Design Selected: " + design

    return render_template("index.html", qr_img=base64_img, text=text)


if __name__ == "__main__":
    app.run(debug=True)
