from PIL import Image, ImageDraw, ImageFont

def draw_blank(image,Dx:int,Dy:int):
    # 设置表格的尺寸和字体
    table_width = 350#1600  # 总宽度，可以根据需要调整
    table_height = 175#800  # 总高度，可以根据需要调整
    cell_x_num = 10
    cell_y_num = 4
    cell_width = int(table_width / cell_x_num)  # 每个单元格的宽度
    cell_height = int(table_height / cell_y_num)  # 每个单元格的高度
    font_size = 25#100  # 字体大小
    border_width = 2#5  # 边框宽度

    # 创建一个白色背景的图像
    table_image = image

    # 准备绘制表格的工具
    draw = ImageDraw.Draw(table_image)

    # 选择一个合适的字体和大小
    # 这里使用默认字体，也可以指定其他字体文件
    font = ImageFont.load_default(font_size)
    small_font = ImageFont.load_default(font_size / 3)

    # 设置数字之间的间隔
    num_spacing = cell_width / 2
    num_left = font_size / -2
    num_top = cell_height / 2 - font_size / 2

    # 绘制表格边框
    draw.rectangle([Dx, Dy, Dx+table_width, Dy+table_height], outline="black", width=border_width)

    # 绘制表格内的线条，分为行和列
    # 列线条
    for x in range(0, table_width, cell_width):
        draw.line([Dx+x, Dy+border_width, Dx+x, Dy+table_height - border_width], fill="black", width=border_width)

    # 行线条
    for y in range(border_width, table_height, cell_height):
        draw.line([Dx+border_width, Dy+y, Dx+table_width - border_width, Dy+y], fill="black", width=border_width)

    # 填充数字到表格中
    pos = ["10", "1", "0.1", "0.01"]
    numbers = '1234567890'
    for i in range(4):
        draw.text((Dx+10, Dy+10 + border_width + i * cell_height), pos[i], font=small_font, fill="black")
        for j, num in enumerate(numbers):
            draw.text((Dx+num_left + cell_width * j + num_spacing, Dy+num_top + border_width + i * cell_height), num,
                      font=font, fill="black")

    return image


# 创建A4纸背景
paper_size = (1240,1754)  # A4纸的尺寸（单位：像素）
paper = Image.new('RGB', paper_size, color=(255, 255, 255))  # 白色背景
top=300

for i in range(7):
    draw_blank(paper,200, top+i*200)
    draw_blank(paper,800, top+i*200)

# 保存图片
paper.save('../resource/normal_card.png')
