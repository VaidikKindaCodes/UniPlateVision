#!/usr/bin/env python3
import csv
import os
import argparse
import random
import shutil
from collections import defaultdict
from PIL import Image

def split(csv_path, images_dir, out_dir='dataset', train=0.8, val=0.1, test=0.1, seed=42):
    assert abs(train + val + test - 1.0) < 1e-6
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        img_to_rows = defaultdict(list)
        for r in reader:
            img_to_rows[r['image']].append(r)

    # Group duplicates so they stay in the same split
    # Known duplicates: [134.jpg, 205.jpg] and [182.jpg, 235.jpg]
    duplicates = [
        {'134.jpg', '205.jpg'},
        {'182.jpg', '235.jpg'}
    ]
    
    # We will treat each group as a single entity for splitting
    all_imgs = set(img_to_rows.keys())
    
    entities = []
    assigned = set()
    for d in duplicates:
        present = list(d.intersection(all_imgs))
        if present:
            entities.append(present)
            assigned.update(present)
            
    for img in all_imgs:
        if img not in assigned:
            entities.append([img])
            
    random.seed(seed)
    random.shuffle(entities)
    
    n = len(entities)
    n_train = int(n * train)
    n_val = int(n * val)
    
    train_imgs = set()
    for e in entities[:n_train]: train_imgs.update(e)
    
    val_imgs = set()
    for e in entities[n_train:n_train+n_val]: val_imgs.update(e)
    
    test_imgs = set()
    for e in entities[n_train+n_val:]: test_imgs.update(e)

    os.makedirs(out_dir, exist_ok=True)
    images_out = os.path.join(out_dir, 'images')
    labels_out = os.path.join(out_dir, 'labels')
    
    for split_name in ('train', 'val', 'test'):
        os.makedirs(os.path.join(images_out, split_name), exist_ok=True)
        os.makedirs(os.path.join(labels_out, split_name), exist_ok=True)

    def write_yolo_labels(img, rows, split_name):
        src = os.path.join(images_dir, img)
        dst = os.path.join(images_out, split_name, img)
        if not os.path.exists(src):
            return
            
        with Image.open(src) as im:
            img_w, img_h = im.size
            
        shutil.copy2(src, dst)
        
        base, _ = os.path.splitext(img)
        label_file = os.path.join(labels_out, split_name, f'{base}.txt')
        
        with open(label_file, 'w', encoding='utf-8') as lf:
            for r in rows:
                # clip coordinates
                xmin = max(0, min(float(r['xmin']), img_w))
                ymin = max(0, min(float(r['ymin']), img_h))
                xmax = max(0, min(float(r['xmax']), img_w))
                ymax = max(0, min(float(r['ymax']), img_h))
                
                # if box is completely outside or invalid after clipping, skip
                if xmax <= xmin or ymax <= ymin:
                    continue
                    
                x_center = ((xmin + xmax) / 2.0) / img_w
                y_center = ((ymin + ymax) / 2.0) / img_h
                width = (xmax - xmin) / img_w
                height = (ymax - ymin) / img_h
                
                # class 0 = plate
                lf.write(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    for img in train_imgs:
        write_yolo_labels(img, img_to_rows.get(img, []), 'train')
    for img in val_imgs:
        write_yolo_labels(img, img_to_rows.get(img, []), 'val')
    for img in test_imgs:
        write_yolo_labels(img, img_to_rows.get(img, []), 'test')
        
    print(f'Split done. Images -> {images_out}, Labels -> {labels_out}')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', default='Dataset/Dataset/vott-export.csv')
    p.add_argument('--images', default='Dataset/Dataset')
    p.add_argument('--out', default='Dataset/processed_dataset')
    p.add_argument('--train', type=float, default=0.8)
    p.add_argument('--val', type=float, default=0.1)
    p.add_argument('--test', type=float, default=0.1)
    args = p.parse_args()
    split(args.csv, args.images, args.out, args.train, args.val, args.test)

if __name__ == '__main__':
    main()
