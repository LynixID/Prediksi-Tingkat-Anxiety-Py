# Import library yang diperlukan
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import mean_absolute_error

# Konfigurasi tampilan halaman
st.set_page_config(layout="wide", page_title="Prediksi Harga Hotel")

# Fungsi untuk memuat dan membersihkan data
def muat_data():
    data = pd.read_csv("booking_hotel.csv", encoding="latin1")
    data.columns = data.columns.str.strip()
    data['Room Price'] = data['Room Price (in BDT or any other currency)'].str.replace("[^\d]", "", regex=True).astype(float)
    return data.dropna(subset=['Room Price'])

# Memuat dataset
dataset = muat_data()

# Konfigurasi sidebar
st.sidebar.image("image.jpg", width=200)
st.sidebar.title("🏨 Menu Navigasi")
st.sidebar.markdown("---")

# Menu sidebar
selected = st.sidebar.selectbox(
    "Pilih Menu",
    ["Beranda", "Dataset", "Visualisasi", "Prediksi"],
)

# Informasi di sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📱 Informasi Aplikasi")
st.sidebar.info("Aplikasi ini menggunakan machine learning dengan algoritma Random Forest Regressor untuk memprediksi harga kamar hotel.")
st.sidebar.markdown("### 📊 Statistik Data")
st.sidebar.metric("Total Data", f"{len(dataset):,} baris")

# Fungsi untuk halaman beranda
def beranda():
    st.title("🏢 Aplikasi Prediksi Harga Hotel")
    st.markdown("---")
    
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("""
        ### Selamat Datang di Aplikasi Prediksi Harga Hotel!
        
        Aplikasi ini membantu memperkirakan harga kamar hotel berdasarkan beberapa faktor penting seperti:
        - 📍 Lokasi Hotel
        - 🛏️ Jenis Kamar
        - 🛋️ Tipe Tempat Tidur
        """)
        
        st.info("""
        ### 🎯 Fitur Utama:
        1. **Dataset**: Melihat dan mengeksplorasi data hotel yang tersedia
        2. **Visualisasi**: Analisis visual data harga hotel
        3. **Prediksi**: Prediksi harga berdasarkan preferensi Anda
        """)

        st.markdown("""
        ### 🤖 Teknologi Machine Learning yang Digunakan
        
        Aplikasi ini menggunakan algoritma **Random Forest Regressor**, sebuah model machine learning yang handal untuk prediksi harga. Beberapa keunggulan penggunaan Random Forest dalam aplikasi ini:
        
        1. **Akurasi Tinggi**: Mengkombinasikan multiple decision trees untuk hasil prediksi yang lebih akurat
        2. **Penanganan Data Kompleks**: Mampu menangani berbagai jenis variabel (lokasi, tipe kamar, dll.)
        3. **Ketahanan terhadap Outlier**: Tidak sensitif terhadap data ekstrem
        4. **Interpretasi Mudah**: Memberikan tingkat kepentingan fitur yang mudah dipahami
        """)

        st.markdown("""
        ### 📊 Dataset dan Sumber Data
        
        Dataset yang digunakan berasal dari [Kaggle - Hotel Dataset (Rates, Reviews, and Amenities)](https://www.kaggle.com/datasets/joyshil0599/hotel-dataset-rates-reviews-and-amenities5k). 
        
        **Mengapa memilih dataset ini?**
        - Kualitas Data: Berisi lebih dari 5,000 entri hotel dengan informasi lengkap
        - Keragaman: Mencakup berbagai lokasi, tipe kamar, dan fasilitas
        - Update Teratur: Dataset diperbarui secara berkala
        - Relevansi: Mencerminkan kondisi pasar hotel yang sebenarnya
        """)

        st.markdown("""
        ### 🎯 Tujuan dan Manfaat
        
        **Tujuan Pengembangan:**
        1. Memberikan estimasi harga hotel yang akurat untuk membantu perencanaan anggaran
        2. Menyediakan insight tentang faktor-faktor yang mempengaruhi harga hotel
        3. Memudahkan perbandingan harga berdasarkan berbagai kriteria
        
        **Manfaat bagi Pengguna:**
        1. Perencanaan Anggaran yang Lebih Baik
        2. Pengambilan Keputusan yang Lebih Informed
        3. Pemahaman Mendalam tentang Tren Harga Hotel
        """)

        st.markdown("""
        ### 🚀 Cara Menggunakan Website
        
        1. **Eksplorasi Dataset**
           - Kunjungi tab "Dataset" untuk melihat data mentah
           - Pelajari berbagai variabel yang tersedia
        
        2. **Analisis Visual**
           - Buka tab "Visualisasi" untuk melihat tren dan pola
           - Eksplorasi grafik interaktif untuk pemahaman lebih dalam
        
        3. **Prediksi Harga**
           - Pilih tab "Prediksi"
           - Masukkan preferensi Anda (lokasi, tipe kamar, dll.)
           - Dapatkan estimasi harga beserta tingkat akurasinya
        """)

    with col2:
        st.image("image.jpg", caption="Prediksi Harga Hotel", use_container_width=True)
        
        st.markdown("""
        ### 💡 Tips Penggunaan
        
        1. Mulai dengan mempelajari dataset untuk pemahaman awal
        2. Gunakan visualisasi untuk melihat tren harga
        3. Coba berbagai kombinasi di fitur prediksi
        4. Perhatikan tingkat akurasi prediksi
        """)

