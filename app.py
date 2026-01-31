import streamlit as st
import pickle
import pandas as pd

# ================= LOAD MODEL =================
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Laptop Price Predictor", layout="centered")

st.title("💻 Laptop Price Predictor")
st.write("Select brand-wise configuration to predict price")

# ================= BRAND CONFIG =================

brand_config = {

    "Apple": {
        "processor": ["Apple"],
        "ram": [8, 16, 24, 32],
        "storage": [256, 512]
    },

    "HP": {
        "processor": ["Intel", "AMD"],
        "ram": [4, 8, 16, 32],
        "storage": [128, 256, 512]
    },

    "DELL": {
        "processor": ["Intel", "AMD"],
        "ram": [4, 8, 16, 32],
        "storage": [128, 256, 512]
    },

    "Lenovo": {
        "processor": ["Intel", "AMD"],
        "ram": [4, 8, 16, 32],
        "storage": [128, 256, 512]
    },

    "ASUS": {
        "processor": ["Intel", "AMD"],
        "ram": [8, 16, 32],
        "storage": [256, 512]
    },

    "Acer": {
        "processor": ["Intel", "AMD"],
        "ram": [4, 8, 16],
        "storage": [128, 256, 512]
    },

    "MSI": {
        "processor": ["Intel", "AMD"],
        "ram": [8, 16, 32],
        "storage": [256, 512]
    },

    "Samsung": {
        "processor": ["Intel", "Qualcomm"],
        "ram": [8, 16],
        "storage": [256, 512]
    },

    "Jio": {
        "processor": ["MediaTek"],
        "ram": [4],
        "storage": [128]
    },

    "Other": {
        "processor": ["Intel", "AMD", "MediaTek"],
        "ram": [4, 8, 16],
        "storage": [128, 256]
    }
}

# ================= INPUTS =================

brand = st.selectbox("Brand", list(brand_config.keys()))

# Auto options by brand
processor_list = brand_config[brand]["processor"]
ram_list = brand_config[brand]["ram"]
storage_list = brand_config[brand]["storage"]

processor = st.selectbox("Processor", processor_list)

ram = st.selectbox("RAM (GB)", ram_list)

storage = st.selectbox("Storage (GB)", storage_list)

ratings = st.slider("Ratings", 2.7, 5.0, 4.0, 0.1)

discount = st.selectbox("Discount", [
    '5%','10%','15%','20%','25%','30%','40%','50%'
])

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


# ================= PREDICT =================

if st.button("Predict Price"):

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

    prediction = model.predict(input_data)[0]

    prediction = max(prediction, 5000)

    st.success(f"💰 Predicted Laptop Price: ₹ {int(prediction):,}")