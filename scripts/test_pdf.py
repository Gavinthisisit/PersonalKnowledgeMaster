import fitz  # fitz就是PyMuPDF的别名

# 打开PDF文件
pdf_path = './test_doc.pdf'
pdf_document = fitz.open(pdf_path)

# 遍历PDF的每一页
for page_number in range(len(pdf_document)):
    page = pdf_document.load_page(page_number)
    text = page.get_text()  # 获取页面文本内容
    print(f"Page {page_number + 1}:\n{text}")

# 关闭PDF文档
pdf_document.close()