# Fungsi untuk halaman dataset
def dataset_view():
    st.title("📊 Dataset Hotel")
    st.markdown("---")
    
    col1, col2 = st.columns([3,1])
    with col1:
        st.dataframe(dataset, use_container_width=True)
    with col2:
        st.metric("Jumlah Data", f"{dataset.shape[0]:,}")
        st.metric("Jumlah Kolom", f"{dataset.shape[1]}")
        
        st.markdown("### 📈 Ringkasan Statistik")
        st.write("Harga Terendah:", f"Rp {dataset['Room Price'].min():,.2f}")
        st.write("Harga Tertinggi:", f"Rp {dataset['Room Price'].max():,.2f}")
        st.write("Harga Rata-rata:", f"Rp {dataset['Room Price'].mean():,.2f}")

# Fungsi untuk halaman visualisasi
def visualisasi():
    st.title("📈 Visualisasi Data")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribusi Harga", "📍 Harga per Lokasi", "🛏️ Analisis Kamar", "⭐ Rating Hotel"])
    
    with tab1:
        st.markdown("### Distribusi Harga Kamar Hotel")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.histplot(dataset["Room Price"], kde=True, ax=ax1)
        ax1.set_title("Distribusi Harga Kamar")
        st.pyplot(fig1)
        
    with tab2:
        st.markdown("### Perbandingan Harga Berdasarkan Lokasi")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=dataset, x="Location", y="Room Price", ax=ax2)
        plt.xticks(rotation=45)
        ax2.set_title("Harga Kamar Berdasarkan Lokasi")
        st.pyplot(fig2)
    
    with tab3:
        st.markdown("### Analisis Harga Berdasarkan Tipe Kamar dan Tempat Tidur")
        
        col1, col2 = st.columns(2)
        
        with col1:
            avg_room_price = dataset.groupby("Room Type")["Room Price"].mean().sort_values(ascending=True)
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            avg_room_price.plot(kind='barh', ax=ax3)
            ax3.set_title("Rata-rata Harga per Jenis Kamar")
            ax3.set_xlabel("Harga (Rp)")
            plt.tight_layout()
            st.pyplot(fig3)
        
        with col2:
            avg_bed_price = dataset.groupby("Bed Type")["Room Price"].mean().sort_values(ascending=True)
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            avg_bed_price.plot(kind='barh', ax=ax4)
            ax4.set_title("Rata-rata Harga per Tipe Tempat Tidur")
            ax4.set_xlabel("Harga (Rp)")
            plt.tight_layout()
            st.pyplot(fig4)
        
        st.markdown("### 📊 Rangkuman Statistik")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.metric("Harga Tertinggi", f"Rp {dataset['Room Price'].max():,.2f}")
        with col4:
            st.metric("Harga Terendah", f"Rp {dataset['Room Price'].min():,.2f}")
        with col5:
            st.metric("Harga Rata-rata", f"Rp {dataset['Room Price'].mean():,.2f}")
    
    with tab4:
        st.markdown("### ⭐ Line Chart Rating Hotel")
        if "Rating" in dataset.columns:  # Pastikan kolom Rating ada
            sorted_dataset = dataset.sort_values(by="Hotel Name")  # Urutkan berdasarkan nama hotel
            fig5, ax5 = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=sorted_dataset, x="Hotel Name", y="Rating", ax=ax5, marker="o")
            ax5.set_title("Rating Hotel")
            ax5.set_xlabel("Nama Hotel")
            ax5.set_ylabel("Rating")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig5)
        else:
            st.error("Kolom 'Rating' tidak ditemukan dalam dataset!")

