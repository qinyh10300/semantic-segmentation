import cv2
import numpy as np

# 用来存储鼠标点击的像素位置
clicked_color = None

# 鼠标回调函数
def click_event(event, x, y, flags, param):
    global clicked_color
    if event == cv2.EVENT_LBUTTONDOWN:
        # 获取点击位置的像素值
        clicked_color = img[y, x]
        print(f"Clicked at ({x}, {y}) - Color: {clicked_color}")
        # 在图像上显示选中的像素位置和颜色

# 读取图像
image_path = 'Image_20250108162518871.bmp'  # 替换为你自己的图片路径
img = cv2.imread(image_path)

# 在窗口显示图像，等待鼠标点击
cv2.imshow("Image", img)
cv2.setMouseCallback("Image", click_event)

# 等待用户点击
cv2.waitKey(0)
cv2.destroyAllWindows()

# 如果点击成功，生成纯色背景图
if clicked_color is not None:
    # 创建一个与原图相同尺寸的纯色图像
    height, width, _ = img.shape
    pure_color_bg = np.full((height, width, 3), clicked_color, dtype=np.uint8)

    # 显示纯色背景图
    cv2.imshow("Pure Color Background", pure_color_bg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存生成的纯色背景图
    output_path = "pure_color_background.bmp"
    cv2.imwrite(output_path, pure_color_bg)
    print(f"Pure color background saved at: {output_path}")
else:
    print("No color selected.")
