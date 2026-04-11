from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

# Mengatur path root proyek dan direktori data
ROOT = Path(__file__).resolve().parents[1]  # Path ke direktori induk proyek
TARGET_DIR = ROOT / "dataset" / "target"  # Direktori untuk data target inflasi
PRICE_DIR = ROOT / "dataset" / "harga-makanan-pokok"  # Direktori untuk data harga komoditas
RESTAURANT_DIR = ROOT / "dataset" / "dataset restoran"  # Direktori untuk data inflasi restoran
OUTPUT_RAW = ROOT / "dataset" / "food_prediction_data.csv"  # File output dataset mentah
OUTPUT_FINAL = ROOT / "dataset" / "final_dataset.csv"  # File output dataset final

# Mapping nama file Excel ke nama fitur harga
PRICE_FILE_MAP = {
    "Tabel Harga Berdasarkan Komoditas.xlsx": "rice_price_2025",  # Harga beras 2025
    "Tabel Harga Berdasarkan Komoditas (1).xlsx": "rice_price_2025",
    "Tabel Harga Berdasarkan Komoditas (2).xlsx": "meat_price_2025",  # Harga daging 2025
    "Tabel Harga Berdasarkan Komoditas (3).xlsx": "chili_price_2025",  # Harga cabai 2025
    "Tabel Harga Berdasarkan Komoditas (4).xlsx": "egg_price_2025",  # Harga telur 2025
    "Tabel Harga Berdasarkan Komoditas (5).xlsx": "rice_price_2024",  # Harga beras 2024
    "Tabel Harga Berdasarkan Komoditas (6).xlsx": "meat_price_2024",  # Harga daging 2024
    "Tabel Harga Berdasarkan Komoditas (7).xlsx": "chili_price_2024",  # Harga cabai 2024
    "Tabel Harga Berdasarkan Komoditas (8).xlsx": "egg_price_2024",  # Harga telur 2024
    "Tabel Harga Berdasarkan Komoditas (10).xlsx": "rice_price_2020",  # Harga beras 2020
    "Tabel Harga Berdasarkan Komoditas (11).xlsx": "chili_price_2020",  # Harga cabai 2020
    "Tabel Harga Berdasarkan Komoditas (12).xlsx": "meat_price_2020",  # Harga daging 2020
    "Tabel Harga Berdasarkan Komoditas (13).xlsx": "egg_price_2020",  # Harga telur 2020
}

# Daftar fitur harga bulanan
MONTHLY_PRICE_FEATURES = [
    "rice_price_2025",
    "meat_price_2025",
    "chili_price_2025",
    "egg_price_2025",
    "rice_price_2024",
    "meat_price_2024",
    "chili_price_2024",
    "egg_price_2024",
    "rice_price_2020",
    "meat_price_2020",
    "chili_price_2020",
    "egg_price_2020",
]


def _clean_numeric(value):
    # Fungsi untuk membersihkan nilai numerik dari string
    if pd.isna(value):
        return np.nan  # Jika nilai kosong, kembalikan NaN
    text = str(value).strip().replace(",", "")  # Hapus spasi dan koma
    if text in {"", "-", "nan"}:
        return np.nan  # Jika string kosong atau invalid, kembalikan NaN
    return pd.to_numeric(text, errors="coerce")  # Konversi ke numerik, jika gagal kembalikan NaN


def _parse_monthly_dates(columns):
    # Fungsi untuk mengurai tanggal bulanan dari nama kolom
    dates = []
    for col in columns:
        label = str(col).strip()
        label = re.sub(r"\s*/\s*", "/", label)  # Normalisasi format tanggal
        parsed = pd.to_datetime(label, dayfirst=True, errors="coerce")  # Parse tanggal
        if pd.isna(parsed):
            continue
        dates.append(parsed.replace(day=1))  # Set ke tanggal 1 bulan tersebut
    return dates


def _parse_target_index_file(path: Path) -> pd.DataFrame:
    # Fungsi untuk mengurai file indeks harga konsumen
    match = re.search(r",\s*(\d{4})\.csv$", path.name)
    if not match:
        raise ValueError(f"Cannot determine year from filename {path.name}")
    year = int(match.group(1))  # Ekstrak tahun dari nama file

    raw = pd.read_csv(path, header=None, encoding="utf-8")  # Baca file CSV tanpa header
    data = raw.iloc[5:, 1:13].apply(lambda col: col.map(_clean_numeric))  # Bersihkan data numerik
    means = data.mean(axis=0, skipna=True)  # Hitung rata-rata per bulan
    dates = pd.date_range(start=f"{year}-01-01", periods=len(means), freq="MS")  # Buat range tanggal bulanan
    return pd.DataFrame({"date": dates, "index": means.values})


