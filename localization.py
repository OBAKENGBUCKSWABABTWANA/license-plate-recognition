from skimage import data, color, filters
from skimage.io import imread
# Load an example image of a car from skimage
image = data.astronaut()  # You can replace this with your own image
image = imread('car.jpg')
# Convert to grayscale
gray_car_image = color.rgb2gray(image)

# Apply a threshold to get a binary image
thresh = filters.threshold_otsu(gray_car_image)
binary_car_image = gray_car_image > thresh
