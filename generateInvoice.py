"""
Generate and store invoice on the desktop
"""

import datetime  # To specify datatype

from PIL import Image  # To get the dimensions of the logo

# pip install reportlab
from reportlab.pdfgen import canvas  # Creates a blank pdf

from reportlab.pdfbase.pdfmetrics import stringWidth  # To get the length of a string to center it

from reportlab.pdfbase.ttfonts import TTFont  # To use fonts
from reportlab.pdfbase import pdfmetrics  # Makes font compatible with our code

import os  # To Create the Directory


def generateInvoice(customerId: str, name: str, aadhaar: str, mobile: str, roomType: str,
                    inDate: datetime.date, outDate: datetime.date, rate: int, price: int, tax: float
                    ) -> None:
    """
    Generate the invoice with respective customer's info
    :rtype: None
    """

    # Create the font compatible for pdf
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

    page = canvas.Canvas(
        directory_path +
        f"\\{customerId}_{name.replace(' ', '_')}_"
        f"{str(inDate.year)}{inDate.month}{inDate.day}_"
        f"{outDate.year}{outDate.month}{outDate.day}.pdf"
    )

    page.setPageSize((page_width, page_height))

    # To draw the elements at the required location, coordinates start from lower left side of page
    y_coordinate = page_height - margin_top - img_height
    x_coordinate = margin_sides + 800

    # Price including the tax
    priceFinal = round(int(price) * (1 + float(tax)/100), 2)

    # Logo
    page.drawInlineImage(
        "Assets\\LogoBlackNameLarge.png",
        (page_width - img_width)/2,
        y_coordinate,
        img_width,
        img_height
    )

    # Reducing the y coordinate as we have to go down for every element
    y_coordinate -= line_space * 3

    # Invoice Heading
    page.setFont("robotoBlack", 90)
    text = "INVOICE"
    text_width = stringWidth(text, "robotoBlack", 90)
    page.drawString(
        (page_width-text_width)/2,
        y_coordinate,
        text
    )

    # Underline
    page.setStrokeColorRGB(0, 0, 0)
    page.setLineWidth(5)
    page.line(
        ((page_width - text_width) / 2) - 3,
        y_coordinate - 8,
        ((page_width + text_width) / 2) + 3,
        y_coordinate - 8
    )

    y_coordinate -= line_space * 2

    # Customer name
    page.setFont("robotoBold", 50)
    text = "Customer's Name: "
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        str(name)
    )

    y_coordinate -= line_space

    # Customer aadhaar
    page.setFont("robotoBold", 50)
    text = "Customer's Aadhaar Number: "
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        str(aadhaar)
    )

    y_coordinate -= line_space

    # Customer mobile
    page.setFont("robotoBold", 50)
    text = "Customer's Contact Number: "
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        "+91 " + str(mobile[0:5]) + "-" + str(mobile[5:10])
    )

    y_coordinate -= line_space*2

    # Customer check In Date
    page.setFont("robotoBold", 50)
    text = "Check In Date: "
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        str(inDate.day) + "-" + str(inDate.month) + "-" + str(inDate.year)
    )

    y_coordinate -= line_space

    # Customer check Out date
    page.setFont("robotoBold", 50)
    text = "Check Out Date: "
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        str(outDate.day) + "-" + str(outDate.month) + "-" + str(outDate.year)
    )

    y_coordinate -= line_space*2

    # Customer roomType
    page.setFont("robotoBold", 50)
    text = "Room: "
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        str(roomType)
    )

    y_coordinate -= line_space

    # Rate
    page.setFont("robotoBold", 50)
    text = "Room Rate: "
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(rate)
    )

    y_coordinate -= line_space

    # Price excl. tax
    page.setFont("robotoBold", 50)
    text = "Price (Tax Excl.): "
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(price)
    )

    y_coordinate -= line_space

    # Tax
    page.setFont("robotoBold", 50)
    text = "Tax: "
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        str(tax)
    )

    y_coordinate -= line_space

    # Total Price
    page.setFont("robotoBold", 50)
    text = "Net Price :"
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(priceFinal)
    )

    y_coordinate -= line_space

    # Round off
    page.setFont("robotoBold", 50)
    text = "Round off:"
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(
            abs(round((priceFinal - round(priceFinal, 0)), 2))
        )
    )

    y_coordinate -= line_space*2

    # Final Value
    page.setFont("robotoBold", 50)
    text = "Total Amount:"
    page.drawString(
        margin_sides,
        y_coordinate,
        text
    )

    page.setFont("robotoItalic", 50)
    page.drawString(
        x_coordinate,
        y_coordinate,
        "\u20B9" + str(
            round(priceFinal, 0)
        )
    )

    y_coordinate -= line_space * 4.5

    # Footnotes
    page.setFont("robotoThin", 25)
    text = "Hotel Man: By: Harsh G, Reeshan J, Aditya M"
    text_width = stringWidth(text, "robotoThin", 25)

    page.drawString(
        page_width - text_width - margin_sides,
        y_coordinate,
        text
    )

    y_coordinate -= line_space/2

    page.setFont("robotoThin", 25)
    text = "Contact: 9XXXX-XXXXX"
    text_width = stringWidth(text, "robotoThin", 25)

    page.drawString(
        page_width - text_width - margin_sides,
        y_coordinate,
        text
    )

    # Saving the page
    page.save()
