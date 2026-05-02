# Dataset Evaluation Guide

## Kahan se Dataset Download Karo

### Option 1 — Best for Indian Scams (Recommended)
**Kaggle — SMS Spam Collection Dataset**
- URL: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
- File: `spam.csv`
- Free download (Kaggle account chahiye)

### Option 2 — Indian Fraud Specific
**Kaggle — Indian Fraud SMS Dataset**
- URL: https://www.kaggle.com/datasets/shubham2703/fraud-sms-dataset
- File: `fraud_sms.csv`

### Option 3 — Phishing URLs
**Kaggle — Phishing URL Dataset**
- URL: https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls
- File: `phishing_site_urls.csv`

## Kahan Paste Karo

Downloaded file yahan paste karo:
```
backend/evaluation/datasets/
```

## Supported File Formats
- CSV with columns: `text`, `label`  (label: spam/ham or 1/0)
- CSV with columns: `message`, `category`
- CSV with columns: `sms`, `type`

Script automatically detect kar lega format.
