import pdfplumber


x0 = 0
top = 5
x1 = 100
bottom = 95
crop_coords = [x0, top, x1, bottom]

# Open the PDF file
with pdfplumber.open("data/1.pdf") as pdf:

    # Iterate through all pages
    

    text = ''
    pages = []
    for i, page in enumerate(pdf.pages):
        my_width = page.width
        my_height = page.height
        # Crop pages
        my_bbox = (crop_coords[0]*float(my_width), crop_coords[1]*float(my_height), crop_coords[2]*float(my_width), crop_coords[3]*float(my_height))
        page_crop = page.crop(bbox=my_bbox)
        text = text+str(page_crop.extract_text()).lower()
        pages.append(page_crop)

    all_pages = pages
    first_page = all_pages[0]
    last_page = all_pages[len(all_pages) - 1]
    all_pages = all_pages[1:len(all_pages) - 1]


    for page in all_pages:
        # print(type(pdf.pages))
        # Extract text from the page
        text = page.extract_text()
        print(text)