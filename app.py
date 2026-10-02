"""Streamlit app.  Run:  python -m streamlit run app.py"""
import os, tempfile
from pathlib import Path

import cv2
import joblib
import pandas as pd
import streamlit as st

from common import CLASSES, SIZES, features, preprocess

BASE = Path(__file__).resolve().parent
OUT, DATA = BASE / "outputs", BASE / "data"

st.set_page_config(page_title="Parkinson Drawing Test", page_icon="🌀", layout="wide")
st.title("🌀 Parkinson's Detection from Hand-drawn Spiral & Wave")
st.warning("⚠️ শুধুমাত্র শিক্ষামূলক ডেমো। চিকিৎসকের রোগনির্ণয়ের বিকল্প নয়।")

tab1, tab2 = st.tabs(["🔍 Prediction", "📊 Project Results"])

with tab1:
    kind = st.radio("ছবির ধরন", ["spiral", "wave"], horizontal=True)
    mp = OUT / f"best_{kind}.joblib"
    if not mp.exists():
        st.error("মডেল পাওয়া যায়নি। আগে `python train.py` চালান।")
        st.stop()
    try:
        model = joblib.load(mp)
    except Exception as e:
        st.error(f"মডেল লোড হয়নি। `python train.py` চালিয়ে নতুন করে বানান। ({e})")
        st.stop()

    src = st.radio("ছবির উৎস", ["নিজের ছবি আপলোড", "ডেটাসেটের নমুনা"], horizontal=True)
    path, truth, tmp = None, None, None
    if src == "নিজের ছবি আপলোড":
        up = st.file_uploader("ছবি (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if up is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(up.name).suffix) as t:
                t.write(up.getbuffer())
            path = tmp = t.name
    else:
        files = sorted((DATA / kind / "testing").glob("*/*.png"))
        pick = st.selectbox("নমুনা বেছে নিন", files, format_func=lambda p: f"{p.parent.name}/{p.name}")
        if pick:
            path, truth = str(pick), pick.parent.name

    if path:
        try:
            orig = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            b = preprocess(path, SIZES[kind])
            p = model.predict_proba(features(b).reshape(1, -1))[0]
        except Exception as e:
            st.error(f"ছবিটা প্রসেস করা যায়নি: {e}")
            st.stop()
        finally:
            if tmp and os.path.exists(tmp):
                os.remove(tmp)
        c1, c2, c3 = st.columns(3)
        c1.image(orig, caption="ইনপুট ছবি", width="stretch")
        c2.image(b, caption="প্রসেস করা ছবি", width="stretch")
        with c3:
            if p[1] >= 0.5:
                st.error(f"### পারকিনসন্সের ঝুঁকি\n**{p[1]*100:.1f}%**")
            else:
                st.success(f"### সুস্থ / কম ঝুঁকি\nপারকিনসন্স সম্ভাবনা **{p[1]*100:.1f}%**")
            st.progress(float(p[1]))
            if truth:
                st.caption(f"আসল লেবেল (ডেটাসেটে): {truth}")

with tab2:
    rp = OUT / "results.csv"
    if rp.exists():
        st.subheader("মডেল তুলনা")
        st.dataframe(pd.read_csv(rp), width="stretch")
        st.caption("subject_wise_acc = একই রোগীর ছবি train/test-এ না মিশিয়ে কঠোর যাচাই (বেশি বাস্তবসম্মত)।")
    cols = st.columns(2)
    for i, (f, cap) in enumerate([("samples.png", "ডেটার নমুনা"), ("comparison.png", "মডেল তুলনা"),
                                  ("confusion_spiral.png", "Confusion Matrix - Spiral"),
                                  ("confusion_wave.png", "Confusion Matrix - Wave")]):
        if (OUT / f).exists():
            cols[i % 2].image(str(OUT / f), caption=cap)
