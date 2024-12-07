# -*- coding: utf-8 -*-
"""Proyek Analisis Data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1q239Yt-bzC-ryDfBe4Q56138QSTOvIZY

# **Proyek Analisis Data: Penyewaan Sepeda**

**Nama : Ikrom Nur Muhammad Al-habib**

**Kelas Bangkit : ML-74**

**Dicoding ID : ikromnur**

# **Menentukan Pertanyaan Bisnis:**

- Bagaimana pengaruh cuaca (weather situation) terhadap jumlah peminjaman sepeda?

- Apakah jumlah peminjaman sepeda bervariasi di setiap musim, dan bagaimana strategi optimalnya?

# **Menyiapkan semua library yang dibutuhkan**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pip freeze requirements.txt

"""# **1. Data Wrangling**

## **1.1 Gathering Data**
"""

day_data = pd.read_csv(r'/content/sample_data/data_1.csv')
hour_data = pd.read_csv(r'/content/sample_data/data_2.csv')

day_data.head()

hour_data.head()

print("Dimensi dataset hour.csv:", hour_data.shape)
print("Dimensi dataset day.csv:", day_data.shape)

"""**Insight:**
1. **Jumlah Data:**
Dataset hour.csv memiliki 17,379 baris dan 17 kolom, sedangkan day.csv memiliki 731 baris dan 16 kolom. Hal ini menunjukkan bahwa hour.csv mencatat data per jam, sementara day.csv menyajikan ringkasan data harian.

## **1.2 Assesing Data**

**1.2.1 Cek Tipe Data**
"""

day_data.info()

hour_data.info()

"""**1.2.2 Cek Missing Value**"""

print("\nMissing values in the day dataset:")
print(day_data.isnull().sum())
print("\nMissing values in the hour dataset:")
print(hour_data.isnull().sum())

"""**1.2.3 Cek Data Duplikat**"""

print("\nData duplikat di day dataset:", day_data.duplicated().sum())
print("Data duplikat di hour dataset:", hour_data.duplicated().sum())

"""**1.2.4 Cek Outlier**"""

def outlier(data):
    columns = data.select_dtypes(include=('int64', 'float64')).columns
    outlier_counts = {}
    for column in columns:
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
        outlier_counts[column] = len(outliers)
    return outlier_counts

outlier_counts_day = outlier(day_data)

# Mengubah dictionary outlier_counts menjadi DataFrame
outlier_day = pd.DataFrame(list(outlier_counts_day.items()), columns=['Column', 'Outlier Count'])
print(outlier_day)

def outlier(data):
    columns = data.select_dtypes(include=('int64', 'float64')).columns
    outlier_counts = {}
    for column in columns:
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
        outlier_counts[column] = len(outliers)
    return outlier_counts

outlier_counts_hour = outlier(hour_data)

# Mengubah dictionary outlier_counts menjadi DataFrame
outlier_hour = pd.DataFrame(list(outlier_counts_hour.items()), columns=['Column', 'Outlier Count'])
print(outlier_hour)

"""**Insight**

1. **Jenis Kolom:**
Kedua dataset memiliki kolom dteday yang bertipe objek (string). Agar analisis waktu lebih akurat, kolom ini perlu diubah ke tipe datetime. Selain itu, kolom temp, atemp, hum, dan windspeed merupakan data numerik dengan tipe float64, sementara sebagian besar kolom lainnya bertipe int64, yang biasanya digunakan untuk merepresentasikan kategori atau jumlah.

2. **Tidak Ada Data Hilang**:
Berdasarkan ringkasan data, kedua dataset tidak memiliki nilai kosong (null), sehingga tidak diperlukan langkah tambahan untuk mengisi atau membersihkan data yang hilang.

3. **Perbedaan Kolom antara day.csv dan hour.csv**:
Perbedaan utama antara kedua dataset adalah keberadaan kolom hr (jam) di hour.csv, yang tidak terdapat di day.csv. Ini karena hour.csv mencatat data peminjaman sepeda per jam, sedangkan day.csv menyajikan data yang sudah diringkas per hari.

4. **Ada Outlier**:
Pada data day maupun hour tedapat outlier yang dimana akan dibersihkan menggunakan interquartil
"""

day_data['dteday'] = pd.to_datetime(day_data['dteday'])
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])

"""**Mengonversi Tipe Data dteday menjadi datetime**:

Pada kedua dataset, day_data dan hour_data, kolom dteday awalnya memiliki tipe data object (string). Karena kolom ini merepresentasikan tanggal, mengonversinya ke tipe datetime akan memudahkan kita dalam melakukan operasi atau analisis berbasis waktu dengan lebih efektif.

## **1.3 Data Cleaning**

