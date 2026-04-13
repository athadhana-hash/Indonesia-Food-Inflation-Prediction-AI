Indonesia Food Inflation Prediction
Deskripsi Proyek

Proyek ini bertujuan untuk memprediksi inflasi makanan di Indonesia menggunakan pendekatan machine learning. Prediksi dilakukan dengan memanfaatkan data harga komoditas pangan, data inflasi, serta data curah hujan yang dapat mempengaruhi produksi dan harga pangan.

Model yang digunakan dalam proyek ini adalah Ridge Regression dan XGBoost Regressor untuk mempelajari hubungan antara perubahan harga komoditas dan pergerakan inflasi dari waktu ke waktu.

Permasalahan

Salah satu tantangan utama dalam proyek ini adalah tidak tersedianya dataset tunggal yang secara langsung dapat digunakan untuk memprediksi inflasi pangan di Indonesia.

Data yang dibutuhkan tersebar di berbagai sumber resmi seperti:

Badan Pusat Statistik (data inflasi dan indeks harga konsumen)
Bank Indonesia (data inflasi sektor restoran)
Badan Meteorologi Klimatologi dan Geofisika (data curah hujan)

Selain itu, data harga komoditas pangan juga tersedia dalam berbagai file yang terpisah.

Secara keseluruhan terdapat 27 dataset mentah dengan format dan struktur yang berbeda. Dataset tersebut mencakup periode tahun 2020 hingga 2025.

Karena data berasal dari berbagai sumber yang tidak terintegrasi, dataset tersebut tidak dapat langsung digunakan untuk proses machine learning.

Solusi

Untuk mengatasi permasalahan tersebut, dibuat sebuah ETL pipeline (Extract, Transform, Load) untuk menggabungkan seluruh dataset menjadi satu master dataset yang siap digunakan untuk analisis dan pemodelan.

Proses ETL dilakukan dengan beberapa tahap utama:

1. Extract
Mengambil data dari berbagai sumber seperti data inflasi, harga komoditas, dan curah hujan.

2. Transform
Melakukan pembersihan dan pengolahan data, seperti:

menyatukan dataset dari berbagai tahun
menyesuaikan format tanggal
menangani nilai yang hilang
menggabungkan dataset berdasarkan periode waktu
membuat fitur tambahan (feature engineering)

Beberapa fitur tambahan yang dibuat antara lain:

lag inflasi (inflasi periode sebelumnya)
rolling mean inflasi
perubahan harga komoditas
indikator curah hujan

3. Load
Setelah seluruh proses selesai, data digabungkan menjadi satu master dataset yang siap digunakan untuk training model machine learning.

Struktur Proyek
data_preprocessing/
├── build_main_dataset.py
└── process.ipynb

train_model/
└── model.ipynb

model/
└── xgb_model.pkl

dataset/
├── target/
├── harga-makanan-pokok/
├── dataset-restoran/
├── curah-hujan/
├── food_prediction_data.csv
└── final_dataset.csv
Cara Menjalankan
1. Membangun Dataset
python data_preprocessing/build_main_dataset.py

Script ini akan menggabungkan seluruh dataset mentah menjadi dataset utama.

2. Preprocessing Data
jupyter notebook data_preprocessing/process.ipynb

Tahap ini melakukan:

pembersihan data
feature engineering
pembuatan dataset final
3. Training Model
jupyter notebook model/model.ipynb

Pada tahap ini dilakukan:

pembagian data train dan test
training model machine learning
evaluasi model
Hasil Model
Ridge Regression

Training MAE : 0.0720
Training MSE : 0.0185

Test MAE : 0.0430
Test MSE : 0.0019

Test R² : 0.9979

XGBoost Regressor

Training MAE : 0.1353
Training RMSE : 0.1834
Training R² : 0.9488

Test MAE : 0.2729
Test RMSE : 0.3968
Test R² : 0.8294

Insight

Hasil analisis menunjukkan bahwa perubahan harga komoditas pangan memiliki hubungan yang kuat dengan pergerakan inflasi.

Komoditas seperti:

beras
cabai
daging
telur

memiliki pengaruh yang cukup signifikan terhadap perubahan inflasi dari bulan ke bulan.

Selain itu, fitur perubahan harga komoditas terbukti lebih berpengaruh dibandingkan nilai harga absolut. Hal ini menunjukkan bahwa lonjakan harga secara tiba-tiba dapat memicu kenaikan inflasi yang cukup signifikan.

Variabel inflasi pada periode sebelumnya juga membantu model dalam menangkap pola pergerakan inflasi dari waktu ke waktu.

Teknologi yang Digunakan
Python
Pandas
NumPy
Scikit-learn
XGBoost
Jupyter Notebook
Kesimpulan

Proyek ini menunjukkan bahwa data ekonomi dari berbagai sumber dapat diintegrasikan melalui proses ETL untuk membangun dataset yang siap digunakan dalam analisis machine learning.

Dengan memanfaatkan data harga komoditas, inflasi, dan faktor lingkungan seperti curah hujan, model machine learning mampu mempelajari pola perubahan inflasi pangan dan memberikan prediksi yang cukup akurat.
