import pandas as pd
import numpy as np
import cv2
from sklearn.cluster import KMeans
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt

RECORDING_FRAME_RATE = 2.5

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
def get_button_coordinates(train_image_as_pil: Image, query_image_path, screen_size, debug=False, image_coords=False):

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
    print(match_x, match_y)

    # debugging
    if debug:
        [plt.plot(*point, marker='o', color='blue', markersize=1) for point in train_points]
        plt.plot(match_x,match_y, marker='x', color='pink', markersize=3)
        plt.imshow(train_image_as_pil)
        plt.show()

    if image_coords:
        return (match_x, match_y)

    # map the image coords to the screen coords
    return map_image_coords_to_screen_coords((match_x, match_y), train_image_as_pil.size, screen_size)
    

def map_image_coords_to_screen_coords(image_coords, image_size, screen_size):
    screen_width, screen_height = screen_size
    image_width, image_height = image_size
    image_x, image_y = image_coords

    screen_x = image_x / image_width * screen_width
    screen_y = image_y / image_height * screen_height
    
    return (screen_x,screen_y)

def map_screen_cords_to_image_coords(screen_coords, image_size, screen_size):
    image_width, image_height = image_size
    screen_width, screen_height = screen_size
    screen_x, screen_y = screen_coords

    image_x = screen_x / screen_width * image_width
    image_y = screen_y / screen_height * image_height
    
    return (int(image_x),int(image_y))

'''
this method darkens an image
'''
def darken_image(img: Image):
    brightness = ImageEnhance.Brightness(img)
    new_image = brightness.enhance(.4)
    return new_image


'''
given a frame, this makes a .avi video of that frame for the duration.
'''
def make_video_from_frame(frame_path, duration, out_name):
    img = cv2.imread(frame_path)
    height, width, layers = img.shape
    
    codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    out = cv2.VideoWriter(out_name, codec, RECORDING_FRAME_RATE, (width, height))

    for i in range(int(duration * RECORDING_FRAME_RATE)):
        out.write(img)

    out.release()