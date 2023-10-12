import sys
EVADB_FOLDER = str(input("""Enter the folder that evadb's root is in there:"""))
if EVADB_FOLDER == "":
    EVADB_FOLDER="/Users/mohammadhp/Desktop/Projects/evadb_extention/evadb/"
sys.path.append(EVADB_FOLDER)


import evadb
import shutil
import cv2
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    cursor = evadb.connect().cursor()
    cursor.query("DROP TABLE IF EXISTS Image;").df()
    cursor.query("LOAD IMAGE 'Images/*.jpeg' INTO Image").df()

    file_path = os.path.join(EVADB_FOLDER, "evadb/functions/ndarray")

    cursor.query("DROP FUNCTION IF EXISTS grayscale;").df()
    cursor.query(f"CREATE FUNCTION grayscale IMPL  '{file_path}/grayscale.py';").df()

    cursor.query("DROP FUNCTION IF EXISTS highpass;").df()
    cursor.query(f"CREATE FUNCTION highpass IMPL  '{file_path}/high_pass.py';").df()

    cursor.query("DROP FUNCTION IF EXISTS threshold;").df()
    cursor.query(f"CREATE FUNCTION threshold IMPL  '{file_path}/threshold.py';").df()

    cursor.query("DROP FUNCTION IF EXISTS blob_detector;").df()
    cursor.query(f"CREATE FUNCTION blob_detector IMPL  '{file_path}/blob_detector.py';").df()
    res4 = cursor.query("""
        SELECT img.data, blob_detector(thresh.data)
        FROM Image as img
        JOIN LATERAL grayscale(img.data) AS gray(data)
        JOIN LATERAL highpass(gray.data) AS high(data)
        JOIN LATERAL threshold(high.data) AS thresh(data)
        """).df()

    for i in range(len(res4.index)):
        base_mask = np.zeros_like(res4["blob_detector.labeled_im"].iloc[i], dtype=np.uint8)
        fig, ax = plt.subplots(1, figsize=(10, 10))

        for label in range(1, res4["blob_detector.num_labels"].iloc[i]):
            mask = base_mask.copy()
            mask[res4["blob_detector.labeled_im"].iloc[i] == label] = 255

            moments = cv2.moments(mask)
            area = moments['m00']

            # Classify defects based on blob attributes
            if area < 1500:
                continue
            elif 1500 <= area < 2500:
                defect_type = 'Porosity'
            elif 2500 <= area < 3500:
                defect_type = 'Blowhole'
            else:
                defect_type = 'Inclusion'

            # Find the center of the blob
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])

            # Annotate the defect type on the plot
            ax.text(cX, cY, defect_type, color='red', fontsize=8, ha='center')

        # Display the result using matplotlib
        ax.imshow(res4["img.data"].iloc[i], cmap='gray')
        ax.set_title('Detected Defects')
        plt.axis('off')
        plt.show()

        # Ask the user if they want to continue viewing
        answer = input("Continue viewing? (yes/no): ")
        if answer.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
