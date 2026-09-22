#!/usr/bin/env python3
import os
import argparse
import shutil
from PIL import Image


def find_and_move(images_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    moved = []
    for root, _, files in os.walk(images_dir):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                path = os.path.join(root, f)
                try:
                    with Image.open(path) as im:
                        im.verify()
                except Exception:
                    dst = os.path.join(out_dir, os.path.relpath(path, images_dir))
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.move(path, dst)
                    moved.append((path, dst))
    print(f'Moved {len(moved)} corrupt files to {out_dir}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--images', default='Dataset/Dataset')
    p.add_argument('--out', default='dataset/corrupt')
    args = p.parse_args()
    find_and_move(args.images, args.out)


if __name__ == '__main__':
    main()