def _parse_monthly_inflation_file(path: Path) -> pd.DataFrame:
    # Fungsi untuk mengurai file inflasi bulanan
    match = re.search(r",\s*(\d{4})\.csv$", path.name)
    if not match:
        raise ValueError(f"Cannot determine year from filename {path.name}")
    year = int(match.group(1))  # Ekstrak tahun dari nama file

    raw = pd.read_csv(path, header=None, encoding="utf-8")  # Baca file CSV tanpa header
    data = raw.iloc[5:, 1:13].apply(lambda col: col.map(_clean_numeric))  # Bersihkan data numerik
    means = data.mean(axis=0, skipna=True)  # Hitung rata-rata inflasi per bulan
    dates = pd.date_range(start=f"{year}-01-01", periods=len(means), freq="MS")  # Buat range tanggal bulanan
    return pd.DataFrame({"date": dates, "inflation": means.values})


def parse_target_series() -> pd.DataFrame:
    # Fungsi untuk mengurai dan menggabungkan data target inflasi
    index_files = sorted(TARGET_DIR.glob("Indeks Harga Konsumen*.csv"))  # Cari file indeks harga
    inflation_files = sorted(TARGET_DIR.glob("Inflasi Bulanan*.csv"))  # Cari file inflasi bulanan

    index_records = []
    for path in index_files:
        df = _parse_target_index_file(path)  # Parse setiap file indeks
        index_records.append(df)

    if not index_records:
        raise FileNotFoundError("No target index files found in dataset/target")

    index_df = pd.concat(index_records, ignore_index=True)  # Gabungkan data indeks
    index_df = index_df.drop_duplicates("date", keep="last").sort_values("date").reset_index(drop=True)
    index_df["inflation"] = index_df["index"].pct_change() * 100  # Hitung inflasi dari indeks
    index_df = index_df.drop(columns=["index"])

    inflation_records = []
    for path in inflation_files:
        df = _parse_monthly_inflation_file(path)  # Parse file inflasi langsung
        inflation_records.append(df)

    if inflation_records:
        inflation_df = pd.concat(inflation_records, ignore_index=True)  # Gabungkan data inflasi
        inflation_df = inflation_df.drop_duplicates("date", keep="last").sort_values("date").reset_index(drop=True)
        combined = pd.concat([index_df, inflation_df], ignore_index=True)  # Gabungkan indeks dan inflasi
        combined = combined.drop_duplicates("date", keep="last").sort_values("date").reset_index(drop=True)
    else:
        combined = index_df

    combined = combined.dropna(subset=["inflation"]).reset_index(drop=True)  # Hapus baris tanpa inflasi
    return combined


def _parse_price_file(path: Path) -> pd.DataFrame:
    # Fungsi untuk mengurai file harga komoditas Excel
    df = pd.read_excel(path, engine="openpyxl", header=0)  # Baca file Excel
    key_col = df.columns[1]
    row = df[df[key_col].astype(str).str.contains("Semua Provinsi", na=False)]  # Cari baris untuk semua provinsi
    if row.empty:
        return pd.DataFrame(columns=["date", "value"])

    row = row.iloc[0]  # Ambil baris pertama yang cocok
    date_columns = df.columns[2:]  # Kolom tanggal mulai dari kolom ke-3
    dates = _parse_monthly_dates(date_columns)  # Parse tanggal dari nama kolom
    values = [ _clean_numeric(x) for x in row.iloc[2:].tolist() ]  # Bersihkan nilai harga
    series_df = pd.DataFrame({"date": dates, "value": values[: len(dates)]})  # Buat DataFrame
    return series_df.dropna(subset=["date"]).reset_index(drop=True)


def load_price_series() -> dict[str, pd.DataFrame]:
    # Fungsi untuk memuat semua seri harga komoditas dari file Excel
    series = {}
    for filename, feature_name in PRICE_FILE_MAP.items():
        path = PRICE_DIR / filename
        if not path.exists():
            continue  # Lewati jika file tidak ada
        parsed = _parse_price_file(path)  # Parse file harga
        if not parsed.empty:
            series[feature_name] = parsed  # Simpan seri harga
    return series


def parse_restaurant_inflation() -> pd.DataFrame:
    # Fungsi untuk mengurai data inflasi restoran
    out = pd.DataFrame()
    for path in sorted(RESTAURANT_DIR.glob("*.csv")):  # Cari file inflasi restoran
        if "Inflasi Bulanan" not in path.name:
            continue  # Hanya file inflasi bulanan
        try:
            df = _parse_monthly_inflation_file(path)  # Parse file
            if not df.empty:
                out = df
                break  # Ambil file pertama yang valid
        except Exception:
            continue  # Lewati jika error
    return out


