import xlrd

def load_xls(filename):
    # 打开文件
    workbook = xlrd.open_workbook(filename)
    # 遍历所有工作表
    content = ""
    for sheet_name in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheet_name)
        # print(f"工作表: {sheet_name}")

        # 遍历工作表中的所有行
        for row_idx in range(sheet.nrows):
            # 获取当前行的所有单元格数据
            row = sheet.row_values(row_idx)
            tmp_content = ""
            for x in row:
                tmp_content += "%s " % x
            content += tmp_content + "\n"
    # 关闭文件
    workbook.release_resources()
    # print(content)
    return content

# load_xls("./交易所证券余额核对_20231228_中国人寿养老有限公司.xls")