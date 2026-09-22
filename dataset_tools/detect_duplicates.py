#!/usr/bin/env python3
import os
import argparse
import hashlib
from collections import defaultdict
try:
    from PIL import Image
    import imagehash
    HAS_PHASH = True
except Exception:
    HAS_PHASH = False


def hash_bytes(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            b = f.read(8192)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def find_duplicates(images_dir, use_phash=HAS_PHASH, threshold=5):
    groups = defaultdict(list)
    paths = []
    for root, _, files in os.walk(images_dir):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                paths.append(os.path.join(root, f))

    if use_phash:
        for p in paths:
            try:
                ph = imagehash.phash(Image.open(p))
                groups[str(ph)].append(p)
            except Exception:
                groups[hash_bytes(p)].append(p)
    else:
        for p in paths:
            groups[hash_bytes(p)].append(p)

    duplicates = {k: v for k, v in groups.items() if len(v) > 1}
    return duplicates


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--images', default='Dataset/Dataset')
    p.add_argument('--use-phash', action='store_true')
    args = p.parse_args()
    dups = find_duplicates(args.images, use_phash=args.use_phash)
    for key, lst in dups.items():
        print(f'Group {key}:')
        for p in lst:
            print('  ', p)
        print()


if __name__ == '__main__':
    main()
