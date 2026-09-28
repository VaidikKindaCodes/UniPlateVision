import os
import pathlib
import csv
import numpy as np
import cv2
from ultralytics import YOLO

model_path = r'runs/detect/runs/detect/v1_yolov8n/weights/best.pt'
test_img_dir = pathlib.Path(r'Dataset/processed_dataset/images/test')
test_lbl_dir = pathlib.Path(r'Dataset/processed_dataset/labels/test')
report_dir = pathlib.Path(r'Dataset/reports')
report_dir.mkdir(parents=True, exist_ok=True)

model = YOLO(model_path)

def compute_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - inter + 1e-6
    return inter / union

results_data = []
test_images = sorted(list(test_img_dir.glob('*.*')))

total_gt = 0
total_pred = 0
total_tp = 0
total_fp = 0
total_fn = 0
all_matched_ious = []
all_matched_confs = []

images_fp = []
images_fn = []
images_multi = []

for img_path in test_images:
    img = cv2.imread(str(img_path))
    h, w = img.shape[:2]
    
    lbl_path = test_lbl_dir / (img_path.stem + '.txt')
    gt_boxes = []
    if lbl_path.exists():
        with open(lbl_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    cx, cy, bw, bh = [float(x) for x in parts[1:5]]
                    x1 = (cx - bw/2) * w
                    y1 = (cy - bh/2) * h
                    x2 = (cx + bw/2) * w
                    y2 = (cy + bh/2) * h
                    gt_boxes.append([x1, y1, x2, y2])
                    
    # Predict
    res = model.predict(source=str(img_path), imgsz=640, device=0, verbose=False)[0]
    preds = []
    for b in res.boxes:
        conf = float(b.conf[0])
        coords = b.xyxy[0].tolist()
        preds.append({'box': coords, 'conf': conf})
        
    preds = sorted(preds, key=lambda x: x['conf'], reverse=True)
    
    matched_gt = [False] * len(gt_boxes)
    matched_ious = []
    pred_confs = [p['conf'] for p in preds]
    
    tp = 0
    fp = 0
    
    for p in preds:
        p_box = p['box']
        best_iou = 0.0
        best_gt_idx = -1
        for i, g_box in enumerate(gt_boxes):
            if not matched_gt[i]:
                iou = compute_iou(p_box, g_box)
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = i
                    
        if best_iou >= 0.50 and best_gt_idx != -1:
            matched_gt[best_gt_idx] = True
            tp += 1
            matched_ious.append(round(best_iou, 4))
            all_matched_ious.append(best_iou)
            all_matched_confs.append(p['conf'])
        else:
            fp += 1
            
    fn = len(gt_boxes) - tp
    
    total_gt += len(gt_boxes)
    total_pred += len(preds)
    total_tp += tp
    total_fp += fp
    total_fn += fn
    
    if fp > 0:
        images_fp.append(img_path.name)
    if fn > 0:
        images_fn.append(img_path.name)
    if len(preds) > 1:
        images_multi.append(img_path.name)
        
    results_data.append({
        'image_name': img_path.name,
        'ground_truth_count': len(gt_boxes),
        'prediction_count': len(preds),
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn,
        'matched_IoUs': matched_ious,
        'prediction_confidences': [round(c, 4) for c in pred_confs],
        'notes': 'possible unannotated object / requires visual verification' if fp > 0 else ''
    })

# Write CSV
csv_path = report_dir / 'v1_error_analysis.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'image_name', 'ground_truth_count', 'prediction_count',
        'true_positives', 'false_positives', 'false_negatives',
        'matched_IoUs', 'prediction_confidences', 'notes'
    ])
    writer.writeheader()
    for row in results_data:
        r = row.copy()
        r['matched_IoUs'] = str(r['matched_IoUs'])
        r['prediction_confidences'] = str(r['prediction_confidences'])
        writer.writerow(r)

# Write Markdown
md_path = report_dir / 'v1_error_analysis.md'
avg_iou = float(np.mean(all_matched_ious)) if all_matched_ious else 0.0
min_iou = float(np.min(all_matched_ious)) if all_matched_ious else 0.0
min_conf = float(np.min(all_matched_confs)) if all_matched_confs else 0.0

with open(md_path, 'w', encoding='utf-8') as f:
    f.write('# Version 1 Model Error Analysis Report\n\n')
    f.write('## Summary Metrics\n')
    f.write(f'- **Total Ground Truth Instances:** {total_gt}\n')
    f.write(f'- **Total Predictions:** {total_pred}\n')
    f.write(f'- **Total True Positives (IoU >= 0.50):** {total_tp}\n')
    f.write(f'- **Total False Positives:** {total_fp}\n')
    f.write(f'- **Total False Negatives:** {total_fn}\n')
    f.write(f'- **Average IoU of Matched Detections:** {avg_iou:.4f}\n')
    f.write(f'- **Lowest Matched IoU:** {min_iou:.4f}\n')
    f.write(f'- **Lowest-Confidence Matched Detection:** {min_conf:.4f}\n')
    f.write(f'- **Images Containing False Positives:** {images_fp}\n')
    f.write(f'- **Images Containing False Negatives:** {images_fn}\n')
    f.write(f'- **Images with Multiple Detections:** {images_multi}\n\n')
    
    f.write('## Per-Image Error Analysis\n\n')
    f.write('| Image Name | GT Count | Pred Count | TP | FP | FN | Matched IoUs | Prediction Confidences | Notes |\n')
    f.write('|---|---|---|---|---|---|---|---|---|\n')
    for r in results_data:
        ious_str = ', '.join([str(x) for x in r['matched_IoUs']]) if r['matched_IoUs'] else '-'
        confs_str = ', '.join([str(x) for x in r['prediction_confidences']]) if r['prediction_confidences'] else '-'
        note = r['notes']
        f.write(f"| {r['image_name']} | {r['ground_truth_count']} | {r['prediction_count']} | {r['true_positives']} | {r['false_positives']} | {r['false_negatives']} | {ious_str} | {confs_str} | {note} |\n")

print('Successfully created CSV and MD error analysis reports.')
print(f'Total GT: {total_gt}, Total Pred: {total_pred}, TP: {total_tp}, FP: {total_fp}, FN: {total_fn}')
print(f'Avg IoU: {avg_iou:.4f}, Min IoU: {min_iou:.4f}, Min Conf: {min_conf:.4f}')
print(f'FP Images: {images_fp}')
print(f'FN Images: {images_fn}')
print(f'Multi Detections: {images_multi}')
