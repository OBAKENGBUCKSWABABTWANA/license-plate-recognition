import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import joblib  # ✅ modern joblib import
from skimage.io import imread
from skimage.filters import threshold_otsu

# All characters you're trying to classify
letters = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
    'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z'
]

def read_training_data(training_directory):
    image_data = []
    target_data = []
    for each_letter in letters:
        letter_dir = os.path.join(training_directory, each_letter)
        if not os.path.exists(letter_dir):
            print(f"Warning: Directory {letter_dir} does not exist.")
            continue

        for each in range(10):
            image_path = os.path.join(letter_dir, f"{each_letter}_{each}.jpg")
            if not os.path.exists(image_path):
                print(f"Warning: {image_path} not found.")
                continue

            try:
                # Load grayscale image
                img = imread(image_path, as_gray=True)
                binary_image = img < threshold_otsu(img)  # Binarize
                flat_image = binary_image.reshape(-1)     # Flatten to 1D (20x20 → 400)
                image_data.append(flat_image)
                target_data.append(each_letter)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

    return np.array(image_data), np.array(target_data)

def cross_validation(model, folds, X, y):
    scores = cross_val_score(model, X, y, cv=folds)
    print(f"{folds}-fold Cross Validation Accuracy:")
    print(scores * 100)

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
training_dir = os.path.join(current_dir, 'train')

# Read training data
image_data, target_data = read_training_data(training_dir)

# Train SVM model
model = SVC(kernel='linear', probability=True)
cross_validation(model, 4, image_data, target_data)
model.fit(image_data, target_data)

# Save model
model_dir = os.path.join(current_dir, 'models', 'svc')
os.makedirs(model_dir, exist_ok=True)
joblib.dump(model, os.path.join(model_dir, 'svc.pkl'))

print("Model trained and saved successfully.")
