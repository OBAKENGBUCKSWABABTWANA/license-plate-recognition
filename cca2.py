from skimage import measure
from skimage.io import imsave
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import localization

# this gets all the connected regions and groups them together
label_image = measure.label(localization.binary_car_image)

# getting the maximum width, height and minimum width and height that a license plate can be
plate_dimensions = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
min_height, max_height, min_width, max_width = plate_dimensions
plate_objects_cordinates = []
plate_like_objects = []
fig, (ax1) = plt.subplots(1)
ax1.imshow(localization.gray_car_image, cmap="gray");

# regionprops creates a list of properties of all the labelled regions
for region in regionprops(label_image):
    if region.area < 50:
        #if the region is so small then it's likely not a license plate
        continue

    # the bounding box coordinates
    min_row, min_col, max_row, max_col = region.bbox
    region_height = max_row - min_row
    region_width = max_col - min_col
    # ensuring that the region identified satisfies the condition of a typical license plate
aspect_ratio = region_width / region_height
if (
    min_height <= region_height <= max_height and
    min_width <= region_width <= max_width and
    2 <= aspect_ratio <= 6
):

        plate_like_objects.append(localization.binary_car_image[min_row:max_row,
                                  min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,
                                              max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
        ax1.add_patch(rectBorder)
        print(f"Detected {len(plate_like_objects)} license plate-like region(s).")

    # let's draw a red rectangle over those regions

# Save each detected plate-like object
for i, plate in enumerate(plate_like_objects):
    imsave(f"plate_candidate_{i+1}.png", plate.astype(float))


plt.show()
