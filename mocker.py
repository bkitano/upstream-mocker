import pandas as pd
import numpy as np
import cv2
import pyautogui
import webbrowser
from time import sleep 
from sklearn.cluster import KMeans

MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/Slice-1.png'
LOGO_PATH = '../checkout_logo.png'
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

browser = webbrowser.get(chrome_path)
browser.open(MOCK_PATH, 1)
sleep(1)

# # scale invariant icon finder
sift = cv2.SIFT_create()

logo_cv = cv2.imread(LOGO_PATH)
img1 = cv2.cvtColor(logo_cv, cv2.COLOR_BGR2GRAY) # query image
q_keypoints, q_descriptors = sift.detectAndCompute(img1,None) # query image

screencap = pyautogui.screenshot('asdf.png').convert('RGB') # Image object
screencap_cv = np.array(screencap)
screencap_cv = screencap_cv[:, :, ::-1].copy()
img2 = cv2.cvtColor(screencap_cv, cv2.COLOR_BGR2GRAY) # train image

t_keypoints, t_descriptors = sift.detectAndCompute(img2,None) # train image

# feature matching https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

matches = bf.match(q_descriptors, t_descriptors)
matches = sorted(matches, key = lambda x:x.distance)

query_points = [ q_keypoints[match.queryIdx].pt for match in matches]
train_points = [ t_keypoints[match.trainIdx].pt for match in matches]

X_train = pd.DataFrame(train_points).to_numpy()
kmeans = KMeans(n_clusters=5).fit(X_train)
    
def get_dominant_cluster_center(points):
    X_train = pd.DataFrame(points).to_numpy()
    kmeans = KMeans(n_clusters=5).fit(X_train)
    cluster = np.bincount(kmeans.labels_).argmax()
    cluster_center = kmeans.cluster_centers_[cluster]
    return list(cluster_center)

logo_location_image_x, logo_location_image_y = get_dominant_cluster_center(train_points)

# map the image coords to the screen coords
screen_x, screen_y = pyautogui.size()
image_x, image_y = screencap.size

screen_logo_position_x = logo_location_image_x / image_x * screen_x
screen_logo_position_y = logo_location_image_y / image_y * screen_y

# debugging
# [plt.plot(*point, marker='o', color='blue', markersize=1) for point in train_points]
# plt.plot(*likely_location_of_logo, marker='o', color='pink', markersize=5)
# plt.imshow(screencap)
# plt.show()

# move the cursor to the button
pyautogui.moveTo(screen_logo_position_x, screen_logo_position_y, duration=1)

# ------------------------------------------------ 
# need to make a screenshot with the popup
# darken the image lol