**1.3.1 Hapus Outlier**
"""

def remove_outlier(data):
    numeric_columns = data.select_dtypes(include=('int64', 'float64')).columns
    clean_data = data.copy()  # Membuat salinan DataFrame agar tidak mengubah data asli
    for column in numeric_columns:
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        clean_data = clean_data[(clean_data[column] >= lower_bound) & (clean_data[column] <= upper_bound)]
    return clean_data

data_cleaned_day = remove_outlier(day_data)

def remove_outlier(data):
    numeric_columns = data.select_dtypes(include=('int64', 'float64')).columns
    clean_data = data.copy()  # Membuat salinan DataFrame agar tidak mengubah data asli
    for column in numeric_columns:
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        clean_data = clean_data[(clean_data[column] >= lower_bound) & (clean_data[column] <= upper_bound)]
    return clean_data

data_cleaned_hour = remove_outlier(hour_data)

"""# **2. Exploratory Data Analysis (EDA)**

## **2.1 Statistika Deskriptif**
"""

day_data.describe()

hour_data.describe()

"""## **2.2 Distribusi Variabel**"""

sns.set_theme(style="whitegrid")
numeric_columns_day = day_data.select_dtypes(include=['int64', 'float64']).columns
plt.figure(figsize=(20, 16))

for i, column in enumerate(numeric_columns_day, 1):
    plt.subplot(4, 4, i)
    sns.histplot(day_data[column], bins=30, kde=True, color=sns.color_palette("Set2")[i % 6],
                 edgecolor='black', alpha=0.8, linewidth=1.5)
    plt.title(f'Distribusi {column}', fontsize=14, fontweight='bold')
    plt.xlabel(column, fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)

plt.tight_layout()
plt.show()

"""**Distribusi Instant**:

Menunjukkan variasi yang cukup besar dengan puncak sekitar nilai 600, mengindikasikan adanya fluktuasi signifikan pada nilai instant.

**Distribusi Season**:

Puncak berada di nilai 3, yang berarti musim gugur (fall) adalah yang paling sering muncul dalam data.

**Distribusi Yr**:

Menunjukkan rentang yang lebar dengan puncak di nilai 0, menandakan bahwa tahun 2011 memiliki frekuensi data lebih tinggi.

**Distribusi Mnth**:

Pola naik turun terlihat jelas, dengan puncak pada bulan ke-6 dan ke-9, mengindikasikan adanya variasi peminjaman sepeda di bulan-bulan tersebut.

**Distribusi Weathersit**:
Paling sering berada di kategori 1, yang berarti cuaca cerah atau berawan sebagian lebih dominan di dataset ini.

**Distribusi Temp (Suhu)**:

Cenderung mengikuti pola distribusi normal, dengan suhu yang paling sering muncul di rentang 20-30 derajat Celsius.

**Distribusi Atemp (Suhu yang Dirasakan)**:

Sama seperti distribusi suhu, distribusi suhu yang dirasakan juga berbentuk normal dengan puncak di sekitar 20-30 derajat Celsius.

**Distribusi Hum (Kelembaban)**:

Menunjukkan pola distribusi normal dengan kelembaban yang paling sering muncul berada di rentang 40-80%.

**Distribusi Windspeed (Kecepatan Angin)**:

Distribusi kecepatan angin mengikuti kurva normal dengan puncak di rentang 10-30 km/jam.

**Distribusi Casual (Pengguna Casual)**:

Memiliki pola normal, dengan pengguna casual paling banyak di angka sekitar 50-60.

**Distribusi Registered (Pengguna Terdaftar)**:

Mengikuti pola normal, dengan jumlah pengguna terdaftar terbanyak sekitar 40-50.

**Distribusi Cnt (Jumlah Total Pengguna)**:

Menunjukkan pola normal dengan jumlah total peminjaman paling sering muncul di kisaran 30-40 pengguna.
"""

sns.set_theme(style="whitegrid")
numeric_columns_day = hour_data.select_dtypes(include=['int64', 'float64']).columns
plt.figure(figsize=(20, 16))

for i, column in enumerate(numeric_columns_day, 1):
    plt.subplot(4, 4, i)
    sns.histplot(hour_data[column], bins=30, kde=True, color=sns.color_palette("Set2")[i % 6],
                 edgecolor='black', alpha=0.8, linewidth=1.5)
    plt.title(f'Distribusi {column}', fontsize=14, fontweight='bold')
    plt.xlabel(column, fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)

plt.tight_layout()
plt.show()

