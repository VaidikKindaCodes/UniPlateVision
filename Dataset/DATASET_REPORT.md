# ANPR Dataset Preparation Report

> [!WARNING]
> **Dataset Preparation Stage Only**
> This report reflects the completion of the dataset preparation pipeline. It does NOT claim that the dataset is perfect, does NOT imply any training has been completed, and makes no claims regarding model accuracy.

## 1. Source and Raw Status
- **Source Repository**: `<local_repo_root>`
- **Raw Image Count**: 237 images on disk
- **Total Annotation Rows**: 226 bounding boxes in the raw VoTT export
- **Annotated Images**: 210 unique images
- **Unannotated Images**: 27 images found on disk with no corresponding CSV annotations
- **Corrupt Images**: 0 corrupt images detected
- **Duplicates Detected**:
  - Group 1: 134.jpg, 205.jpg
  - Group 2: 182.jpg, 235.jpg
- **Invalid Annotations**: 2 bounding boxes were found to slightly exceed image boundaries (115.jpg and 130.jpg). These were automatically clipped during the YOLO conversion.

## 2. Processed Dataset Details
- **Final Output Location**: `Dataset/processed_dataset/`
- **Annotation Format**: YOLO TXT format (normalized center coordinates)
- **Number of Labels/Classes**: 1
- **Class Mapping**:
  - `0`: plate
- **Final Data Split** (Duplicate groups were kept entirely in the same split to prevent train/val leakage):
  - **Train**: 168 images
  - **Validation**: 20 images
  - **Test**: 22 images

## 3. Preprocessing Steps Performed
1. **Environment Setup**: Created a virtual environment (`venv`) and installed all needed dependencies.
2. **Dataset Auditing**: Analyzed the raw VoTT CSV against the files on disk, finding 27 unannotated images.
3. **Data Integrity Checks**: Validated bounding box coordinates and ran image integrity (corruption) and perceptual hash duplicate detection checks.
4. **Label Conversion**: Updated the `split_dataset.py` script to actively convert the raw CSV bounding boxes into normalized YOLO txt label format. Exceeded bounding boxes were clipped to image limits.
5. **Data Splitting**: Grouped duplicated images so they were routed as a single entity, preventing data leakage, and generated an 80/10/10 random split.
6. **Configuration Gen**: Created the YOLO `data.yaml` manifest.
7. **Visual Validation**: Generated a batch of 20 sample images with bounding boxes overlaid to ensure the coordinate conversion was correct.

## 4. Known Limitations & Manual Review Needed
- **Unannotated Images**: 27 raw images lack annotations. They have not been deleted, but they are excluded from the processed dataset. A visual contact sheet was produced at `Dataset/reports/unannotated_contact_sheet.jpg` for manual review to decide if they should be annotated, used as negative samples, or removed.
- The single "plate" class currently relies purely on a single annotator's pass.
