# Repository Cleanup Audit

## Classification Criteria
- **KEEP**: Required for the project.
- **KEEP/DEMO**: Useful example/demo artifact.
- **KEEP/RESEARCH**: Useful for dataset/research documentation.
- **REMOVE**: Generated/local/unnecessary files that should be deleted.
- **GITIGNORE**: Must not be committed but should remain locally on disk.
- **AUDIT**: Needs a manual decision from you.

## Folder & File Analysis

| Path | Classification | Reason | Safe to remove? | Action required |
|------|----------------|--------|-----------------|-----------------|
| `.github/` | KEEP | Contains FUNDING.yml. | No | Keep. |
| `.vscode/` | GITIGNORE | Contains `settings.json` with local `venv` path. | No | Add to `.gitignore`. |
| `Code/` | AUDIT | Old YOLOv3/TensorFlow scripts. Likely obsolete now that we use modern YOLO, but might have reference value. | Yes (if obsolete) | Decide if you want to keep legacy code. |
| `Dataset/Dataset/` | KEEP | Immutable raw dataset (images & VoTT CSV). | No | Keep untouched. |
| `Dataset/processed_dataset/` | KEEP | Final YOLO format data and `data.yaml`. | No | Keep. |
| `Dataset/reports/` | KEEP/RESEARCH | Documentation, reconciliation, and audit logs. | No | Keep (except `C:\Users\...` paths). |
| `Dataset/samples/` & `professor_samples/` | KEEP/DEMO | Rendered visualization examples. | No | Keep. |
| `Dataset/annotations/` & `Dataset/images/` | REMOVE | Empty directories created by previous split attempts. | Yes | Delete folders. |
| `Dataset.zip` | REMOVE | Redundant 13.4MB archive of `Dataset/Dataset/`. | Yes | Delete file. |
| `dataset_tools/` | KEEP | Utility scripts (`pretrain_audit.py`, `split_dataset.py`, etc.) for reproducibility. | No | Keep. |
| `venv/` | GITIGNORE | Local Python virtual environment. | No | Already in `.gitignore`. |
| `NPR.mp4`, `NPR_detection.jpg`, `test.jpg` | KEEP/DEMO | Demo files (video is 3.2MB). | Yes (if unneeded) | Keep as examples. |
| `Predicted_output.jpg` | KEEP | Displayed directly in `README.md` banner. | No | Keep. |
| `xml_to_csv.py` | AUDIT | Legacy script mentioned in `README.md`. Obsolete in our new pipeline. | Yes | Decide if keeping for legacy support. |
| `.gitignore` | KEEP | Standard git ignore list. | No | Update with new exclusions. |
| `README.md` | KEEP | Main project documentation. | No | Update later to reflect new pipeline. |

## Specific Audit Checks

1. **venv/**: Safely excluded via `.gitignore` already.
2. **.vscode/**: Contains `settings.json` specific to your local machine's `venv` path. Should NOT be committed.
3. **Dataset.zip**: Redundant. The 13.4MB file is identical to the contents of `Dataset/Dataset/`.
4. **Demo media**: `Predicted_output.jpg` is actively used by `README.md`. The others are standalone demos.
5. **Code/**: This is the original repository's legacy YOLOv3 code. We are preparing for a modern Ultralytics YOLO pipeline, so this is technically obsolete but you may want to retain it for reference.
6. **dataset_tools/**: We actively use `split_dataset.py`, `find_unannotated.py`, `reconcile_dataset.py`, `pretrain_audit.py`, `draw_samples.py`, and `generate_prof_report.py`. The others are useful utility scripts.
7. **Absolute Paths**: Found `c:\Users\HP\Downloads\RM_Demo\Number-Plate-Detection-and-Recognition` hardcoded in `Dataset/DATASET_REPORT.md`. This should be changed to a relative path before committing.
8. **Secrets/API Keys**: A `grep` check found no raw API keys or passwords. (A `token` variable exists in `Download_Weights.py`, but it is safely requesting a token from an API).
9. **README.md Links**: If you remove `Predicted_output.jpg`, the banner image will break. If you remove `xml_to_csv.py`, the instructions in section 3.1 will be invalid.

---

### A. Files safe to remove
- `Dataset.zip`
- `Dataset/annotations/` (empty folder)
- `Dataset/images/` (empty folder)

### B. Files that should be added to .gitignore
- `.vscode/`

### C. Files that should remain
- `Dataset/Dataset/`
- `Dataset/processed_dataset/`
- `Dataset/reports/`
- `Dataset/samples/`
- `Dataset/professor_samples/`
- `dataset_tools/`
- `Predicted_output.jpg`
- `README.md`

### D. Files that need my decision
- `Code/` (Legacy YOLOv3 scripts)
- `xml_to_csv.py` (Legacy conversion script)
- `NPR.mp4`, `NPR_detection.jpg`, `test.jpg` (Demo files)

### E. Recommended final repository structure
```text
.
├── .github/
├── .gitignore
├── README.md
├── Predicted_output.jpg
├── Dataset/
│   ├── Dataset/ (raw)
│   ├── processed_dataset/ (YOLO split)
│   ├── reports/
│   ├── samples/
│   └── professor_samples/
└── dataset_tools/
    └── *.py (pipeline scripts)
```
*(With `Code/`, `xml_to_csv.py`, and other demos either deleted or moved to a legacy/demo folder)*