"""**Distribusi Instant**: Menunjukkan variasi yang signifikan dengan puncaknya sekitar nilai 15.000, yang menandakan adanya fluktuasi besar dalam data ini.

**Distribusi Season**: Puncaknya berada di nilai 3, yang menunjukkan bahwa musim gugur (fall) adalah yang paling sering terjadi dalam dataset.

**Distribusi Yr**: Menunjukkan rentang nilai yang lebar, dengan puncak sekitar 0.4, menunjukkan bahwa tahun 2013 memiliki frekuensi yang lebih tinggi.

**Distribusi Mnth**: Menunjukkan pola yang naik turun, dengan puncak pada bulan ke-6 dan ke-9, yang menandakan variasi peminjaman sepeda yang cukup besar di bulan-bulan tersebut.

**Distribusi Weathersit**: Nilai yang paling sering muncul adalah 1, menunjukkan bahwa kondisi cuaca "Cerah, Sedikit berawan, atau Berawan sebagian" lebih dominan.

**Distribusi Temp (Suhu)**: Polanya menyerupai distribusi normal, dengan suhu yang paling sering berada di kisaran 20-30 derajat Celsius.

**Distribusi Atemp (Suhu yang Dirasakan)**: Distribusi suhu yang dirasakan juga mengikuti pola normal, dengan kisaran yang sama, yaitu 20-30 derajat Celsius.

**Distribusi Hum (Kelembaban)**: Kelembaban menunjukkan pola distribusi normal, dengan nilai yang sering berada di rentang 40-80%.

**Distribusi Windspeed (Kecepatan Angin)**: Tidak menunjukkan pola distribusi normal, namun kecepatan angin yang paling umum berada di kisaran 10-30 km/jam.

**Distribusi Casual (Pengguna Casual)**: Tidak mengikuti pola distribusi normal, dengan puncak pengguna casual berada di kisaran 3.000-4.000.

**Distribusi Registered (Pengguna Terdaftar)**: Distribusi pengguna terdaftar juga tidak mengikuti pola normal, dengan jumlah yang sering berada di sekitar 2.000-3.000 pengguna.

**Distribusi Cnt (Jumlah Total Pengguna)**: Tidak mengikuti pola normal, dengan jumlah total pengguna paling sering berada di kisaran 3.000-4.000 pengguna.

## **2.3 Korelasi Variabel**
"""

# Korelasi antar fitur day dan hour
correlation_day = day_data.corr()
correlation_hour = hour_data.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_day, annot=True, fmt='.2f', cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
plt.title('Correlation Matrix for Day Data (without date variables)')
plt.show()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_hour, annot=True, fmt='.2f', cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
plt.title('Correlation Matrix for Hour Data (without date variables)')
plt.show()

"""**Variabel dengan korelasi tertinggi terhadap jumlah penyewaan sepeda**"""

highest_corr = correlation_hour['cnt'].sort_values(ascending=False)
print("\nHighest correlated variables with 'cnt' in hour data:")
print(highest_corr)

highest_corr = correlation_day['cnt'].sort_values(ascending=False)
print("\nHighest correlated variables with 'cnt' in hour data:")
print(highest_corr)

"""# **Kesimpulan:**
Faktor terbesar yang memengaruhi jumlah peminjaman sepeda adalah pengguna terdaftar (registered), yang menunjukkan bahwa platform sepeda lebih banyak digunakan oleh pengguna setia dibandingkan pengguna kasual.
Suhu dan jam dalam sehari juga berperan penting dalam mempengaruhi peminjaman sepeda.
Faktor-faktor seperti kelembaban dan kondisi cuaca buruk memiliki dampak negatif, sedangkan status hari kerja atau libur tidak begitu berpengaruh.

# **Menjawab pertanyaan bisnis**

## **1. Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda**
"""

# Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda pada data day.csv
plt.figure(figsize=(8, 6))
sns.barplot(x='weathersit', y='cnt', data=day_data, palette='coolwarm')
plt.title('Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda (Data Harian)')
plt.xlabel('Weathersit (1=Clear, 2=Mist, 3=Snow/Rain)')
plt.ylabel('Jumlah Peminjaman Sepeda (cnt)')
plt.show()

"""**Interpretasi Visualisasi**:

Visualisasi bar plot di atas menunjukkan hubungan yang jelas antara kondisi cuaca (weathersit) dan jumlah peminjaman sepeda. Terdapat tiga kategori cuaca:

1. **Clear (Cerah)**: Jumlah peminjaman sepeda paling tinggi pada kondisi cuaca cerah. Ini menunjukkan bahwa sebagian besar orang lebih memilih untuk menyewa sepeda ketika cuaca cerah dan mendukung aktivitas luar ruangan.

2. **Mist (Kabut)**: Jumlah peminjaman sepeda masih cukup tinggi pada kondisi berkabut, meskipun lebih rendah dibandingkan cuaca cerah. Hal ini mengindikasikan bahwa kabut tidak terlalu menghambat aktivitas bersepeda.

3. **Snow/Rain (Salju/Hujan)**: Jumlah peminjaman sepeda paling rendah pada kondisi bersalju atau hujan. Ini menunjukkan bahwa cuaca buruk seperti salju atau hujan secara signifikan mengurangi minat masyarakat untuk menyewa sepeda.
Garis error bar pada setiap batang menunjukkan rentang nilai atau variabilitas data. Garis error bar yang lebih panjang mengindikasikan bahwa ada lebih banyak variasi dalam jumlah peminjaman sepeda pada kondisi cuaca tersebut.

## **2. Pengaruh Musim terhadap Jumlah Peminjaman Sepeda (Season vs Cnt)**
"""

