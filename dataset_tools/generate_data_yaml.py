#!/usr/bin/env python3
import csv
import argparse
import yaml
import os


def get_classes_from_csv(csv_path):
    classes = []
    seen = set()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            lab = r.get('label')
            if lab and lab not in seen:
                seen.add(lab)
                classes.append(lab)
    return classes


def generate(out_path='data.yaml', train_images='dataset/images/train', val_images='dataset/images/val', test_images='dataset/images/test', csv_sample='Dataset/Dataset/vott-export.csv'):
    classes = get_classes_from_csv(csv_sample)
    data = {
        'train': train_images,
        'val': val_images,
        'test': test_images,
        'nc': len(classes),
        'names': classes,
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f)
    print(f'Wrote {out_path} with {len(classes)} classes')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='dataset/data.yaml')
    p.add_argument('--train', default='dataset/images/train')
    p.add_argument('--val', default='dataset/images/val')
    p.add_argument('--test', default='dataset/images/test')
    p.add_argument('--csv', default='Dataset/Dataset/vott-export.csv')
    args = p.parse_args()
    generate(args.out, args.train, args.val, args.test, args.csv)


if __name__ == '__main__':
    main()
