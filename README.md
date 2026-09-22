# Number-Plate-Detection-and-Recognition

Building a Custom License Plate Detector and Recognizer.

![Number Plate Detection](Predicted_output.jpg)

## 1. Project Overview & Current Status
This repository was originally designed to train a custom license plate detector using YOLOv3 and PyTesseract OCR. 

**Upcoming Pipeline**: We are currently upgrading this repository to use a modern **Ultralytics YOLO** object detection pipeline. 
- **Completed**: Stage 1 (Dataset collection, inspection, YOLO-format conversion, splitting, and readiness auditing).
- **Upcoming / Next Steps**: Stage 2 (Fine-tuning a pretrained YOLO detector using the processed dataset).

---

## 2. Repository Structure

### Active Directories:
- **`Dataset/`**: Contains the core data pipeline.
  - `Dataset/`: The immutable raw image and CSV source data.
  - `processed_dataset/`: The cleaned, validated, YOLO-formatted dataset split into `train/`, `val/`, and `test/`, ready for training.
  - `reports/` & `samples/`: Dataset audits, sample previews, and validation outputs.
- **`dataset_tools/`**: Modern Python scripts managing data inspection, duplicate handling, and YOLO formatting.
- **`examples/`**: Demonstration files and samples from the original repository.

### Legacy Directories:
- **`legacy/`**: Contains the original YOLOv3 and TensorFlow implementation code (`Code/` folder and `xml_to_csv.py`), preserved for historical reference only.

---

## 3. Dataset Preparation Workflow (Stage 1 - Completed)
The dataset preparation has already been executed via the scripts in `dataset_tools/`. The pipeline performs the following steps:
1. **Inspection**: Verifies raw annotations and flags unannotated or missing images.
2. **Validation**: Ensures bounding box coordinates are within image bounds and removes/flags corrupted images.
3. **Duplicate Detection**: Hashes images to find duplicates and groups them to prevent data leakage.
4. **Conversion & Splitting**: Converts VoTT CSV bounding boxes to normalized YOLO text format and randomly splits data (80/10/10) into `Dataset/processed_dataset/`.

*Note: You do not need to rerun the dataset preparation unless you modify the raw `Dataset/Dataset/`.*

---

## 4. Getting Started (For Legacy YOLOv3 Reference)
If you wish to explore the old legacy implementation stored in `legacy/Code/`, you will need an older environment (Python 3.3+).

**Note:** The legacy paths historically referenced `Number Plate Detection and Recognition/Data/...`. If you run legacy scripts, you may need to adjust paths as the `Code/` directory is now located inside `legacy/`.

---

## 5. Notes & Future Work
For better results in the upcoming YOLO models, we plan to:
- Increase epochs while training.
- Use image enhancement before prediction.
- Adapt models for surveillance/CCTV style data.

**To make everything run smoothly for the upcoming Stage 2 pipeline, please retain the modern `Dataset/` and `dataset_tools/` structures.**