# Pengaruh Musim terhadap Jumlah Peminjaman Sepeda pada data day.csv
plt.figure(figsize=(8, 6))
sns.barplot(x='season', y='cnt', data=day_data, palette='Set2')
plt.title('Pengaruh Musim terhadap Jumlah Peminjaman Sepeda (Data Harian)')
plt.xlabel('Season (1=Spring, 2=Summer, 3=Fall, 4=Winter)')
plt.ylabel('Jumlah Peminjaman Sepeda (cnt)')
plt.show()

"""**Interpretasi Visualisasi**:

Visualisasi bar plot di atas menunjukkan hubungan yang jelas antara musim dan jumlah peminjaman sepeda. Terdapat empat kategori musim:

1. **Spring (Musim Semi)**: Jumlah peminjaman sepeda cenderung lebih rendah pada musim semi.

2. **Summer (Musim Panas)**: Jumlah peminjaman sepeda meningkat secara signifikan pada musim panas. Ini menunjukkan bahwa banyak orang lebih memilih bersepeda saat cuaca hangat dan cerah.

3. **Fall (Musim Gugur)**: Jumlah peminjaman sepeda masih cukup tinggi pada musim gugur, meskipun sedikit menurun dibandingkan musim panas.

4. **Winter (Musim Dingin)**: Jumlah peminjaman sepeda kembali menurun pada musim dingin, kemungkinan besar karena cuaca dingin dan kondisi jalan yang kurang mendukung untuk bersepeda.
Garis error bar pada setiap batang menunjukkan rentang nilai atau variabilitas data. Garis error bar yang lebih panjang mengindikasikan bahwa ada lebih banyak variasi dalam jumlah peminjaman sepeda pada musim tersebut.

# **Kesimpulan dan Implikasi Bisnis**

Analisis terhadap data peminjaman sepeda telah mengungkapkan beberapa temuan penting yang dapat menjadi dasar pengambilan keputusan bisnis.

- **Pengaruh Cuaca dan Musim**: Cuaca cerah dan musim panas menjadi faktor pendorong utama peningkatan jumlah peminjaman sepeda. Sebaliknya, cuaca buruk dan musim dingin cenderung menurunkan minat masyarakat untuk menyewa sepeda. Implikasinya, perusahaan perlu menyesuaikan persediaan sepeda, strategi promosi, dan bahkan mempertimbangkan produk tambahan seperti jas hujan atau sepeda listrik untuk musim dingin.

- **Perbedaan Tipe Pelanggan**: Pelanggan casual dan registered memiliki pola penggunaan yang berbeda. Pelanggan casual cenderung lebih impulsif, sementara registered lebih stabil. Hal ini mengindikasikan perlunya strategi pemasaran yang berbeda untuk masing-masing segmen. Misalnya, menawarkan program loyalitas untuk pelanggan registered dan promosi jangka pendek untuk menarik pelanggan casual.

- **Peran Suhu**: Suhu memiliki korelasi positif dengan jumlah peminjaman sepeda, terutama pada musim semi dan gugur. Ini menunjukkan pentingnya mempertimbangkan faktor cuaca dalam perencanaan bisnis.

**Implikasi Bisnis Secara Umum**:

- Perencanaan yang Lebih Baik: Dengan memahami faktor-faktor yang mempengaruhi jumlah peminjaman sepeda, perusahaan dapat melakukan perencanaan yang lebih baik, baik dalam hal persediaan sepeda maupun sumber daya manusia.

- Strategi Pemasaran yang Efektif: Perusahaan dapat mengembangkan strategi pemasaran yang lebih targeted, dengan mempertimbangkan segmen pelanggan, musim, dan kondisi cuaca.

- Pengembangan Produk yang Inovatif: Perusahaan dapat mempertimbangkan untuk mengembangkan produk atau layanan baru yang dapat memenuhi kebutuhan pelanggan yang berbeda-beda.

- Pengambilan Keputusan yang Data-Driven: Semua keputusan bisnis dapat didasarkan pada data yang akurat dan analisis yang mendalam.
"""