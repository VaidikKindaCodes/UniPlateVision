import os
import pathlib
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

model_path = r'runs/detect/runs/detect/v1_yolov8n/weights/best.pt'
test_img_dir = pathlib.Path(r'Dataset/processed_dataset/images/test')
test_lbl_dir = pathlib.Path(r'Dataset/processed_dataset/labels/test')
out_dir = pathlib.Path(r'runs/detect/v1_error_visuals')
out_dir.mkdir(parents=True, exist_ok=True)

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

target_images = ['57.jpg', '75.jpg', '7.jpg', '135.jpg']

for img_name in target_images:
    img_path = test_img_dir / img_name
    lbl_path = test_lbl_dir / (pathlib.Path(img_name).stem + '.txt')
    
    img = cv2.imread(str(img_path))
    h, w = img.shape[:2]
    
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
                    
    res = model.predict(source=str(img_path), imgsz=640, device=0, verbose=False)[0]
    preds = []
    for b in res.boxes:
        conf = float(b.conf[0])
        coords = b.xyxy[0].tolist()
        preds.append({'box': coords, 'conf': conf})
        
    preds = sorted(preds, key=lambda x: x['conf'], reverse=True)
    
    # Calculate IoUs and match
    matched_gt = [False] * len(gt_boxes)
    pred_matches = []
    
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
            pred_matches.append({'match': True, 'iou': best_iou, 'gt_idx': best_gt_idx})
        else:
            # Check if there is any overlap with any GT box even if < 0.50
            any_iou = 0.0
            any_gt_idx = -1
            for i, g_box in enumerate(gt_boxes):
                iou = compute_iou(p_box, g_box)
                if iou > any_iou:
                    any_iou = iou
                    any_gt_idx = i
            pred_matches.append({'match': False, 'max_iou': any_iou, 'gt_idx': any_gt_idx})
            
    # Print details for inspection
    print(f'=== {img_name} ===')
    print(f'Dimensions: {w}x{h}')
    print(f'Ground Truth Boxes ({len(gt_boxes)}):')
    for i, g in enumerate(gt_boxes):
        print(f'  GT {i}: {g}')
    print(f'Predictions ({len(preds)}):')
    for i, p in enumerate(preds):
        pm = pred_matches[i]
        print(f'  Pred {i}: {p["box"]}, Conf: {p["conf"]:.4f}, Match Info: {pm}')
        
    # Draw Visualization: Side-by-Side (Left: Ground Truth, Right: Predictions)
    # Plus a combined view below
    
    img_gt = img.copy()
    img_pred = img.copy()
    
    # Draw GT on img_gt
    for i, g in enumerate(gt_boxes):
        x1, y1, x2, y2 = [int(v) for v in g]
        cv2.rectangle(img_gt, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img_gt, f'GT {i+1}', (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    # Draw Pred on img_pred
    for i, p in enumerate(preds):
        x1, y1, x2, y2 = [int(v) for v in p['box']]
        pm = pred_matches[i]
        if pm['match']:
            color = (255, 0, 0) # Blue for matched TP
            lbl = f'P{i+1}: {p["conf"]:.2f} (IoU:{pm["iou"]:.2f})'
        else:
            color = (0, 0, 255) # Red for FP / Low IoU
            max_iou = pm.get('max_iou', 0.0)
            lbl = f'P{i+1}: {p["conf"]:.2f} (maxIoU:{max_iou:.2f})'
            
        cv2.rectangle(img_pred, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img_pred, lbl, (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
    # Combine side-by-side
    header_gt = np.zeros((30, w, 3), dtype=np.uint8)
    cv2.putText(header_gt, "Ground Truth", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    header_pred = np.zeros((30, w, 3), dtype=np.uint8)
    cv2.putText(header_pred, "YOLOv8 V1 Predictions", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    panel_gt = np.vstack([header_gt, img_gt])
    panel_pred = np.vstack([header_pred, img_pred])
    
    combined = np.hstack([panel_gt, panel_pred])
    
    save_path = out_dir / f'visual_audit_{img_name}'
    cv2.imwrite(str(save_path), combined)
    print(f'Saved visualization to: {save_path}')

print("Completed visual audit script.")
