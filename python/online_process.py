from fea_extractor import FeaExtractor
from fea_extractor import SKETCH, IMAGE

import argparse as ap
import numpy as np
import os
import cv2
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from scipy.cluster.vq import *
from scipy.spatial.distance import cdist
from scipy import stats
from sklearn.preprocessing import StandardScaler

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-t", "--testimage", help="Path to Test Image", required="True")
parser.add_argument("-f", "--featype", help="Feature type", required="True")
args = vars(parser.parse_args())

# Get the training classes names and store them in a list
image_path = args["testimage"]
fea_type = args["featype"]


pkl_path = ''
if fea_type == 'HOG':
    pkl_path = "python/hog_all.pkl"
elif fea_type == 'SIFT':
    pkl_path = "python/sfit_s.pkl"

# Load the im_features, k, voc, image_paths, idf and vocabulary
im_features, k, voc, image_paths, idf = joblib.load(pkl_path)

# image_path = '330sketches/6/9.png'

# Create feature extraction and keypoint detector objects
im = cv2.imread(image_path)
im = cv2.resize(im, (200, 200))
extractor = FeaExtractor()
fea = extractor.compute(im, SKETCH, fea_type)

test_features = np.zeros((1, k), "float32")
words, distance = vq(fea, voc)
for w in words:
    test_features[0][w] += 1

# Perform Tf-Idf vectorization
test_features = np.multiply(test_features, idf)

# Scaling the words
# test_features = stdSlr.transform(test_features)

dist = cdist(test_features, im_features, 'cityblock')
dist = dist[0]

res = sorted(zip(dist, image_paths), key=lambda x: x[0])
for i in range(10):
    # cv2.imshow(str(i), cv2.imread(res[i][1]))
    print res[i][1] + ':' +  str(res[i][0])
    # cv2.waitKey()
