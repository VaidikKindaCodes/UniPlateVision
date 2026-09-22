Dataset tools

Utilities to inspect and prepare the VoTT-exported Indian license-plate dataset.

Available scripts:

- `inspect_dataset.py` — report image/annotation counts, classes, dimensions, missing files.
- `validate_annotations.py` — validate bbox values and image bounds.
- `remove_corrupt.py` — find and move corrupt/unopenable images.
- `detect_duplicates.py` — detect duplicate images (perceptual or byte-hash).
- `stats.py` — generate class and bbox statistics.
- `split_dataset.py` — create train/val/test splits and copy images + annotations.
- `generate_data_yaml.py` — create a YAML manifest for training (paths + class names).

Notes:
- These scripts work from the VoTT CSV format with header: `image,xmin,ymin,xmax,ymax,label`.
- They keep outputs under `dataset/` by default; change args to point to other locations.

Run `python script.py --help` for usage details.
