#!/usr/bin/env python3
import csv
import os
import argparse
import json
from collections import defaultdict, Counter
from PIL import Image


def load_vott_csv(csv_path):
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def inspect(csv_path, images_dir, out_json=None, sample_limit=0):
    rows = load_vott_csv(csv_path)
    total_annotations = len(rows)
    images = Counter()
    classes = Counter()
    missing = set()
    sizes = defaultdict(lambda: None)

    for i, r in enumerate(rows):
        imgname = r.get('image')
        label = r.get('label') or r.get('class')
        images[imgname] += 1
        if label:
            classes[label] += 1

    unique_images = list(images.keys())

    for idx, img in enumerate(unique_images):
        path = os.path.join(images_dir, img)
        if not os.path.exists(path):
            missing.add(img)
            continue
        try:
            with Image.open(path) as im:
                sizes[img] = im.size  # (w,h)
        except Exception:
            missing.add(img)

    width_counts = Counter()
    height_counts = Counter()
    for s in sizes.values():
        if s:
            w, h = s
            width_counts[w] += 1
            height_counts[h] += 1

    summary = {
        'total_annotations': total_annotations,
        'unique_images': len(unique_images),
        'classes': dict(classes),
        'missing_images_count': len(missing),
        'missing_images_sample': list(sorted(missing))[:20],
        'image_size_counts': {
            'width_counts_top10': width_counts.most_common(10),
            'height_counts_top10': height_counts.most_common(10),
        }
    }

    print(json.dumps(summary, indent=2))
    if out_json:
        with open(out_json, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', default='Dataset/Dataset/vott-export.csv')
    p.add_argument('--images', default='Dataset/Dataset')
    p.add_argument('--out', help='Write summary JSON')
    args = p.parse_args()
    inspect(args.csv, args.images, args.out)


if __name__ == '__main__':
    main()
