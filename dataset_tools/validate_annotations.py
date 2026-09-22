#!/usr/bin/env python3
import csv
import os
import argparse
from PIL import Image


def validate(csv_path, images_dir, report_path=None, max_errors=1000):
    errors = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, r in enumerate(reader, 1):
            img = r.get('image')
            xmin = float(r.get('xmin') or 0)
            ymin = float(r.get('ymin') or 0)
            xmax = float(r.get('xmax') or 0)
            ymax = float(r.get('ymax') or 0)
            label = r.get('label') or ''

            path = os.path.join(images_dir, img)
            if not os.path.exists(path):
                errors.append((i, img, 'missing image'))
                if len(errors) >= max_errors:
                    break
                continue
            try:
                with Image.open(path) as im:
                    w, h = im.size
            except Exception as e:
                errors.append((i, img, f'cannot open image: {e}'))
                if len(errors) >= max_errors:
                    break
                continue

            if xmin >= xmax or ymin >= ymax:
                errors.append((i, img, f'invalid bbox coords {xmin,ymin,xmax,ymax}'))
            if xmin < 0 or ymin < 0 or xmax > w or ymax > h:
                errors.append((i, img, f'bbox out of bounds image_size={w,h}'))
            if label == '':
                errors.append((i, img, 'empty label'))
            if len(errors) >= max_errors:
                break

    if report_path:
        with open(report_path, 'w', encoding='utf-8') as out:
            for e in errors:
                out.write(','.join(map(str, e)) + '\n')

    for e in errors[:50]:
        print(e)
    print(f'Total errors: {len(errors)}')


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--csv', default='Dataset/Dataset/vott-export.csv')
    p.add_argument('--images', default='Dataset/Dataset')
    p.add_argument('--out')
    args = p.parse_args()
    validate(args.csv, args.images, args.out)


if __name__ == '__main__':
    main()
