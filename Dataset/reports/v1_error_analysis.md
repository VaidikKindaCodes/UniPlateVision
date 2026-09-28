# Version 1 Model Error Analysis Report

## Summary Metrics
- **Total Ground Truth Instances:** 25
- **Total Predictions:** 26
- **Total True Positives (IoU >= 0.50):** 24
- **Total False Positives:** 2
- **Total False Negatives:** 1
- **Average IoU of Matched Detections:** 0.8621
- **Lowest Matched IoU:** 0.5956
- **Lowest-Confidence Matched Detection:** 0.4312
- **Images Containing False Positives:** ['57.jpg', '75.jpg']
- **Images Containing False Negatives:** ['57.jpg']
- **Images with Multiple Detections:** ['100.jpg', '103.jpg', '57.jpg', '75.jpg']

## Per-Image Error Analysis

| Image Name | GT Count | Pred Count | TP | FP | FN | Matched IoUs | Prediction Confidences | Notes |
|---|---|---|---|---|---|---|---|---|
| 100.jpg | 2 | 2 | 2 | 0 | 0 | 0.9264, 0.9713 | 0.9554, 0.9247 |  |
| 103.jpg | 2 | 2 | 2 | 0 | 0 | 0.9378, 0.8617 | 0.9476, 0.903 |  |
| 135.jpg | 1 | 1 | 1 | 0 | 0 | 0.5956 | 0.7894 |  |
| 139.jpg | 1 | 1 | 1 | 0 | 0 | 0.8889 | 0.9243 |  |
| 141.jpg | 1 | 1 | 1 | 0 | 0 | 0.9431 | 0.903 |  |
| 150.jpg | 1 | 1 | 1 | 0 | 0 | 0.9636 | 0.9729 |  |
| 160.jpg | 1 | 1 | 1 | 0 | 0 | 0.8231 | 0.8373 |  |
| 169.jpg | 1 | 1 | 1 | 0 | 0 | 0.8872 | 0.8936 |  |
| 19.jpg | 1 | 1 | 1 | 0 | 0 | 0.9597 | 0.9217 |  |
| 190.jpg | 1 | 1 | 1 | 0 | 0 | 0.9377 | 0.9232 |  |
| 196.jpg | 1 | 1 | 1 | 0 | 0 | 0.7721 | 0.9039 |  |
| 199.jpg | 1 | 1 | 1 | 0 | 0 | 0.8491 | 0.8331 |  |
| 24.jpg | 1 | 1 | 1 | 0 | 0 | 0.8936 | 0.8423 |  |
| 42.jpg | 1 | 1 | 1 | 0 | 0 | 0.8443 | 0.9039 |  |
| 45.jpg | 1 | 1 | 1 | 0 | 0 | 0.8525 | 0.8602 |  |
| 51.jpg | 1 | 1 | 1 | 0 | 0 | 0.7895 | 0.8736 |  |
| 57.jpg | 2 | 2 | 1 | 1 | 1 | 0.8595 | 0.9217, 0.3571 | possible unannotated object / requires visual verification |
| 7.jpg | 1 | 1 | 1 | 0 | 0 | 0.7083 | 0.4312 |  |
| 71.jpg | 1 | 1 | 1 | 0 | 0 | 0.883 | 0.9423 |  |
| 75.jpg | 1 | 2 | 1 | 1 | 0 | 0.7948 | 0.9017, 0.8903 | possible unannotated object / requires visual verification |
| 86.jpg | 1 | 1 | 1 | 0 | 0 | 0.8812 | 0.9216 |  |
| 97.jpg | 1 | 1 | 1 | 0 | 0 | 0.8672 | 0.8771 |  |
