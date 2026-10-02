# Parkinson's রোগ শনাক্তকরণ: হাতে আঁকা Spiral ও Wave ছবি থেকে

## সবচেয়ে সহজ চালানো (Windows)
1. zip **Extract All** করুন।
2. ভেতরে **RUN_WINDOWS.bat** ডাবল-ক্লিক করুন।
3. এটা নিজে নিজে: লাইব্রেরি ইনস্টল -> মডেল train -> ব্রাউজারে app খোলা (http://localhost:8501)

Mac/Linux: টার্মিনালে `bash run_mac_linux.sh`

## হাতে চালাতে চাইলে (প্রজেক্ট ফোল্ডারের ভেতরে CMD খুলে)
```bash
pip install -r requirements.txt
python train.py
python -m streamlit run app.py
```
(ফোল্ডারে ঢুকতে: File Explorer-এর address bar-এ `cmd` লিখে Enter)

## ফাইল পরিচিতি
- `data/` - spiral ও wave ছবি (training/testing, healthy/parkinson)
- `common.py` - ছবি প্রসেস + feature বের করা
- `train.py` - ৪টা মডেল train, মূল্যায়ন, সেরা মডেল সেভ
- `app.py` - Streamlit ওয়েব অ্যাপ (ছবি আপলোড বা নমুনা বেছে prediction)
- `outputs/` - results.csv, চার্ট, সেভ করা মডেল

## পদ্ধতি
1. ছবি gray -> resize (spiral 128x128, wave 256x128) -> Otsu binarize
2. Feature: HOG + stroke পরিসংখ্যান (ink ratio, দৈর্ঘ্য, পুরুত্ব, বিস্তার)
3. মডেল: SVM, Logistic Regression, Random Forest, Gradient Boosting
4. 5-fold CV দিয়ে সেরা মডেল বাছাই (test দিয়ে নয়), তারপর test set-এ মূল্যায়ন
5. কঠোর যাচাই: GroupKFold (একই রোগীর ছবি train ও test-এ একসাথে যায় না)

## ফলাফল
| মডেল | Spiral test acc | Wave test acc |
|---|---|---|
| SVM (RBF) | 0.933 | 0.767 |
| Logistic Regression | 0.900 | 0.800 |
| Random Forest | 0.833 | 0.767 |
| Gradient Boosting | 0.833 | 0.733 |

রোগী-ভিত্তিক কঠোর যাচাইয়ে: Spiral ~0.70-0.81, Wave ~0.62-0.68 (এটাই বেশি বাস্তবসম্মত)।

## সীমাবদ্ধতা (রিপোর্টে লিখুন)
- test set মাত্র ৩০টি ছবি, তাই ১টা ছবিতেই accuracy ~৩.৩% বদলায়
- একই রোগীর ছবি train ও test দুটোতেই আছে (leakage), তাই সাধারণ test accuracy বেশি দেখায়
- ডেটা খুব ছোট; শুধু শিক্ষামূলক ডেমো, চিকিৎসা-নির্ণয় নয়
- ভবিষ্যৎ কাজ: data augmentation, CNN/transfer learning

## ডেটাসেট
Parkinson's Disease Spiral and Wave Drawings (Kaggle)
