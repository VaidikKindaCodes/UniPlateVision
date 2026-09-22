import os
import shutil
import random

source_samples_dir = 'Dataset/samples/annotated'
prof_samples_dir = 'Dataset/professor_samples'
md_out = 'Dataset/PROFESSOR_DATASET_SUMMARY.md'
html_out = 'Dataset/PROFESSOR_DATASET_SUMMARY.html'

os.makedirs(prof_samples_dir, exist_ok=True)

# Select 12 samples
all_samples = [f for f in os.listdir(source_samples_dir) if f.endswith(('.jpg', '.png'))]
random.seed(42)
selected_samples = random.sample(all_samples, min(12, len(all_samples)))

# Copy samples
for s in selected_samples:
    shutil.copy2(os.path.join(source_samples_dir, s), os.path.join(prof_samples_dir, s))

# Write Markdown
md_content = f"""# Automatic Number Plate Recognition: Dataset Presentation

## PAGE 1 — Dataset Overview
- **Project**: Automatic Number Plate Recognition
- **Dataset Source**: Local vehicle image dataset
- **Raw Images**: 237
- **Annotated Images**: 210
- **License Plate Annotations**: 226
- **Unannotated Images**: 27
- **Annotation Class**: `plate`
- **Status Check**: READY WITH MANUAL REVIEW (27 unannotated images set aside)

## PAGE 2 — Dataset Preparation
**Preparation Pipeline:**
```
Raw Indian vehicle images
        ↓
Annotation inspection
        ↓
Data validation
        ↓
Duplicate/corrupt check
        ↓
YOLO annotation conversion
        ↓
Train / Validation / Test split
```

**Final Split:**
- **Train**: 168
- **Validation**: 20
- **Test**: 22

## PAGE 3 — Sample Images
Here are sample images from our dataset with the license-plate bounding boxes visible:
"""
for s in selected_samples:
    md_content += f"![{s}](professor_samples/{s})\n"

md_content += """
## PAGE 4 — Annotation Example
The bounding boxes in the sample images above identify the precise location of the license plate within the frame. This spatial information, converted into normalized YOLO format (x_center, y_center, width, height), serves as the ground-truth for object detection training.

## PAGE 5 — Current Status & Next Step

### COMPLETED:
- Dataset collected/obtained
- Dataset inspected
- Annotations validated
- YOLO labels prepared
- Train/validation/test split created
- Dataset quality checks performed

### NEXT PLANNED:
- Fine-tune a pretrained YOLO detector
- Evaluate detection performance
- Later add surveillance/CCTV-style data and study adaptation to that environment
"""

with open(md_out, 'w', encoding='utf-8') as f:
    f.write(md_content)

# Write HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automatic Number Plate Recognition: Dataset Presentation</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .page {{
            background: #fff;
            padding: 40px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #2980b9;
            border-left: 4px solid #2980b9;
            padding-left: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-box {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }}
        .stat-box.warning {{
            background: #fdf2e9;
            border: 1px solid #e67e22;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .pipeline {{
            background: #2c3e50;
            color: #fff;
            padding: 20px;
            border-radius: 6px;
            font-family: monospace;
            text-align: center;
            line-height: 2;
            font-size: 16px;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }}
        .gallery img {{
            width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .status-section {{
            display: flex;
            gap: 20px;
        }}
        .status-box {{
            flex: 1;
            padding: 20px;
            border-radius: 6px;
        }}
        .completed {{
            background: #e8f8f5;
            border: 1px solid #1abc9c;
        }}
        .planned {{
            background: #ebf5fb;
            border: 1px solid #3498db;
        }}
        ul {{
            padding-left: 20px;
        }}
    </style>
</head>
<body>
    <h1>Automatic Number Plate Recognition</h1>

    <div class="page">
        <h2>Dataset Overview</h2>
        <div class="stats-grid">
            <div class="stat-box"><div class="stat-value">237</div>Raw Images</div>
            <div class="stat-box"><div class="stat-value">210</div>Annotated Images</div>
            <div class="stat-box"><div class="stat-value">226</div>License Plate Annotations</div>
            <div class="stat-box warning">
                <div class="stat-value" style="color: #e67e22;">27</div>Unannotated Images
                <br><small>READY WITH MANUAL REVIEW</small>
            </div>
            <div class="stat-box"><div class="stat-value">plate</div>Annotation Class</div>
        </div>
    </div>

    <div class="page">
        <h2>Dataset Preparation</h2>
        <div class="pipeline">
            Raw Indian vehicle images<br>↓<br>Annotation inspection<br>↓<br>Data validation<br>↓<br>Duplicate/corrupt check<br>↓<br>YOLO annotation conversion<br>↓<br>Train / Validation / Test split
        </div>
        <br>
        <div class="stats-grid">
            <div class="stat-box"><div class="stat-value">168</div>Train</div>
            <div class="stat-box"><div class="stat-value">20</div>Validation</div>
            <div class="stat-box"><div class="stat-value">22</div>Test</div>
        </div>
    </div>

    <div class="page">
        <h2>Sample Images</h2>
        <p>Actual images from our dataset with ground-truth license-plate bounding boxes visible:</p>
        <div class="gallery">
"""
for s in selected_samples:
    html_content += f'            <img src="professor_samples/{s}" alt="{s}">\n'

html_content += """        </div>
    </div>

    <div class="page">
        <h2>Annotation Example</h2>
        <div style="display: flex; gap: 20px; margin-bottom: 20px;">
"""
for s in selected_samples[:2]:
    html_content += f'            <img src="professor_samples/{s}" style="width: 48%; border-radius: 6px;" alt="{s}">\n'

html_content += """        </div>
        <p>The bounding boxes in the sample images above identify the precise location of the license plate within the frame. This spatial information, converted into normalized YOLO format (x_center, y_center, width, height), serves as the ground-truth for object detection training.</p>
    </div>

    <div class="page">
        <h2>Current Status & Next Step</h2>
        <div class="status-section">
            <div class="status-box completed">
                <h3 style="color: #16a085; margin-top: 0;">COMPLETED</h3>
                <ul>
                    <li>Dataset collected/obtained</li>
                    <li>Dataset inspected</li>
                    <li>Annotations validated</li>
                    <li>YOLO labels prepared</li>
                    <li>Train/validation/test split created</li>
                    <li>Dataset quality checks performed</li>
                </ul>
            </div>
            <div class="status-box planned">
                <h3 style="color: #2980b9; margin-top: 0;">NEXT PLANNED</h3>
                <ul>
                    <li>Fine-tune a pretrained YOLO detector</li>
                    <li>Evaluate detection performance</li>
                    <li>Later add surveillance/CCTV-style data and study adaptation to that environment</li>
                </ul>
            </div>
        </div>
    </div>

</body>
</html>
"""

with open(html_out, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Reports generated.")
