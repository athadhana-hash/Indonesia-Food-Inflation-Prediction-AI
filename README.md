# Prediksi Inflasi Makanan

Proyek ini bertujuan untuk memprediksi inflasi makanan di Indonesia menggunakan data harga komoditas pokok, data inflasi, dan data curah hujan. Model menggunakan teknik machine learning seperti Ridge Regression dan XGBoost untuk melakukan prediksi berdasarkan fitur-fitur yang telah diproses.

## Struktur Proyek

```
data_preprocessing/
├── build_main_dataset.py    # Script untuk membangun dataset utama dari file sumber
└── process.ipynb            # Notebook untuk preprocessing data dan feature engineering

model/
└── model.ipynb              # Notebook untuk training model dan evaluasi

dataset/
├── target/                  # Data inflasi dan indeks harga konsumen
├── harga-makanan-pokok/     # Data harga komoditas (beras, daging, cabai, telur)
├── dataset restoran/        # Data inflasi restoran
├── curah-hujan/             # Data curah hujan
├── food_prediction_data.csv # Dataset mentah hasil build_main_dataset.py
└── final_dataset.csv        # Dataset final hasil preprocessing
```

## Persyaratan Sistem

- Python 3.8 atau lebih baru
- Jupyter Notebook
- Library Python:
  - pandas
  - numpy
  - scikit-learn
  - xgboost
  - openpyxl (untuk membaca file Excel)

## Instalasi

1. Clone atau download repository ini.
2. Pastikan Python dan pip terinstall.
3. Install dependencies dengan perintah:

   ```
   pip install pandas numpy scikit-learn xgboost openpyxl jupyter
   ```

   Atau jika ada file requirements.txt (jika dibuat), gunakan:

   ```
   pip install -r requirements.txt
   ```

## Cara Menjalankan

### 1. Membangun Dataset Utama

Jalankan script untuk membangun dataset dari file sumber:

```
python data_preprocessing/build_main_dataset.py
```

Perintah ini akan:
- Membaca data dari folder `dataset/target/`, `dataset/harga-makanan-pokok/`, dll.
- Menggabungkan data harga komoditas dari tahun 2020, 2024, dan 2025 menjadi kolom tunggal.
- Menghasilkan file `dataset/food_prediction_data.csv` dan `dataset/final_dataset.csv`.

### 2. Preprocessing Data

Buka dan jalankan notebook preprocessing:

```
jupyter notebook data_preprocessing/process.ipynb
```

Di dalam notebook, jalankan semua cell secara berurutan. Notebook ini akan:
- Memuat dataset mentah.
- Menangani nilai yang hilang.
- Melakukan feature engineering (lag features, rolling means, dll.).
- Melakukan standardisasi fitur.
- Menyimpan dataset final ke `dataset/final_dataset.csv`.

### 3. Training Model

Buka dan jalankan notebook model:

```
jupyter notebook model/model.ipynb
```

Di dalam notebook, jalankan semua cell secara berurutan. Notebook ini akan:
- Memuat dataset final.
- Membagi data menjadi train dan test.
- Melatih model Ridge Regression dan XGBoost.
- Mengevaluasi performa model.
- Menampilkan hasil prediksi.

## Fitur Utama

- **Data Harga Komoditas**: Harga beras, daging, cabai, dan telur dari berbagai tahun.
- **Data Inflasi**: Inflasi bulanan dan indeks harga konsumen.
- **Data Curah Hujan**: Simulasi data curah hujan bulanan.
- **Feature Engineering**: Lag features, rolling means, momentum, dan anomaly detection.
- **Model**: Ridge Regression dan XGBoost untuk prediksi.

## Catatan

- Pastikan semua file data berada di folder `dataset/` sesuai struktur.
- Jika ada error saat menjalankan, periksa versi library dan path file.
- Model telah dioptimalkan untuk mengurangi overfitting dengan memilih fitur yang relevan.

## Kontribusi

Jika ingin berkontribusi, silakan buat pull request atau laporkan issue.

## Insight

Insight Hasil Analisis dan Pemodelan

Berdasarkan hasil eksplorasi data dan pemodelan yang telah dilakukan, terlihat bahwa perubahan harga beberapa komoditas pangan memiliki pengaruh yang cukup besar terhadap pergerakan inflasi. Komoditas seperti beras, cabai, daging, dan telur menunjukkan hubungan yang cukup jelas dengan perubahan inflasi dari bulan ke bulan. Ketika terjadi kenaikan harga pada komoditas tersebut, terutama pada komoditas yang volatil seperti cabai, inflasi cenderung ikut mengalami peningkatan.

Selain itu, hasil pemodelan juga menunjukkan bahwa perubahan harga (persentase kenaikan atau penurunan) memberikan pengaruh yang lebih kuat dibandingkan nilai harga itu sendiri. Hal ini terlihat pada fitur perubahan harga komoditas yang memiliki kontribusi cukup besar terhadap prediksi model. Kondisi ini menunjukkan bahwa lonjakan harga secara tiba-tiba dapat memicu perubahan inflasi yang cukup signifikan.

Variabel inflasi pada periode sebelumnya juga memiliki pengaruh terhadap inflasi periode berikutnya. Hal ini terlihat dari fitur lag dan rolling average yang membantu model dalam menangkap pola pergerakan inflasi dari waktu ke waktu. Dengan kata lain, inflasi memiliki kecenderungan mengikuti pola dari periode sebelumnya sehingga informasi historis menjadi penting dalam proses prediksi.

Faktor curah hujan juga ikut dimasukkan dalam model karena dapat mempengaruhi produksi pertanian. Meskipun pengaruhnya tidak sebesar harga komoditas, variabel ini tetap memberikan kontribusi dalam membantu model memahami kondisi yang dapat mempengaruhi ketersediaan pangan dan pada akhirnya berdampak pada harga di pasar.

## Model
Ridge Regression Menghasilkan:
Training MAE: 0.0720
Training MSE: 0.0185
Test MAE: 0.0430
Test MSE: 0.0019
Test R²: 0.9979

XGBoost Regressor Menghasilkan:
Training MAE : 0.1353
Training RMSE: 0.1834
Training R²: 0.9488
Test MAE : 0.2729
Test RMSE: 0.3968
Test R²: 0.8294
