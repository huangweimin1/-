from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random
# 定义全局颜色变量
STAMP_COLOR = '#e17362'
Font='仿宋_GB2312.ttf'
class StampGenerator:
    def __init__(self, outer_radius=100, ring_width=7,
                 star_scale=0.35, vertical_offset=15, noise_level=0.09,
                 top_text_size=34,text_top="纽约州纽约市国王县", top_text_rotation=37,top_text_spacing=1, top_text_distance_ratio=0.19,
                 bottom_text_size=19,text_bottom="社区委员会",bottom_text_distance_ratio=0.40,horizontal_letter_spacing=2,
                 draw_bottom_num=True,num_bottom='8812054411',bottom_num_size=10,bottom_num_spacing=3,bottom_num_distance_ratio=0.07,bottom_num_rotation=-90):
        """
        初始化印章生成类
        :param outer_radius: 圆环外半径，单位为像素
        :param ring_width: 圆环的宽度，单位为像素
        :param text_top: 上方圆弧文字
        :param text_bottom: 下方水平文字
        :param star_scale: 五角星相对于圆环的比例（0-1）
        :param vertical_offset: 五角星在垂直方向上的偏移
        :param noise_level: 噪点控制参数（0-1之间），数值越大噪点越多
        :param top_text_size: 上方文字大小
        :param bottom_text_size: 下方文字大小
        :param top_text_spacing: 上方文字的间距
        :param top_text_distance_ratio: 上方文字距离圆心的比例
        :param bottom_text_distance_ratio: 下方文字距离圆心的比例
        :param horizontal_letter_spacing: 水平方向上文字的间距
        :param top_text_rotation: 上方文字整体围绕圆心旋转的角度

        :param draw_bottom_num: 是否绘制底部数字
        :param num_bottom: 下方圆弧数字4115220020315
        :param bottom_num_size:下方数字大小
        :param bottom_num_spacing: 下方数字的间距
        :param bottom_num_distance_ratio: 下方数字距离圆心的比例
        :param bottom_num_rotation: 下方数字整体围绕圆心旋转的角度
        """
        self.outer_radius = outer_radius
        self.ring_width = ring_width
        self.text_top = text_top
        self.text_bottom = text_bottom
        self.star_scale = star_scale
        self.vertical_offset = vertical_offset
        self.noise_level = noise_level
        self.top_text_size = top_text_size  # 上方文字大小
        self.bottom_text_size = bottom_text_size  # 下方文字大小
        self.top_text_spacing = top_text_spacing  # 上方文字的间距
        self.top_text_distance_ratio = top_text_distance_ratio  # 上方文字距离圆心的比例
        self.bottom_text_distance_ratio = bottom_text_distance_ratio  # 下方文字距离圆心的比例
        self.horizontal_letter_spacing = horizontal_letter_spacing  # 水平方向文字的间距
        self.top_text_rotation = top_text_rotation  # 新增参数：上方文字整体旋转角度
        self.image_size = (outer_radius * 2 + 100, outer_radius * 2 + 100)

        #底部数字相关参数
        self.draw_bottom_num=draw_bottom_num
        self.num_bottom=num_bottom
        self.bottom_num_size=bottom_num_size
        self.bottom_num_spacing=bottom_num_spacing
        self.bottom_num_distance_ratio=bottom_num_distance_ratio
        self.bottom_num_rotation=bottom_num_rotation


    def generate_stamp(self):
        # 创建白色背景的图像
        image = Image.new('RGB', self.image_size, (255, 255, 255))
        draw = ImageDraw.Draw(image)
        center = (self.image_size[0] // 2, self.image_size[1] // 2)

        # 绘制红色圆环
        outer_radius = self.outer_radius
        ring_width = self.ring_width
        draw.ellipse(
            (center[0] - outer_radius, center[1] - outer_radius, center[0] + outer_radius, center[1] + outer_radius),
            outline=STAMP_COLOR, width=ring_width)

        # 绘制五角星
        star_center = (center[0], center[1] - int(outer_radius * self.star_scale / 2))  # 五角星中心位置
        self._draw_star(draw, star_center, outer_radius * self.star_scale, self.vertical_offset)

        # 计算上方文字的距离
        top_text_distance = int(outer_radius * self.top_text_distance_ratio)

        # 绘制上方文字（围绕圆环内侧分散排列）
        self._draw_top_text(draw, self.text_top, center, top_text_distance)

        if self.draw_bottom_num:#如果绘制数字
            # 计算下方数字的距离
            bottom_num_distance = int(outer_radius * self.bottom_num_distance_ratio)
            # 绘制上方文字（围绕圆环内侧分散排列）
            self._draw_bottom_num(draw, self.num_bottom, center, bottom_num_distance)

        # 绘制下方水平文字（距离圆心的比例控制）
        bottom_text_distance = int(self.outer_radius * self.bottom_text_distance_ratio)  # 根据比例计算偏移
        self._draw_horizontal_text(draw, self.text_bottom, center, bottom_text_distance)

        # 添加随机噪点
        stamp_np = np.array(image)
        self._apply_noise(stamp_np)
        # 将图像转换回Pillow格式
        stamp_image = Image.fromarray(stamp_np)

        return stamp_image

    def _draw_star(self, draw, center, radius, vertical_offset=0):
        """绘制标准五角星，确保几何中心位于圆心，并可调整其在垂直方向的位置"""
        star_points = []
        for i in range(5):
            outer_angle = 2 * np.pi * i / 5 - np.pi / 2  # 计算外部点的角度，确保顶端朝上
            inner_angle = outer_angle + np.pi / 5  # 计算内部点的角度

            # 计算外部点和内部点的坐标
            outer_x = center[0] + radius * np.cos(outer_angle)
            outer_y = center[1] + radius * np.sin(outer_angle) + vertical_offset  # 应用垂直偏移

            inner_radius = radius / 2.5  # 内部点的半径
            inner_x = center[0] + inner_radius * np.cos(inner_angle)
            inner_y = center[1] + inner_radius * np.sin(inner_angle) + vertical_offset  # 应用垂直偏移

            star_points.append((outer_x, outer_y))
            star_points.append((inner_x, inner_y))

        draw.polygon(star_points, fill=STAMP_COLOR)
    def _draw_top_text(self, draw, text, center, distance_from_center, center_char_index=None):
        text=text[::-1]#逆序字符串，不知道为啥，画出来的顺序是反的
        """绘制上方文字，围绕圆环内侧分散排列，并且可以调整字符间的弧度间距，
           同时确保第一个字和最后一个字在水平上对齐，整个句子在垂直方向上位于圆心"""
        try:
            font = ImageFont.truetype(Font, self.top_text_size)  # 使用指定字体和上方文字大小
        except IOError:
            font = ImageFont.load_default()  # 如果找不到字体则使用默认字体

        # 计算每个字符占用的角度，包括字符本身和间距
        total_angle = 0
        angles = []
        for char in text:
            char_bbox = draw.textbbox((0, 0), char, font=font)
            char_width = char_bbox[2] - char_bbox[0]
            # 字符宽度转换为角度，加上字符间距角度
            char_angle = (char_width / ((self.outer_radius - self.ring_width - distance_from_center) * 2 * np.pi)) * 360
            angles.append(char_angle)
            total_angle += char_angle + self.top_text_spacing  # 增加字符间距角度

        # 减去最后一个字符的额外间距
        total_angle -= self.top_text_spacing

        # 计算每个字符的实际角度
        angle_per_char = total_angle / len(text)

        # 计算整个字符串的起始角度，确保第一个字符和最后一个字符在水平方向上对齐
        if center_char_index is None:
            center_char_index = len(text) // 2  # 默认以中间字符为中心

        # 计算中心字符的总角度偏移量
        center_angle_offset = sum(angles[:center_char_index]) + (center_char_index * self.top_text_spacing)

        # 计算整个字符串的起始角度，确保第一个字符和最后一个字符在水平方向上对齐
        start_angle = -30 - (total_angle / 2) + (center_angle_offset - angles[center_char_index] / 2)

        # 添加整体旋转角度
        start_angle += self.top_text_rotation

        # 绘制每个字符
        for i, char in enumerate(text):
            # 计算当前字符的位置角度
            angle = start_angle + i * angle_per_char
            x = center[0] + (self.outer_radius - self.ring_width - distance_from_center) * np.cos(np.radians(angle))
            y = center[1] - (self.outer_radius - self.ring_width - distance_from_center) * np.sin(np.radians(angle))

            # 调整旋转角度，使文字沿着圆弧方向对齐
            angle_degrees = angle - 90
            draw.text((x, y), char, font=font, fill=STAMP_COLOR, anchor="mm")
    def _draw_bottom_num(self, draw, text, center, distance_from_center, center_char_index=None):

        """绘制下方数字，与绘制上方文字完全相同，围绕圆环内侧分散排列，并且可以调整字符间的弧度间距，
           同时确保第一个字和最后一个字在水平上对齐，整个句子在垂直方向上位于圆心"""
        try:
            font = ImageFont.truetype(Font, self.bottom_num_size)  # 使用指定字体和上方文字大小
        except IOError:
            font = ImageFont.load_default()  # 如果找不到字体则使用默认字体

        # 计算每个字符占用的角度，包括字符本身和间距
        total_angle = 0
        angles = []
        for char in text:
            char_bbox = draw.textbbox((0, 0), char, font=font)
            char_width = char_bbox[2] - char_bbox[0]
            # 字符宽度转换为角度，加上字符间距角度
            char_angle = (char_width / ((self.outer_radius - self.ring_width - distance_from_center) * 2 * np.pi)) * 360
            angles.append(char_angle)
            total_angle += char_angle + self.bottom_num_spacing  # 增加字符间距角度

        # 减去最后一个字符的额外间距
        total_angle -= self.bottom_num_spacing

        # 计算每个字符的实际角度
        angle_per_char = total_angle / len(text)

        # 计算整个字符串的起始角度，确保第一个字符和最后一个字符在水平方向上对齐
        if center_char_index is None:
            center_char_index = len(text) // 2  # 默认以中间字符为中心

        # 计算中心字符的总角度偏移量
        center_angle_offset = sum(angles[:center_char_index]) + (center_char_index * self.bottom_num_spacing)

        # 计算整个字符串的起始角度，确保第一个字符和最后一个字符在水平方向上对齐
        start_angle = -30 - (total_angle / 2) + (center_angle_offset - angles[center_char_index] / 2)

        # 添加整体旋转角度
        start_angle += self.bottom_num_rotation

        # 绘制每个字符
        for i, char in enumerate(text):
            # 计算当前字符的位置角度
            angle = start_angle + i * angle_per_char
            x = center[0] + (self.outer_radius - self.ring_width - distance_from_center) * np.cos(np.radians(angle))
            y = center[1] - (self.outer_radius - self.ring_width - distance_from_center) * np.sin(np.radians(angle))

            # 调整旋转角度，使文字沿着圆弧方向对齐
            angle_degrees = angle - 90
            draw.text((x, y), char, font=font, fill=STAMP_COLOR, anchor="mm")

    def _draw_horizontal_text(self, draw, text, center, y_offset):
        """绘制水平文字"""
        try:
            font = ImageFont.truetype(Font, self.bottom_text_size)  # 使用指定字体和下方文字大小
        except IOError:
            font = ImageFont.load_default()

        # 计算整个文本的宽度（考虑水平间距）
        text_width = 0
        for char in text:
            char_bbox = draw.textbbox((0, 0), char, font=font)  # 获取字符的边界框
            char_width = char_bbox[2] - char_bbox[0]  # 计算字符的宽度
            text_width += char_width + self.horizontal_letter_spacing  # 加上每个字符的宽度和间距

        # 去掉最后一个字符的间距
        text_width -= self.horizontal_letter_spacing

        # 计算文本的起始位置
        text_position = (center[0] - text_width // 2, center[1] + y_offset)

        # 在画布上绘制文本
        for char in text:
            draw.text(text_position, char, font=font, fill=STAMP_COLOR)
            char_bbox = draw.textbbox((0, 0), char, font=font)  # 获取字符的边界框
            char_width = char_bbox[2] - char_bbox[0]  # 计算字符的宽度
            text_position = (text_position[0] + char_width + self.horizontal_letter_spacing, text_position[1])

    def _apply_noise(self, img_np):
        """给图像应用随机白色噪点"""
        noise_amount = int(self.noise_level * img_np.size // 3)
        for _ in range(noise_amount):
            x = random.randint(0, img_np.shape[1] - 1)
            y = random.randint(0, img_np.shape[0] - 1)
            img_np[y, x] = 255  # 将该位置设置为白色噪点
# 使用示例
stamp_generator = StampGenerator()  #均使用默认参数
stamp_image = stamp_generator.generate_stamp()
#stamp_image.show()  # 显示印章
#stamp_image.save('stamp_with_star_and_text_v13.png')  # 保存印章