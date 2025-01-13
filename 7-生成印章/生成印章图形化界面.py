import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
import random
from 超分辨率处理 import super_resolution
from 生成印章 import StampGenerator

class StampApp:
    def __init__(self, root):
        self.root = root
        self.root.title("印章生成器")
        self.generator = StampGenerator()

        self.create_widgets()
        self.current_stamp_image = None  # 存储当前的印章图片
        self.update_preview()  # 初始化时生成初始图片

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 外圆半径
        self.outer_radius_var = tk.IntVar(value=self.generator.outer_radius)
        ttk.Label(frame, text="外圆半径:").grid(column=0, row=0, sticky=tk.W)
        tk.Scale(frame, from_=50, to=150, variable=self.outer_radius_var, orient=tk.HORIZONTAL, command=self.update_preview).grid(column=1, row=0, sticky=tk.W)

        # 圆环宽度
        self.ring_width_var = tk.IntVar(value=self.generator.ring_width)
        ttk.Label(frame, text="圆环宽度:").grid(column=0, row=1, sticky=tk.W)
        tk.Scale(frame, from_=1, to=20, variable=self.ring_width_var, orient=tk.HORIZONTAL, command=self.update_preview).grid(column=1, row=1, sticky=tk.W)

        # 上方文字
        self.text_top_var = tk.StringVar(value=self.generator.text_top)
        ttk.Label(frame, text="上方文字:").grid(column=0, row=2, sticky=tk.W)
        entry_top = ttk.Entry(frame, textvariable=self.text_top_var)#这里没有使用链式调用，感觉使用链式调用可能会更清晰
        entry_top.grid(column=1, row=2, sticky=tk.W)
        entry_top.bind('<KeyRelease>', self.update_preview)  # 绑定事件

        # 下方文字
        self.text_bottom_var = tk.StringVar(value=self.generator.text_bottom)
        ttk.Label(frame, text="下方文字:").grid(column=0, row=3, sticky=tk.W)
        entry_bottom = ttk.Entry(frame, textvariable=self.text_bottom_var)
        entry_bottom.grid(column=1, row=3, sticky=tk.W)
        entry_bottom.bind('<KeyRelease>', self.update_preview)  # 绑定事件

        # 五角星比例
        self.star_scale_var = tk.DoubleVar(value=self.generator.star_scale)
        ttk.Label(frame, text="五角星比例:").grid(column=0, row=4, sticky=tk.W)
        tk.Scale(frame, from_=0.1, to=1.0, variable=self.star_scale_var, orient=tk.HORIZONTAL, resolution=0.01, command=self.update_preview).grid(column=1, row=4, sticky=tk.W)

        # 五角星垂直偏移
        self.vertical_offset_var = tk.IntVar(value=self.generator.vertical_offset)
        ttk.Label(frame, text="五角星垂直偏移:").grid(column=0, row=5, sticky=tk.W)
        tk.Scale(frame, from_=-100, to=100, variable=self.vertical_offset_var, orient=tk.HORIZONTAL, command=self.update_preview).grid(column=1, row=5, sticky=tk.W)

        # 噪点水平
        self.noise_level_var = tk.DoubleVar(value=self.generator.noise_level)
        ttk.Label(frame, text="噪点水平:").grid(column=0, row=6, sticky=tk.W)
        tk.Scale(frame, from_=0.0, to=1.0, variable=self.noise_level_var, orient=tk.HORIZONTAL, resolution=0.01, command=self.update_preview).grid(column=1, row=6, sticky=tk.W)

        # 上方文字大小
        self.top_text_size_var = tk.IntVar(value=self.generator.top_text_size)
        ttk.Label(frame, text="上方文字大小:").grid(column=0, row=7, sticky=tk.W)
        tk.Scale(frame, from_=10, to=50, variable=self.top_text_size_var, orient=tk.HORIZONTAL, command=self.update_preview).grid(column=1, row=7, sticky=tk.W)

        # 下方文字大小
        self.bottom_text_size_var = tk.IntVar(value=self.generator.bottom_text_size)
        ttk.Label(frame, text="下方文字大小:").grid(column=0, row=8, sticky=tk.W)
        tk.Scale(frame, from_=10, to=50, variable=self.bottom_text_size_var, orient=tk.HORIZONTAL, command=self.update_preview).grid(column=1, row=8, sticky=tk.W)

        # 上方文字间距
        self.top_text_spacing_var = tk.IntVar(value=self.generator.top_text_spacing)
        ttk.Label(frame, text="上方文字间距:").grid(column=0, row=9, sticky=tk.W)
        tk.Scale(frame, from_=-20, to=50, variable=self.top_text_spacing_var, orient=tk.HORIZONTAL, command=self.update_preview).grid(column=1, row=9, sticky=tk.W)

        # 上方文字距离圆心比例
        self.top_text_distance_ratio_var = tk.DoubleVar(value=self.generator.top_text_distance_ratio)
        ttk.Label(frame, text="上方文字距离圆心比例:").grid(column=0, row=10, sticky=tk.W)
        tk.Scale(frame, from_=0.0, to=1.0, variable=self.top_text_distance_ratio_var, orient=tk.HORIZONTAL, resolution=0.01, command=self.update_preview).grid(column=1, row=10, sticky=tk.W)

        # 下方文字距离圆心比例
        self.bottom_text_distance_ratio_var = tk.DoubleVar(value=self.generator.bottom_text_distance_ratio)
        ttk.Label(frame, text="下方文字距离圆心比例:").grid(column=0, row=11, sticky=tk.W)
        tk.Scale(frame, from_=0.0, to=1.0, variable=self.bottom_text_distance_ratio_var, orient=tk.HORIZONTAL, resolution=0.01, command=self.update_preview).grid(column=1, row=11, sticky=tk.W)

        # 水平方向文字间距
        self.horizontal_letter_spacing_var = tk.IntVar(value=self.generator.horizontal_letter_spacing)
        ttk.Label(frame, text="水平方向文字间距:").grid(column=0, row=12, sticky=tk.W)
        tk.Scale(frame, from_=-20, to=20, variable=self.horizontal_letter_spacing_var, orient=tk.HORIZONTAL, command=self.update_preview).grid(column=1, row=12, sticky=tk.W)

        # 上方文字旋转角度
        self.top_text_rotation_var = tk.IntVar(value=self.generator.top_text_rotation)
        ttk.Label(frame, text="上方文字旋转角度:").grid(column=0, row=13, sticky=tk.W)
        tk.Scale(frame, from_=-180, to=180, variable=self.top_text_rotation_var, orient=tk.HORIZONTAL, command=self.update_preview).grid(column=1, row=13, sticky=tk.W)


        # 下方数字
        self.num_bottom_var = tk.StringVar(value=self.generator.num_bottom)
        ttk.Label(frame, text="下方数字:").grid(column=0, row=14, sticky=tk.W)
        #文本输入框
        entry_top = ttk.Entry(frame, textvariable=self.num_bottom_var)#这里没有使用链式调用，感觉使用链式调用可能会更清晰
        entry_top.grid(column=1, row=14, sticky=tk.W)
        entry_top.bind('<KeyRelease>', self.update_preview)  # 绑定事件

        # 下方数字旋转角度！！！！！！！！！！有时间将其他参数补充完整
        self.bottom_num_rotation_var = tk.DoubleVar(value=self.generator.bottom_num_rotation)#定义并初始化输入框的初始值
        ttk.Label(frame, text="下方数字旋转角度:").grid(column=0, row=15, sticky=tk.W)#先定义Label参数，然后在网格第0列，14行（上一个组件的下一行）绘制一个Label
        # variable: 初始化输入框的初始值并将其值绑定给bottom_num_rotation_var
        # command: 修改事件触发回调函数
        # resolution: 移动一次滑块数值改变多少，默认为5，这里设置为0，01，此时注意使用tk.DoubleVar()，而不是tk.IntVar()
        # state = "disabled"  # 禁用滑块
        # myScale.cget("state") #获取指定参数值
        # myScale.config(state="disabled") #重置指定参数值
        # sticky: 用于控制小部件（如按钮、标签、滑块等）在其网格单元格中的对齐方式。sticky 参数通常与 grid 方法一起使用，用于指定小部件在单元格中的定位。
        tk.Scale(frame, from_=-180, to=180, variable=self.bottom_num_rotation_var, orient=tk.HORIZONTAL,
                 command=self.update_preview,resolution=0.01).grid(column=1, row=15, sticky=tk.W)#在第1列，14行绘制Scale组件

        # 图像显示区域
        self.image_label = ttk.Label(frame)#以Label形式展示图片
        self.image_label.grid(column=2, row=0, rowspan=15,padx=10, pady=10)

        # 保存按钮
        save_button = ttk.Button(frame, text="保存", command=self.save_stamp)
        save_button.grid(column=0, row=16, sticky=tk.E)#注意更新它的行数

    def update_preview(self, *args):
        # 更新生成器参数
        self.update_generator_params()
        # 生成新的印章图片
        self.current_stamp_image = self.generator.generate_stamp()
        #超分辨率处理,更加真实
        self.current_stamp_image=super_resolution(stamp_image=self.current_stamp_image)

        # 显示新的印章图片
        stamp_photo = ImageTk.PhotoImage(self.current_stamp_image)
        self.image_label.configure(image=stamp_photo)
        self.image_label.image = stamp_photo

    def save_stamp(self):
        if self.current_stamp_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.current_stamp_image.save(file_path)
                print(f"图片已保存至: {file_path}")

    def update_generator_params(self):
        self.generator.outer_radius = self.outer_radius_var.get()
        self.generator.ring_width = self.ring_width_var.get()
        self.generator.text_top = self.text_top_var.get()
        self.generator.text_bottom = self.text_bottom_var.get()
        self.generator.star_scale = self.star_scale_var.get()
        self.generator.vertical_offset = self.vertical_offset_var.get()
        self.generator.noise_level = self.noise_level_var.get()
        self.generator.top_text_size = self.top_text_size_var.get()
        self.generator.bottom_text_size = self.bottom_text_size_var.get()
        self.generator.top_text_spacing = self.top_text_spacing_var.get()
        self.generator.top_text_distance_ratio = self.top_text_distance_ratio_var.get()
        self.generator.bottom_text_distance_ratio = self.bottom_text_distance_ratio_var.get()
        self.generator.horizontal_letter_spacing = self.horizontal_letter_spacing_var.get()
        self.generator.top_text_rotation = self.top_text_rotation_var.get()
        #下面是关于底部数字的参数
        self.generator.bottom_num_rotation=self.bottom_num_rotation_var.get()
        self.generator.num_bottom=self.num_bottom_var.get()
if __name__ == "__main__":
    root = tk.Tk()
    app = StampApp(root)
    root.mainloop()