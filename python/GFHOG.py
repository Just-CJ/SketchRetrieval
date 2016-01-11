# coding=utf-8
import cv2
import numpy as np
import sklearn

SKETCH = 1
IMAGE = 2
test = np.array([])


class GFHOG:

    __gradient = None
    __hog = None

    def __init__(self):
        self.__hog = cv2.HOGDescriptor('hog.xml')

    def compute(self, img, t=SKETCH):

        if t == SKETCH:
            self.compute_sketch(img)
        else:
            self.compute_image(img)

    def compute_sketch(self, img):
        # 灰度化
        if img.ndim > 2:
            cv2.cvtColor(img, cv2.COLOR_BGR2GRAY, img)

        # 计算梯度场
        self.compute_gradient(img)

    def compute_image(self, img):

        # 灰度化
        if img.ndim > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 提取边缘
        edge = np.zeros(img.shape, dtype=np.uint8)
        for s in range(19, 1, -2):
            cv2.GaussianBlur(img, (s, s), 0, edge)
            cv2.Canny(edge, 100, 200, edge)
            sum = cv2.sumElems(edge)
            area = 1.0*sum[0] / (edge.size*255)
            if area > 0.02:
                break
        cv2.bitwise_not(edge, edge)
        # cv2.imshow("edge", edge)
        # cv2.waitKey()
        # 计算梯度场
        self.compute_gradient(edge)

    def compute_gradient(self, edge):
        gradient = np.zeros(edge.shape, dtype=np.float32)
        gradient = edge * np.float32(1.0 / 255.0)

        # 计算梯度场
        gradient = self.gradient_field(gradient)

        cv2.bitwise_not(edge, edge)
        self.__gradient = np.copy(gradient)

        tmp = gradient*255.0
        cv2.imwrite("5_gradient.jpg", np.array(tmp, dtype=np.uint8))
        cv2.imshow("gradient", np.array(tmp, dtype=np.uint8))
        cv2.waitKey()
        # 计算hog
        self.__hog.compute(gradient)

    def gradient_field(self, gradient):
        # 默认mask
        mask = np.zeros(gradient.shape, dtype=np.uint8)
        cv2.bitwise_not(mask, mask)

        ww = gradient.shape[1]
        hh = gradient.shape[0]

        dx = np.zeros(gradient.shape, dtype=np.float32)
        dy = np.zeros(gradient.shape, dtype=np.float32)

        # 计算水平与竖直的差分
        cv2.Sobel(gradient, cv2.CV_32F, 1, 0, dx)
        cv2.Sobel(gradient, cv2.CV_32F, 0, 1, dy)

        # 结果与mask相乘
        # dx = np.multiply(mask, dx)
        # dy = np.multiply(mask, dy)
        # dx = cv2.multiply(mask, dx)
        # dy = cv2.multiply(mask, dy)

        mag = np.zeros(gradient.shape, dtype=np.float32)
        ang = np.zeros(gradient.shape, dtype=np.float32)

        # 转换到极坐标
        cv2.cartToPolar(dx, dy, mag, ang)

        mag = ang * np.float32(1.0/(2.0*np.pi))
        return mag

    def gradient(self):
        return self.__gradient

if __name__ == '__main__':
    im = cv2.imread('img/5.png')
    # im = cv2.resize(im, (100, im.shape[0]*100/im.shape[1]))
    # cv2.imwrite("5_scale.jpg", im)
    # cv2.waitKey()
    gfhog = GFHOG()
    gfhog.compute(im, SKETCH)