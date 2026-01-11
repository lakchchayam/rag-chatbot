from pypdf import PdfWriter

writer = PdfWriter()
writer.add_blank_page(width=72, height=72)

with open("test_upload.pdf", "wb") as f:
    writer.write(f)

print("Created test_upload.pdf")
