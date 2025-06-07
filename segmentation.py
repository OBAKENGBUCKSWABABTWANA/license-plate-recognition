import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from skimage.io import imsave  # Optional: for saving characters
import cca2

# Check that we have enough plate-like objects
if len(cca2.plate_like_objects) < 3:
    print("Error: Less than 3 license plate-like regions were detected.")
    exit()

# Select the third detected plate-like object
license_plate = np.invert(cca2.plate_like_objects[2])

# Label the connected components
labelled_plate = measure.label(license_plate)

# Set up plot
fig, ax1 = plt.subplots(1)
ax1.imshow(license_plate, cmap="gray")

# Character size filtering assumptions
character_dimensions = (
    0.3 * license_plate.shape[0],  # min height
    0.7 * license_plate.shape[0],  # max height
    0.03 * license_plate.shape[1], # min width
    0.2 * license_plate.shape[1]   # max width
)
min_height, max_height, min_width, max_width = character_dimensions

# Storage
characters = []
column_list = []

# Loop through each connected region
for region in regionprops(labelled_plate):
    y0, x0, y1, x1 = region.bbox
    region_height = y1 - y0
    region_width = x1 - x0

    if (
        min_height <= region_height <= max_height and
        min_width <= region_width <= max_width
    ):
        # Extract region of interest (ROI)
        roi = license_plate[y0:y1, x0:x1]

        # Draw rectangle
        rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
                                        linewidth=2, fill=False)
        ax1.add_patch(rect_border)

        # Resize to 20x20 and store
        resized_char = resize(roi, (20, 20))
        characters.append(resized_char)
        column_list.append(x0)

# Optional: sort characters left to right
characters = [char for _, char in sorted(zip(column_list, characters))]

# Optional: Save characters as images
for i, char in enumerate(characters):
    imsave(f"char_{i+1}.png", char.astype(float))

print(f"{len(characters)} characters segmented and saved.")
plt.show()
