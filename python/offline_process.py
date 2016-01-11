from fea_extractor import FeaExtractor
from fea_extractor import SKETCH, IMAGE
import numpy as np
import os
import cv2
import time
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from scipy.cluster.vq import *
from sklearn.preprocessing import StandardScaler


train_path = 'resize_img_s'
training_names = os.listdir(train_path)

image_paths = []
for training_name in training_names:
    dir = os.path.join(train_path, training_name)
    class_path = [os.path.join(dir, f) for f in os.listdir(dir)]
    image_paths += class_path


# List where all the descriptors are stored
des_list = []

_i = 0
for image_path in image_paths:
    _i+=1
    im = cv2.imread(image_path)
    extractor = FeaExtractor()
    fea = extractor.compute(im, IMAGE, 'SIFT')
    des_list.append((image_path, fea))
    print 'stage 1: ', 1.0*_i/len(image_paths)*100, " %"

# Stack all the descriptors vertically in a numpy array
descriptors = des_list[0][1]
_i = 1
for image_path, descriptor in des_list[1:]:
    _i += 1
    descriptors = np.vstack((descriptors, descriptor))
    print 'stage 2: ', 1.0*_i/len(image_paths)*100, " %"


# Perform k-means clustering
k = 400
# start = time.clock()
# voc, variance = kmeans(descriptors, k, 1)
# end = time.clock()
# print end - start

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1e-5)
flags = cv2.KMEANS_RANDOM_CENTERS
start = time.clock()
ret, label, voc = cv2.kmeans(descriptors, k, criteria, 10, flags)
end = time.clock()
print end - start

# Calculate the histogram of features
im_features = np.zeros((len(image_paths), k), "float32")
for i in xrange(len(image_paths)):
    words, distance = vq(des_list[i][1],voc)
    for w in words:
        im_features[i][w] += 1
    print 'stage 3: ', 1.0*i/len(image_paths)*100, " %"


# Perform Tf-Idf vectorization
nbr_occurences = np.sum((im_features > 0) * 1, axis=0)
idf = np.array(np.log((1.0*len(image_paths)+1) / (1.0*nbr_occurences + 1)), 'float32')
im_features = np.multiply(im_features, idf)

# Scaling the words
stdSlr = StandardScaler().fit(im_features)
# im_features = stdSlr.transform(im_features)


# Save the
joblib.dump((im_features, k, voc, image_paths, idf), "sift_s.pkl", compress=3)
