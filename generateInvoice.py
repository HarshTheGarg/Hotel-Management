"""
Generate and store invoice on the desktop
"""

import datetime  # To specify datatype

from PIL import Image  # To get the dimensions of the logo

from reportlab.pdfgen import canvas  # Creates a blank pdf
# pip install reportlab

from reportlab.pdfbase.pdfmetrics import stringWidth  # To get the length of a string to center it

from reportlab.pdfbase.ttfonts import TTFont  # To use fonts
from reportlab.pdfbase import pdfmetrics  # Makes font compatible with our code

import os  # To Create the Directory


# generate invoice
def generateInvoice(customerId: str, name: str, aadhaar: str, mobile: str, roomType: str,
                    inDate: datetime.date, outDate: datetime.date, rate: int, price: int, tax: float
                    ) -> None:
    """
    Generate the invoice with respective customer's info
    :rtype: None
    """
    # Create the right font
    pdfmetrics.registerFont(TTFont("robotoBlack", "Assets/Roboto/Roboto-Black.ttf"))
    pdfmetrics.registerFont(TTFont("robotoBold", "Assets/Roboto/Roboto-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("robotoRegular", "Assets/Roboto/Roboto-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("robotoThin", "Assets/Roboto/Roboto-Thin.ttf"))
    pdfmetrics.registerFont(TTFont("robotoItalic", "Assets/Roboto/Roboto-Italic.ttf"))

    # Page Information
    page_height = 3508
    page_width = 2000
    margin_top = 150
    margin_sides = 350
    line_space = 100

    # Create the folder on desktop
    directory_path = os.environ["USERPROFILE"] + "\\Desktop\\HotelMan"
    if os.path.exists(directory_path):
        pass
    else:
        os.mkdir(directory_path)

    # Resize the image
    img = Image.open("Assets/LogoBlackNameLarge.png")
    actual_img_width, actual_img_height = img.size
    img_ratio = actual_img_width / actual_img_height

    img_width = 700
    img_height = img_width / img_ratio

    c = canvas.Canvas(directory_path + "\\{}_{}_{}{}{}_{}{}{}.pdf".format(
        customerId, name.replace(" ", "_"),
        str(inDate.year), str(inDate.month), str(inDate.day),
        str(outDate.year), str(outDate.month), str(outDate.day)
    ))

    c.setPageSize((page_width, page_height))

    y_coordinate = page_height - margin_top - img_height
    x_coordinate = margin_sides + 800

    priceFinal = round(int(price) * (1 + float(tax)/100), 2)

    # Logo
    c.drawInlineImage(
        "Assets\\LogoBlackNameLarge.png",
        (page_width - img_width)/2,
        y_coordinate,
        img_width,
        img_height
    )

    y_coordinate -= line_space * 3

    # Invoice Heading
    c.setFont("robotoBlack", 90)
    text = "INVOICE"
    text_width = stringWidth(text, "robotoBlack", 90)
    c.drawString(
        (page_width-text_width)/2,
        y_coordinate,
        text
    )

    # Underline
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(5)
    c.line(
        ((page_width - text_width) / 2) - 3,
        y_coordinate - 8,
        ((page_width + text_width) / 2) + 3,
        y_coordinate - 8
    )

    y_coordinate -= line_space * 2

    # Customer name
    c.setFont("robotoBold", 50)
    text = "Customer's Name: "
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        str(name)
    )

    y_coordinate -= line_space

    # Customer aadhaar
    c.setFont("robotoBold", 50)
    text = "Customer's Aadhaar Number: "
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        str(aadhaar)
    )

    y_coordinate -= line_space

    # Customer mobile
    c.setFont("robotoBold", 50)
    text = "Customer's Contact Number: "
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        "+91 " + str(mobile[0:5]) + "-" + str(mobile[5:10])
    )

    y_coordinate -= line_space*2

    # Customer check In Date
    c.setFont("robotoBold", 50)
    text = "Check In Date: "
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        str(inDate.day) + "-" + str(inDate.month) + "-" + str(inDate.year)
    )

    y_coordinate -= line_space

    # Customer check Out date
    c.setFont("robotoBold", 50)
    text = "Check Out Date: "
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        str(outDate.day) + "-" + str(outDate.month) + "-" + str(outDate.year)
    )

    y_coordinate -= line_space*2

    # Customer roomType
    c.setFont("robotoBold", 50)
    text = "Room: "
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        str(roomType)
    )

    y_coordinate -= line_space

    # Rate
    c.setFont("robotoBold", 50)
    text = "Room Rate: "
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(rate)
    )

    y_coordinate -= line_space

    # Price excl. tax
    c.setFont("robotoBold", 50)
    text = "Price (Tax Excl.): "
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(price)
    )

    y_coordinate -= line_space

    # Tax
    c.setFont("robotoBold", 50)
    text = "Tax: "
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        str(tax)
    )

    y_coordinate -= line_space

    # Total Price
    c.setFont("robotoBold", 50)
    text = "Net Price :"
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(priceFinal)
    )

    y_coordinate -= line_space

    # Round off
    c.setFont("robotoBold", 50)
    text = "Round off:"
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(
            abs(round((priceFinal - round(priceFinal, 0)), 2))
        )
    )

    y_coordinate -= line_space*2

    # Final Value
    c.setFont("robotoBold", 50)
    text = "Total Amount:"
    c.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    c.setFont("robotoItalic", 50)
    c.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(
            round(priceFinal, 0)
        )
    )

    y_coordinate -= line_space * 4.5

    # Notes
    c.setFont("robotoThin", 25)
    text = "Hotel Man: By: Harsh G, Reeshan J, Aditya M"
    text_width = stringWidth(text, "robotoThin", 25)

    c.drawString(
        page_width - text_width - margin_sides,
        y_coordinate,
        text
    )

    y_coordinate -= line_space/2

    c.setFont("robotoThin", 25)
    text = "Contact: 9XXXX-XXXXX"
    text_width = stringWidth(text, "robotoThin", 25)

    c.drawString(
        page_width - text_width - margin_sides,
        y_coordinate,
        text
    )

    c.save()
