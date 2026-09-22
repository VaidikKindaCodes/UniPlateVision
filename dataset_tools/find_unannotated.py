import os
import csv
# pyrefly: ignore [missing-import]
from PIL import Image
import matplotlib.pyplot as plt

csv_path = 'Dataset/Dataset/vott-export.csv'
images_dir = 'Dataset/Dataset'
report_path = 'Dataset/reports/unannotated_images.txt'
contact_sheet_path = 'Dataset/reports/unannotated_contact_sheet.jpg'

annotated = set()
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        annotated.add(r['image'])

all_images = set(f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
unannotated = sorted(all_images - annotated)

with open(report_path, 'w', encoding='utf-8') as f:
    for img in unannotated:
        f.write(img + '\n')

print(f"Found {len(unannotated)} unannotated images.")

# Create contact sheet
cols = 5
rows = (len(unannotated) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(15, 3*rows))
for i, ax in enumerate(axes.flatten()):
    if i < len(unannotated):
        img_path = os.path.join(images_dir, unannotated[i])
        img = Image.open(img_path)
        ax.imshow(img)
        ax.set_title(unannotated[i], fontsize=8)
    ax.axis('off')

plt.tight_layout()
plt.savefig(contact_sheet_path)
print(f"Contact sheet saved to {contact_sheet_path}")
