# Final Repository Structure

```text
.
├── .github/
│   └── FUNDING.yml
├── .gitignore
├── README.md               <-- Main project documentation
├── Predicted_output.jpg    <-- Used in README.md as the main banner image
├── Dataset/
│   ├── Dataset/            <-- Immutable raw images and VoTT CSV annotations
│   ├── processed_dataset/  <-- The active YOLO dataset split (train/val/test) and data.yaml ready for training
│   ├── reports/            <-- Reconciliations, unannotated lists, and dataset verification reports
│   ├── samples/            <-- Visualization of YOLO labels drawn on images
│   └── professor_samples/  <-- Filtered clean samples used for presentation
├── dataset_tools/          <-- Modern Python scripts for dataset inspection, prep, and pipeline auditing
│   └── *.py
├── examples/
│   └── NPR.mp4, NPR_detection.jpg, test.jpg  <-- Standalone demonstration outputs
└── legacy/
    ├── Code/               <-- Original legacy YOLOv3 and TensorFlow scripts
    └── xml_to_csv.py       <-- Legacy data conversion script
```

### Folder Purposes
- **`Dataset/`**: The entire data pipeline workspace. Only `processed_dataset/` should be fed into a training pipeline. The `Dataset/Dataset/` folder is strictly read-only raw data.
- **`dataset_tools/`**: Reproducible utilities. If the raw dataset changes, these tools can re-generate the entire processed structure.
- **`examples/`**: Kept separate from the core codebase to store various past demonstration media without cluttering root.
- **`legacy/`**: Retained for historical context. The codebase here relies on older versions of YOLOv3, TensorFlow, and older hardcoded paths.
