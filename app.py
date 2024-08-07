import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load dataset dari file Excel
df = pd.read_csv('Liverdiease.csv')

# Menampilkan ukuran dataset sebelum dirapihkan
df_shape_before = df.shape

# Merapihkan dataset
df = df.dropna()  # Menghapus baris dengan nilai yang hilang
df = df.drop_duplicates()  # Menghapus duplikat

# Mengganti nama kolom untuk merapihkan
df.columns = df.columns.str.strip()  # Menghapus spasi di awal dan akhir nama kolom
df.columns = df.columns.str.replace(' ', '_')  # Mengganti spasi dengan underscore

df_shape_after = df.shape

# Load model and scaler
with open('liver_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# Function to predict liver disease
def predict_liver_disease(features):
    features = np.array(features).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)
    return 'Positif Penyakit Liver' if prediction == 1 else 'Negatif Penyakit Liver'

# Function to get prevention tips
def get_prevention_tips():
    return """
    **Halo Pengguna!**
    **Berikut Tips Pencegahan Penyakit Liver:**
    1. Kurangi konsumsi alkohol.
    2. Jaga pola makan sehat dan seimbang.
    3. Lakukan olahraga secara teratur.
    4. Hindari penggunaan obat-obatan tanpa resep dokter.
    5. Lakukan pemeriksaan kesehatan secara berkala.
    """

# Home Page
def home():
    st.title("LiverGuard: Aplikasi Deteksi Penyakit Liver")
    st.image("https://o.remove.bg/uploads/f42258e8-eb04-4b01-9bd1-6a6b4bbf84c6/LIVERGUARD__1___1_.jpg")
    st.write("Halo, selamat datang di LiverGuard!")
    st.write("Aplikasi yang membantu Anda mendeteksi penyakit liver dan memberikan tips pencegahan.")

# Login Page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "liver123":
            st.success("Login berhasil")
            st.session_state['logged_in'] = True
        else:
            st.error("Username atau password salah")

# Detection Page
def detection():
    st.title("Deteksi Penyakit Liver")
    gender = st.radio("Gender", ('Female', 'Male'))
    age = st.number_input("Age", 1, 100)
    tb = st.number_input("Total Bilirubin", 0.0, 100.0)
    db = st.number_input("Direct Bilirubin", 0.0, 100.0)
    alkphos = st.number_input("Alkaline Phosphotase", 0, 1000)
    sgpt = st.number_input("Alamine Aminotransferase", 0, 1000)
    sgot = st.number_input("Aspartate Aminotransferase", 0, 1000)
    tp = st.number_input("Total Proteins", 0.0, 10.0)
    alb = st.number_input("Albumin", 0.0, 10.0)
    agratio = st.number_input("Albumin and Globulin Ratio", 0.0, 10.0)
    
    if st.button("Prediksi"):
        features = [0 if gender == 'Female' else 1, age, tb, db, alkphos, sgpt, sgot, tp, alb, agratio]
        result = predict_liver_disease(features)
        st.success(result)
        st.write(get_prevention_tips())

# Data Page
def data_page():
    st.title("Dataset")
    st.write("Berikut adalah dataset yang digunakan dalam aplikasi ini:")
    st.write(f"Ukuran dataset sebelum dirapihkan: {df_shape_before[0]} baris dan {df_shape_before[1]} kolom.")
    st.write(f"Ukuran dataset setelah dirapihkan: {df_shape_after[0]} baris dan {df_shape_after[1]} kolom.")
    st.dataframe(df)

# Logout Page
def logout():
    st.session_state['logged_in'] = False
    st.success("Logout berhasil")
    st.success("Terimakasih telah mengunjungi Aplikasi LiverGuard, semoga Anda sehat selalu!")

# Main function
def main():
    st.sidebar.title("Dashboard")
    menu = st.sidebar.radio("Menu", ["Home", "Login", "Data", "Deteksi Penyakit Liver", "Logout"])
    
    # Apply background gradient
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to right, #96BBD2, #02457A);
        }
        .stButton > button {
            background-color: #6c757d;
            color: white;
        }
        footer {
            visibility: hidden;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    # Header and Footer
    if menu == "Home":
        home()
    elif menu == "Login":
        if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
            login()
        else:
            st.write("Anda sudah login.")
    elif menu == "Deteksi Penyakit Liver":
        if 'logged_in' in st.session_state and st.session_state['logged_in']:
            detection()
        else:
            st.warning("Silakan login terlebih dahulu.")
    elif menu == "Data":
        data_page()
    elif menu == "Logout":
        if 'logged_in' in st.session_state and st.session_state['logged_in']:
            logout()
        else:
            st.write("Anda belum login.")
    
    # Footer
    st.markdown("<h5 style='text-align: center; color: #728495;'>© 2024 LiverGuard</h5>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