def build_rainfall(start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    # Fungsi untuk membangun data curah hujan simulasi
    dates = pd.date_range(start=start_date, end=end_date, freq="MS")  # Range tanggal bulanan
    monthly_pattern = {  # Pola curah hujan bulanan (mm)
        1: 250, 2: 220, 3: 180, 4: 120, 5: 80, 6: 60,
        7: 50, 8: 40, 9: 60, 10: 100, 11: 180, 12: 240,
    }
    rainfall_values = []
    for date in dates:
        year_factor = 0.95 + (date.year - dates[0].year) * 0.01  # Faktor tahunan
        base = monthly_pattern[date.month] * year_factor  # Basis curah hujan
        rainfall = base + (base * 0.1 * np.sin(date.month * 0.5))  # Tambahkan variasi
        rainfall_values.append(max(0.0, rainfall))  # Pastikan tidak negatif
    return pd.DataFrame({"date": dates, "rainfall": rainfall_values})

    return pd.DataFrame({"date": dates, "rainfall": rainfall_values})


def build_dataset() -> pd.DataFrame:
    # Fungsi utama untuk membangun dataset mentah
    df = parse_target_series()  # Parse data target inflasi

    price_series = load_price_series()  # Muat seri harga komoditas
    for feature_name, price_df in price_series.items():
        df = df.merge(price_df.rename(columns={"value": feature_name}), on="date", how="left")  # Gabungkan harga

    # Mapping untuk menggabungkan harga tahun ke kolom tunggal
    year_price_map = {
        "rice": ["rice_price_2025", "rice_price_2024", "rice_price_2020"],
        "chili": ["chili_price_2025", "chili_price_2024", "chili_price_2020"],
        "meat": ["meat_price_2025", "meat_price_2024", "meat_price_2020"],
        "egg": ["egg_price_2025", "egg_price_2024", "egg_price_2020"],
    }

    for commodity, year_columns in year_price_map.items():
        base_series = None
        for col in year_columns:
            if col in df.columns:
                if base_series is None:
                    base_series = df[col].copy()  # Mulai dengan kolom pertama
                else:
                    base_series = base_series.fillna(df[col])  # Isi NaN dengan kolom berikutnya
        if base_series is not None:
            df[f"{commodity}_price"] = base_series  # Buat kolom harga tunggal

    # Hapus kolom harga tahun-spesifik untuk menyederhanakan dataset
    year_price_cols = [col for cols in year_price_map.values() for col in cols if col in df.columns]
    if year_price_cols:
        df = df.drop(columns=year_price_cols)

    restaurant_df = parse_restaurant_inflation()  # Parse inflasi restoran
    if not restaurant_df.empty:
        df = df.merge(restaurant_df.rename(columns={"inflation": "restaurant_inflation"}), on="date", how="left")

    rainfall_df = build_rainfall(df["date"].min(), df["date"].max())  # Bangun data curah hujan
    df = df.merge(rainfall_df, on="date", how="left")

    df = df.sort_values("date").reset_index(drop=True)  # Urutkan berdasarkan tanggal
    df["lag_inflation"] = df["inflation"].shift(1)  # Lag inflasi 1 bulan
    df["lag_1"] = df["lag_inflation"]
    df["lag_2"] = df["inflation"].shift(2)  # Lag inflasi 2 bulan
    df["rolling_3"] = df["inflation"].rolling(3).mean()  # Rolling mean 3 bulan

    return df


def build_final_dataset(raw_df: pd.DataFrame) -> pd.DataFrame:
    # Fungsi untuk membangun dataset final dengan feature engineering
    df = raw_df.copy()
    price_cols = [col for col in df.columns if col.startswith("rice_price") or col.startswith("chili_price") or col.startswith("meat_price") or col.startswith("egg_price")]
    df[price_cols] = df[price_cols].interpolate(method="linear", limit_direction="both")  # Interpolasi harga
    df = df.ffill().bfill()  # Fill missing values

    df["inflation_momentum"] = df["inflation"].diff(1)  # Momentum inflasi
    for col in ["rice_price", "chili_price", "meat_price", "egg_price"]:
        if col in df.columns:
            df[f"{col}_pct_change"] = df[col].pct_change() * 100  # Persentase perubahan harga

    if "rainfall" in df.columns:
        df["rainfall_anomaly"] = (df["rainfall"] - df["rainfall"].mean()) / df["rainfall"].std(ddof=0)  # Anomali curah hujan

    df["inflation_rolling_3"] = df["inflation"].rolling(window=3).mean()  # Rolling mean inflasi 3 bulan
    df["inflation_rolling_6"] = df["inflation"].rolling(window=6).mean()  # Rolling mean inflasi 6 bulan
    df = df.ffill().bfill()  # Fill lagi
    return df


def main() -> None:
    # Fungsi utama untuk menjalankan pipeline
    dataset = build_dataset()  # Bangun dataset mentah
    OUTPUT_RAW.parent.mkdir(parents=True, exist_ok=True)  # Buat direktori jika perlu
    dataset.to_csv(OUTPUT_RAW, index=False)  # Simpan dataset mentah
    print(f"Raw dataset written to {OUTPUT_RAW}")

    final_dataset = build_final_dataset(dataset)  # Bangun dataset final
    final_dataset.to_csv(OUTPUT_FINAL, index=False)  # Simpan dataset final
    print(f"Final dataset written to {OUTPUT_FINAL}")


if __name__ == "__main__":
    main()  # Jalankan jika script dieksekusi langsung
