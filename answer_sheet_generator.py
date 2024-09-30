import time

import qrcode
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import imutils
from imutils.perspective import four_point_transform

class answer_sheet_generator:
    def __init__(self):
        self.font_path = "resource/文泉驿正黑体wqy-zenhei.ttc"
        self.font_size = 25
        self.original_photo = "resource/normal_card.png"
        self.QR_version = 1
        self.top = 300
        self.column1 = 25
        self.interval = 100
        self.column2 = 575
        self.QR_Size = 150
        self.QR_x = 100
        self.QR_y = 100
        self.Threshold_value=500#低于此限度的空识别为未填

    def make(self, Race_Name: str, QR: str, text: str, List: list):
        original = Image.open(self.original_photo)
        draw = ImageDraw.Draw(original)

        def draw_text(text: str, x, y, Front_Size=self.font_size):
            Front = ImageFont.truetype(self.font_path, Front_Size)
            text_position = (x, y)
            draw.text(text_position, text, font=Front, fill="black")  # 填充颜色为黑色

        if len(List) <= 7:
            for i in range(len(List)):
                draw_text(List[i]["Class"], self.column1, self.top + i * 200)
                draw_text(List[i]["Name"], self.column1 + self.interval, self.top + i * 200)
        else:
            for i in range(7):
                draw_text(List[i]["Class"], self.column1, self.top + i * 200)
                draw_text(List[i]["Name"], self.column1 + self.interval, self.top + i * 200)
            for i in range(7, len(List)):
                draw_text(List[i]["Class"], self.column2, self.top + (i - 7) * 200)
                draw_text(List[i]["Name"], self.column2 + self.interval, self.top + (i - 7) * 200)

        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(QR)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        img_qr = img_qr.resize((self.QR_Size, self.QR_Size))
        original.paste(img_qr, (self.QR_x, self.QR_y))
        draw_text(text, self.QR_x, self.QR_y + self.QR_Size)
        draw_text(Race_Name, 300, 100, 100)
        out=Image.new("RGBA", (1240, 1754), (255, 255, 255))
        out.paste(original.resize((1240-20, 1754-20)),(10,10))
        draw_out=ImageDraw.Draw(out)
        draw_out.rectangle([10, 10, 1240-10, 1754-10], outline="black", width=5)
        out.save("Temp/a.png")

    def where_is_my_QR(self,path:str,test:bool=False):
        #致敬 MC mod "Where Is It"-https://www.mcmod.cn/class/7565.html
        #致敬 MC mod "Where Is My Stuff"-https://www.mcmod.cn/class/6648.html
        # 读取图片
        image = cv2.imread(path)
        # 检查图片是否正确读取
        if image is None:
            print("图片未找到，请检查路径是否正确。")
        else:
            # 转换为灰度图像
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # 高斯滤波
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            # 自适应二值化
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 2)
            edged = cv2.Canny(thresh, 75, 100)
            # 从边缘图中寻找轮廓，然后初始化答题卡对应的轮廓
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[1] if imutils.is_cv3() else cnts[0]
            docCnt = None
            # 确保至少有一个轮廓被找到
            if len(cnts) > 0:
                # 将轮廓按大小降序排序
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
                # 对排序后的轮廓循环处理
                for c in cnts:
                    # 获取近似的轮廓
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                    # 如果我们的近似轮廓有四个顶点，那么就认为找到了答题卡
                    if len(approx) == 4:
                        docCnt = approx
                        break
            else:
                print("not find!")
            # 对原始图像和灰度图都进行四点透视变换
            paper=four_point_transform(image, docCnt.reshape(4, 2))
            cv2.resize(paper,(1240,1754))
            paper=paper[100:300,100:300]
            if test:cv2.imshow("QR_Area",paper)
            if test:cv2.imwrite("Temp/QR_Area.jpg",paper)
            if test:cv2.waitKey(5000)
            if test:cv2.destroyAllWindows()
            ### 使用微信识别二维码 需安装 opencv-contrib-python~=4.9.0.80
            detector = cv2.wechat_qrcode_WeChatQRCode()
            res, points = detector.detectAndDecode(paper)
            return res[0]

    def recognition_4(self, path: str, test=False):
        ShowSize=(256,512)
        def show(image):
            return cv2.resize(image,ShowSize)
        # 读取图片
        image = cv2.imread(path)
        #image=cv2.resize(image,(512,1080))
        if test:cv2.imshow('image', show(image))
        # 检查图片是否正确读取
        if image is None:
            print("图片未找到，请检查路径是否正确。")
        else:
            # 转换为灰度图像
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if test:cv2.imshow('gray', show(gray))
            if test:cv2.imwrite('Temp/1gray.jpg', gray)

            # 高斯滤波
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            if test:cv2.imshow('blurred', show(blurred))
            if test:cv2.imwrite('Temp/2blurred.jpg', blurred)

            # 自适应二值化
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 2)
            if test:cv2.imshow('thresh', show(thresh))
            if test: cv2.imwrite('Temp/3thresh.jpg', thresh)
            edged = cv2.Canny(thresh, 75, 100)
            if test:cv2.imshow('edged', show(edged))
            if test: cv2.imwrite('Temp/4edged.jpg', edged)
            # 从边缘图中寻找轮廓，然后初始化答题卡对应的轮廓
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            cnts = cnts[1] if imutils.is_cv3() else cnts[0]
            if test:cv2.imshow('cnts', show(cv2.drawContours(image.copy(), cnts, -1, (0, 255, 0), 2)))
            if test: cv2.imwrite('Temp/5cnts.jpg', cv2.drawContours(image.copy(), cnts, -1, (0, 255, 0), 2))
            docCnt = None

            # 确保至少有一个轮廓被找到
            if len(cnts) > 0:
                # 将轮廓按大小降序排序
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
                # 对排序后的轮廓循环处理
                for c in cnts:
                    # 获取近似的轮廓
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                    # 如果我们的近似轮廓有四个顶点，那么就认为找到了答题卡
                    if len(approx) == 4:
                        docCnt = approx
                        if test:cv2.imshow('find', show(cv2.drawContours(image, [docCnt], -1, (0, 255, 0), 5)))
                        if test: cv2.imwrite('Temp/6find.jpg', cv2.drawContours(image, [docCnt], -1, (0, 255, 0), 5))
                        break
            else:
                print("not find!")
            # 对原始图像和灰度图都进行四点透视变换
            if test:paper = four_point_transform(image, docCnt.reshape(4, 2))
            warped = four_point_transform(gray, docCnt.reshape(4, 2))
            if test:paper = cv2.resize(paper,(1240,1754))
            warped = cv2.resize(warped,(1240,1754))
            if test:cv2.imshow('paper', show(paper))
            if test:cv2.imwrite('Temp/7paper.jpg', paper)
            # 对灰度图应用大津二值化算法
            out = cv2.threshold(warped, 0, 255,
                                   cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            if test:draw = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
            if test:cv2.imshow('out', show(out))
            if test:cv2.imwrite('Temp/8out.jpg', out)
            table_width = 350#1600  # 总宽度，可以根据需要调整
            table_height = 175#800  # 总高度，可以根据需要调整
            cell_x_num = 10
            cell_y_num = 4
            cell_width = int(table_width / cell_x_num)  # 每个单元格的宽度
            cell_height = int(table_height / cell_y_num)  # 每个单元格的高度
            C1=200
            C2=800
            top=300
            Height=200
            answer=[]
            #i，j，k，m，n，p，q
            for m in [C1,C2]:
                # 遍历每一排
                for k in range(7):
                    darkest_block =[]
                    for i in range(4):
                        # 初始化一个列表，用于存储当前排的方块的黑色像素数量
                        black_pixel_counts = []
                        # 遍历每一排的每个方块
                        for j in range(10):
                            x1=m+cell_width*j
                            y1=top+cell_height*i+k*Height
                            x2=x1+cell_width
                            y2=y1+cell_height
                            # 获取当前方块的像素值
                            block_pixels = out[y1:y2,x1:x2]
                            #cv2.imwrite(f'Temp/{x1}-{x2} {y1}-{y2}.jpg', block_pixels)
                            if test:draw=cv2.rectangle(draw, (x1,y1), (x2,y2), (0, 255, 0), 2)
                            # 计算当前方块的白色像素数量
                            black_pixel_count = np.sum(block_pixels == 255)
                            # 将当前方块的白色像素数量添加到列表中
                            black_pixel_counts.append(black_pixel_count)
                        # 找出当前排白色像素数量最多的方块的索引
                        if test:print(black_pixel_counts)
                        max_index = np.argmax(black_pixel_counts)
                        if black_pixel_counts[max_index]<self.Threshold_value:
                            darkest_block.append("?")
                        else:
                            if max_index==9: max_index=-1
                            # 将当前排最黑的方块的编号添加到字典中
                            darkest_block.append(max_index + 1)
                    # 打印结果
                    if test:print(darkest_block)
                    answer.append(darkest_block)
            if test:cv2.imshow('finally', show(draw))
            if test:cv2.imwrite('Temp/9finally.jpg', draw)
            if test:cv2.waitKey(5000)
            if test:cv2.destroyAllWindows()
            return answer
if __name__ == "__main__":
    answer_sheet_generator = answer_sheet_generator()
    QR = "114514"
    data = [{"Class": "912", "Name": "JUNU"}, {"Class": "912", "Name": "JUNU"}, {"Class": "912", "Name": "JUNU"},
            {"Class": "912", "Name": "JUNU"}, {"Class": "912", "Name": "JUNU"}, {"Class": "912", "Name": "JUNU"},
            {"Class": "912", "Name": "JUNU"}, {"Class": "912", "Name": "JUNU"}]
    #answer_sheet_generator.make("九年级男子实心球", QR + " 这是您的场次编号，如果您无法登录系统，请将答题卡送至登分处","No. " + QR, data)
    print("您正在扫描的场次编号为：",str(answer_sheet_generator.where_is_my_QR("test.jpg",test=False)).split(" ")[0])
    need=answer_sheet_generator.recognition_4("test.jpg",test=False)
    for i in range(len(need)):
        print(f"第{i+1}位空： {need[i][0]}{need[i][1]}.{need[i][2]}{need[i][3]}")