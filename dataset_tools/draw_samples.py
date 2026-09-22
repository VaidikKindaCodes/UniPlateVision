import os
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

images_dir = 'Dataset/processed_dataset/images/train'
labels_dir = 'Dataset/processed_dataset/labels/train'
out_dir = 'Dataset/samples/annotated'
os.makedirs(out_dir, exist_ok=True)

images = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]
random.seed(42)
sample_imgs = random.sample(images, min(20, len(images)))

for img_name in sample_imgs:
    img_path = os.path.join(images_dir, img_name)
    label_path = os.path.join(labels_dir, img_name.replace('.jpg', '.txt'))
    
    img = Image.open(img_path)
    w, h = img.size
    
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 5:
                    _, x_center, y_center, width, height = map(float, parts)
                    # Convert YOLO format back to pixel coordinates for drawing
                    box_w = width * w
                    box_h = height * h
                    x_min = (x_center * w) - (box_w / 2)
                    y_min = (y_center * h) - (box_h / 2)
                    
                    rect = patches.Rectangle((x_min, y_min), box_w, box_h, linewidth=2, edgecolor='r', facecolor='none')
                    ax.add_patch(rect)
                    
    plt.axis('off')
    out_path = os.path.join(out_dir, img_name)
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()

print(f"Saved {len(sample_imgs)} annotated samples to {out_dir}")
