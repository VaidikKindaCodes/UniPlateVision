import os
import csv
import matplotlib.pyplot as plt
from PIL import Image

raw_dir = 'Dataset/Dataset'
csv_path = 'Dataset/Dataset/vott-export.csv'
processed_base = 'Dataset/processed_dataset/images'
report_path = 'Dataset/reports/dataset_reconciliation.md'
unannotated_txt = 'Dataset/reports/unannotated_images.txt'
contact_sheet_path = 'Dataset/reports/unannotated_contact_sheet.jpg'

# 1. Raw Images
raw_images = set(f for f in os.listdir(raw_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png')))

# 2. Referenced Images
referenced_images = set()
if os.path.exists(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            referenced_images.add(row['image'])

# 3. Processed Images
processed_train = set(f for f in os.listdir(os.path.join(processed_base, 'train')) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
processed_val = set(f for f in os.listdir(os.path.join(processed_base, 'val')) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
processed_test = set(f for f in os.listdir(os.path.join(processed_base, 'test')) if f.lower().endswith(('.jpg', '.jpeg', '.png')))

processed_images = processed_train.union(processed_val).union(processed_test)

# A. Annotated + Processed
annotated_processed = processed_images.intersection(referenced_images)

# B. Unannotated
unannotated = raw_images - referenced_images

# C. Referenced But Missing
referenced_missing = referenced_images - raw_images

# D. Raw Images Not Accounted For
raw_unaccounted = raw_images - processed_images - unannotated

# Annotated existing in raw
annotated_in_raw = referenced_images.intersection(raw_images)

# Output unannotated text file
with open(unannotated_txt, 'w', encoding='utf-8') as f:
    for img in sorted(unannotated):
        f.write(img + '\n')

# Create contact sheet
cols = 5
rows = (len(unannotated) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(15, 3*rows))
for i, ax in enumerate(axes.flatten()):
    if i < len(unannotated):
        img_name = sorted(list(unannotated))[i]
        img_path = os.path.join(raw_dir, img_name)
        img = Image.open(img_path)
        ax.imshow(img)
        # Put title below image
        ax.set_title(img_name, fontsize=10, y=-0.2)
    ax.axis('off')

plt.subplots_adjust(hspace=0.4)
plt.savefig(contact_sheet_path, bbox_inches='tight')
plt.close()

# Report Generation
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# Dataset Reconciliation Report\n\n")
    
    f.write(f"Raw Images Found: {len(raw_images)}\n")
    f.write(f"Images Referenced in CSV: {len(referenced_images)}\n")
    f.write(f"Processed Images (train+val+test): {len(processed_images)}\n\n")
    
    f.write(f"Train Count: {len(processed_train)}\n")
    f.write(f"Val Count: {len(processed_val)}\n")
    f.write(f"Test Count: {len(processed_test)}\n\n")
    
    eq1_left = len(raw_images)
    eq1_right = len(annotated_in_raw) + len(unannotated)
    f.write(f"Verification 1 (raw images = annotated images + unannotated images): {'Passed' if eq1_left == eq1_right else 'Failed'} ({eq1_left} = {len(annotated_in_raw)} + {len(unannotated)})\n")
    
    eq2_left = len(processed_train) + len(processed_val) + len(processed_test)
    eq2_right = len(annotated_processed)
    f.write(f"Verification 2 (train + val + test = annotated images used for training): {'Passed' if eq2_left == eq2_right else 'Failed'} ({eq2_left} = {eq2_right})\n\n")
    
    f.write("## A. ANNOTATED + PROCESSED\n")
    f.write(f"Count: {len(annotated_processed)}\n")
    for img in sorted(annotated_processed):
        f.write(f"- {img}\n")
    f.write("\n")
    
    f.write("## B. UNANNOTATED\n")
    f.write(f"Count: {len(unannotated)}\n")
    for img in sorted(unannotated):
        f.write(f"- {img}\n")
    f.write("\n")
    
    f.write("## C. REFERENCED BUT MISSING\n")
    f.write(f"Count: {len(referenced_missing)}\n")
    for img in sorted(referenced_missing):
        f.write(f"- {img}\n")
    f.write("\n")
    
    f.write("## D. RAW IMAGES NOT ACCOUNTED FOR\n")
    f.write(f"Count: {len(raw_unaccounted)}\n")
    for img in sorted(raw_unaccounted):
        f.write(f"- {img}\n")
    f.write("\n")

print("Reconciliation complete. Reports generated.")
