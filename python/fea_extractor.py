# coding=utf-8
import cv2
import numpy as np

SKETCH = 1
IMAGE = 2
test = np.array([])


class FeaExtractor:

    __fea = None

    def __init__(self):
        pass

    def compute(self, img, t=SKETCH, fea_type='HOG'):

        if t == SKETCH:
            self.compute_sketch(img, fea_type)
        else:
            self.compute_image(img, fea_type)

        return self.__fea

    def compute_sketch(self, img, fea_type):
        # 灰度化
        if img.ndim > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if fea_type == 'HOG':
            # 计算hog
            self.compute_hog(img)
        elif fea_type == 'SIFT':
            self.compute_sift(img)

    def compute_image(self, img, fea_type):

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

        if fea_type == 'HOG':
            # 计算hog
            self.compute_hog(img)
        elif fea_type == 'SIFT':
            self.compute_sift(img)

    def compute_hog(self, edge):
        __hog = cv2.HOGDescriptor('python/hog.xml')
        tmpfea = __hog.compute(edge, (50, 50))
        self.__fea = tmpfea.reshape((tmpfea.shape[0]/36, 36))

    def compute_sift(self, edge):
        fea_det = cv2.FeatureDetector_create("SIFT")
        des_ext = cv2.DescriptorExtractor_create("SIFT")
        kpts = fea_det.detect(edge)
        kpts, tmpfea = des_ext.compute(edge, kpts)
        self.__fea = tmpfea

    def fea(self):
        return self.__fea


if __name__ == '__main__':
    im = cv2.imread('img/5.png')
    print im.shape
    im = cv2.resize(im, dsize=(200, 200))
    hog = FeaExtractor()
    fea = hog.compute(im, SKETCH)
    print np.max(fea)