# Fungsi untuk halaman prediksi
def prediksi():
    st.title("🔮 Prediksi Harga Hotel")
    st.markdown("---")
    
    # Penjelasan cara kerja prediksi
    st.markdown("""
    ### ℹ️ Cara Kerja Prediksi:
    1. Model mempelajari pola dari dataset yang berisi data historis harga hotel
    2. Prediksi dilakukan berdasarkan 3 faktor utama:
        - Lokasi hotel yang dipilih
        - Jenis kamar yang diinginkan
        - Tipe tempat tidur yang tersedia
    3. Model akan menganalisis data historis untuk menemukan harga yang paling sesuai
    """)
    
    col1, col2 = st.columns([1,1])
    
    with col1:
        st.markdown("### Parameter Input")
        lokasi = st.selectbox("📍 Lokasi", dataset["Location"].unique())
        jenis_kamar = st.selectbox("🛏️ Jenis Kamar", dataset["Room Type"].unique())
        jenis_tempat_tidur = st.selectbox("🛋️ Jenis Tempat Tidur", dataset["Bed Type"].unique())
        
        st.markdown("""
        ### 💡 Tips Penggunaan Hasil Prediksi:
        1. Gunakan range prediksi sebagai patokan dalam merencanakan anggaran
        2. Perhatikan nilai MAE untuk memahami tingkat ketidakpastian prediksi
        3. Nilai R² dapat membantu Anda menilai keandalan prediksi
        4. Lakukan beberapa kali prediksi dengan kombinasi berbeda untuk perbandingan
        """)
        
        # Tambahkan tombol untuk melakukan prediksi
        predict_button = st.button("Prediksi Harga")
        
    with col2:
        st.markdown("### Hasil Prediksi")
        
        if predict_button:
            # [Kode prediksi yang sama...]
            X = dataset[["Location", "Room Type", "Bed Type"]]
            y = dataset["Room Price"]
            
            X_encoded = pd.get_dummies(X)
            
            X_train, X_test, y_train, y_test = train_test_split(
                X_encoded, 
                y, 
                test_size=0.2, 
                random_state=None
            )
            
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=1,
                random_state=None
            )
            model.fit(X_train, y_train)
            
            data_input = pd.DataFrame([[lokasi, jenis_kamar, jenis_tempat_tidur]], 
                                    columns=["Location", "Room Type", "Bed Type"])
            data_input_encoded = pd.get_dummies(data_input)
            
            missing_cols = set(X_encoded.columns) - set(data_input_encoded.columns)
            for col in missing_cols:
                data_input_encoded[col] = 0
            data_input_encoded = data_input_encoded[X_encoded.columns]
            
            hasil_prediksi = model.predict(data_input_encoded)
            
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2_score = model.score(X_test, y_test)
            
            st.metric("💰 Prediksi Harga", f"Rp {hasil_prediksi[0]:,.2f}")
            st.metric("📉 Mean Absolute Error", f"±Rp {mae:,.2f}")
            st.metric("📊 R² Score", f"{r2_score:.4f}")
            
            lower_bound = hasil_prediksi[0] - mae
            upper_bound = hasil_prediksi[0] + mae
            st.info(f"Range Prediksi: Rp {lower_bound:,.2f} - Rp {upper_bound:,.2f}")
            
            st.markdown("""
            ### 📋 Penjelasan Detail Hasil Prediksi:
            
            #### 1. 💰 Prediksi Harga
            - Ini adalah estimasi harga kamar hotel berdasarkan pilihan Anda
            - Harga ini merupakan hasil analisis dari pola data historis
            - Prediksi ini mempertimbangkan lokasi, jenis kamar, dan tipe tempat tidur yang Anda pilih
            
            #### 2. 📉 Mean Absolute Error (MAE)
            - MAE menunjukkan rata-rata selisih antara prediksi dengan harga sebenarnya
            - Semakin kecil nilai MAE, semakin akurat prediksi
            - Contoh: Jika MAE Rp 100.000, artinya prediksi bisa meleset ±Rp 100.000 dari harga sebenarnya
            
            #### 3. 📊 R² Score (Coefficient of Determination)
            - Nilai antara 0 hingga 1 yang menunjukkan seberapa baik model memprediksi
            - Semakin mendekati 1, semakin akurat model
            - Contoh interpretasi:
              - R² = 0.8 berarti model menjelaskan 80% variasi harga
              - R² = 0.5 berarti model menjelaskan 50% variasi harga
              - R² < 0.3 menunjukkan prediksi kurang akurat
            
            #### 4. 📍 Range Prediksi
            - Rentang harga yang mungkin berdasarkan MAE
            - Harga sebenarnya kemungkinan besar berada dalam rentang ini
            - Range ini memberikan gambaran tentang fluktuasi harga yang mungkin terjadi
            """)

# Router halaman
if selected == "Beranda":
    beranda()
elif selected == "Dataset":
    dataset_view()
elif selected == "Visualisasi":
    visualisasi()
elif selected == "Prediksi":
    prediksi()