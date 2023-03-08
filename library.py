import pandas as pd
import numpy as np
import cv2
import pyautogui
from sklearn.cluster import KMeans
from PIL import Image

MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/Slice-1.png'
LOGO_PATH = '../checkout_logo.png'
CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
SCREEN_SIZE = tuple(pyautogui.size())

'''
Gets the coordinates of the cluster with the most points.
'''
def get_dominant_cluster_center(points):
    X_train = pd.DataFrame(points).to_numpy()
    kmeans = KMeans(n_clusters=5).fit(X_train)
    cluster = np.bincount(kmeans.labels_).argmax()
    cluster_center = kmeans.cluster_centers_[cluster]
    return list(cluster_center)

'''
returns the location of the object on the page (scale invariant)
'''
def get_button_coordinates(train_image_as_pil: Image, query_image_path=LOGO_PATH):

    # # scale invariant icon finder
    sift = cv2.SIFT_create()

    query_cv = cv2.imread(query_image_path)
    query_img = cv2.cvtColor(query_cv, cv2.COLOR_BGR2GRAY)
    _, q_descriptors = sift.detectAndCompute(query_img, None)

    train_cv = np.array(train_image_as_pil)
    train_cv = train_cv[:, :, ::-1].copy()
    train_img = cv2.cvtColor(train_cv, cv2.COLOR_BGR2GRAY)
    t_keypoints, t_descriptors = sift.detectAndCompute(train_img, None)

    # feature matching https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    matches = bf.match(q_descriptors, t_descriptors)

    train_points = [ t_keypoints[match.trainIdx].pt for match in matches ]
    match_x, match_y = get_dominant_cluster_center(train_points)

    # map the image coords to the screen coords
    screen_x, screen_y = SCREEN_SIZE
    image_x, image_y = train_image_as_pil.size

    mapped_x = match_x / image_x * screen_x
    mapped_y = match_y / image_y * screen_y
    return (mapped_x,mapped_y)

# debugging
# [plt.plot(*point, marker='o', color='blue', markersize=1) for point in train_points]
# plt.plot(*likely_location_of_logo, marker='o', color='pink', markersize=5)
# plt.imshow(screencap)
# plt.show()
