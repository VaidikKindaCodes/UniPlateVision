#!/usr/bin/env python3
import csv
import argparse
from collections import Counter


def generate_stats(csv_path, out_json=None):
    classes = Counter()
    areas = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            label = r.get('label')
            classes[label] += 1
            try:
                xmin = float(r.get('xmin') or 0)
                ymin = float(r.get('ymin') or 0)
                xmax = float(r.get('xmax') or 0)
                ymax = float(r.get('ymax') or 0)
                areas.append((xmax - xmin) * (ymax - ymin))
            except Exception:
                pass

    print('Classes:')
    for k, v in classes.most_common():
        print(f'  {k}: {v}')
    if areas:
        areas.sort()
        n = len(areas)
        print(f'BBox areas: min={areas[0]:.1f} median={areas[n//2]:.1f} max={areas[-1]:.1f}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', default='Dataset/Dataset/vott-export.csv')
    args = p.parse_args()
    generate_stats(args.csv)


if __name__ == '__main__':
    main()
