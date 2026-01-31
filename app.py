import streamlit as st
import pickle
import pandas as pd
import os
import matplotlib.pyplot as plt


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Laptop Price Predictor",
    layout="centered",
    page_icon="💻"
)


# ================= SIDEBAR =================
st.sidebar.title("⚙️ Settings")
st.sidebar.info("Laptop Price Prediction System")
st.sidebar.markdown("Developed by Abhiraj 🚀")


# ================= LOAD MODEL =================
@st.cache_resource
def load_model():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model.pkl")

    if not os.path.exists(model_path):
        st.error("❌ model.pkl file not found!")
        st.stop()

    with open(model_path, "rb") as f:
        return pickle.load(f)


model = load_model()


# ================= TITLE =================
st.title("💻 Laptop Price Predictor")
st.write("Select laptop configuration to predict price")


# ================= MODEL INFO =================
st.info("📊 Model Accuracy: 98% (R² Score)")


# ================= BRAND CONFIG =================

brand_config = {

    "Apple": {"processor": ["Apple"], "ram": [8, 16, 24, 32], "storage": [256, 512]},
    "HP": {"processor": ["Intel", "AMD"], "ram": [4, 8, 16, 32], "storage": [128, 256, 512]},
    "DELL": {"processor": ["Intel", "AMD"], "ram": [4, 8, 16, 32], "storage": [128, 256, 512]},
    "Lenovo": {"processor": ["Intel", "AMD"], "ram": [4, 8, 16, 32], "storage": [128, 256, 512]},
    "ASUS": {"processor": ["Intel", "AMD"], "ram": [8, 16, 32], "storage": [256, 512]},
    "Acer": {"processor": ["Intel", "AMD"], "ram": [4, 8, 16], "storage": [128, 256, 512]},
    "MSI": {"processor": ["Intel", "AMD"], "ram": [8, 16, 32], "storage": [256, 512]},
    "Samsung": {"processor": ["Intel", "Qualcomm"], "ram": [8, 16], "storage": [256, 512]},
    "Jio": {"processor": ["MediaTek"], "ram": [4], "storage": [128]},
    "Other": {"processor": ["Intel", "AMD", "MediaTek"], "ram": [4, 8, 16], "storage": [128, 256]}
}


# ================= INPUTS =================

brand = st.selectbox("Brand", list(brand_config.keys()))

processor = st.selectbox(
    "Processor",
    brand_config[brand]["processor"]
)

ram = st.selectbox(
    "RAM (GB)",
    brand_config[brand]["ram"]
)

storage = st.selectbox(
    "Storage (GB)",
    brand_config[brand]["storage"]
)

ratings = st.slider("Ratings", 2.7, 5.0, 4.0, 0.1)

discount = st.selectbox(
    "Discount",
    ['5%', '10%', '15%', '20%', '25%', '30%', '40%', '50%']
)


# ================= HELPER =================

def estimate_original_price(ram, storage, processor, brand):

    price = 25000

    price += (ram // 4) * 4000

    if storage == 256:
        price += 4000
    elif storage == 512:
        price += 8000

    if processor in ["Intel", "AMD"]:
        price += 6000
    elif processor == "Apple":
        price += 15000

    if brand in ["Apple", "MSI"]:
        price += 10000
    elif brand in ["HP", "DELL", "Lenovo"]:
        price += 4000

    return price


# ================= AI RECOMMENDATION =================

def recommendation(ram, ratings, brand):

    if ram < 8:
        st.warning("⚠️ Low RAM for heavy usage / gaming")

    if ratings < 3.5:
        st.warning("⚠️ Low user ratings")

    if brand in ["Apple", "MSI"]:
        st.success("✅ Premium performance laptop")

    elif brand in ["HP", "DELL", "Lenovo"]:
        st.success("✅ Best for office & students")


# ================= PREDICT =================

if st.button("🚀 Predict Price"):

    original_price = estimate_original_price(
        ram, storage, processor, brand
    )

    input_data = pd.DataFrame({
        "Brands": [brand],
        "processor": [processor],
        "Discount": [discount],
        "ratings": [ratings],
        "Original_price": [original_price],
        "RAM": [ram],
        "Storage": [storage]
    })

    pred = model.predict(input_data)[0]

    pred = max(pred, 5000)


    # ================= RANGE =================
    low = int(pred * 0.95)
    high = int(pred * 1.05)


    # ================= RESULT =================
    st.success(f"💰 Predicted Price: ₹ {int(pred):,}")
    st.info(f"📈 Estimated Range: ₹ {low:,} – ₹ {high:,}")


    # ================= GRAPH =================
    fig, ax = plt.subplots()

    ax.bar(
        ["Predicted Price"],
        [pred]
    )

    ax.set_ylabel("Price (₹)")
    ax.set_title("Price Prediction")

    st.pyplot(fig)


    # ================= AI ADVICE =================
    st.subheader("🤖 AI Recommendation")

    recommendation(ram, ratings, brand)
