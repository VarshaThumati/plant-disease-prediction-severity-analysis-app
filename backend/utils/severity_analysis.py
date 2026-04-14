import cv2
import numpy as np

def get_disease_mask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # --- Brown / Yellow (blight) ---
    lower1 = np.array([10, 100, 20])
    upper1 = np.array([35, 255, 255])

    # --- Dark spots (late blight / severe infection) ---
    lower2 = np.array([0, 0, 0])
    upper2 = np.array([180, 255, 50])

    # --- Grayish / mold ---
    lower3 = np.array([0, 0, 50])
    upper3 = np.array([180, 50, 150])

    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)
    mask3 = cv2.inRange(hsv, lower3, upper3)

    combined_mask = mask1 | mask2 | mask3

    return combined_mask


def calculate_severity_and_spread(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (256, 256))

    disease_mask = get_disease_mask(img)

    # --- REMOVE NOISE (Step 2 also important) ---
    kernel = np.ones((3,3), np.uint8)
    disease_mask = cv2.morphologyEx(disease_mask, cv2.MORPH_OPEN, kernel)
    disease_mask = cv2.morphologyEx(disease_mask, cv2.MORPH_DILATE, kernel)

    # --- NEW STEP 3 (Leaf-only calculation) ---
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 40, 40])
    upper_green = np.array([90, 255, 255])

    leaf_mask = cv2.inRange(hsv, lower_green, upper_green)

    valid_area = leaf_mask > 0

    infected_pixels = np.sum((disease_mask > 0) & valid_area)
    total_pixels = np.sum(valid_area)

    if total_pixels == 0:
        severity = 0
    else:
        severity = (infected_pixels / total_pixels) * 100

    # --- Spread ---
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(disease_mask)
    areas = stats[1:, cv2.CC_STAT_AREA]

    if len(areas) == 0:
        spread = 0
    else:
        if len(areas) == 0 or np.max(areas) == 0:
            spread = 0
        else:
            spread = np.sum(areas) / np.max(areas)

    return round(severity, 2), round(spread, 2)