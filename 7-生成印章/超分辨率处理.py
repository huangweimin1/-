import cv2
from PIL import Image
import numpy as np
def super_resolution(stamp_image): #PIL 图像对象
    # 获取原始图像的尺寸
    original_width, original_height = stamp_image.size

    # 加载生成的印章图像
    #stamp_image = Image.open("12.png")  # 替换为生成的印章图像路径
    stamp_np = np.array(stamp_image)

    # 初始化超分辨率模型
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    # https://github.com/fannymonori/TF-ESPCN/tree/master/export下载模型
    model_path = "ESPCN_x4.pb"  # x4表示四倍，与下面的scale一致

    # 读取超分辨率模型
    sr.readModel(model_path)

    # 设置放大倍率（根据模型）
    scale = 4  # 这里使用x4放大倍率
    sr.setModel("espcn", scale)

    # 转换图像到超分辨率版本
    upscaled_img = sr.upsample(stamp_np)
    # 显示和保存图像
    upscaled_image_pil = Image.fromarray(upscaled_img)



    # 将超分辨率图像缩放
    resized_image = upscaled_image_pil.resize((600,600))#太大界面展示不下
    #return  upscaled_image_pil
    return resized_image
    #upscaled_image_pil.show()

    #upscaled_image_pil.save("upscaled_stamp.png")


