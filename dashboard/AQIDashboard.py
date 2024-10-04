import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

sns.set(style='dark')

# Membaca data
AQI_A = pd.read_csv("AQI_Aotizhongxin.csv")
AQI_B = pd.read_csv("AQin_Dongsi.csv")  # Ganti dengan nama file stasiun B yang sesuai
# Pastikan kolom 'Date Time' ada dan dalam format datetime
AQI_A['Date Time'] = pd.to_datetime(AQI_A['Date Time'])
AQI_B['Date Time'] = pd.to_datetime(AQI_B['Date Time'])

# Mendapatkan rentang tanggal minimum dan maksimum untuk stasiun A
min_date_A = AQI_A['Date Time'].min().date() 
max_date_A = AQI_A['Date Time'].max().date()  

# Sidebar untuk pemilihan stasiun
with st.sidebar:
    st.image("AQIDashboard.jpg")
    
    # Pilihan stasiun
    station_choice = st.selectbox("Pilih Stasiun", ["Station Aotizhongxin", "Station Dongsi"])
    
    # Batasi pengguna untuk hanya memilih rentang 7 hari (1 minggu)
    if station_choice == "Station Aotizhongxin":
        start_date, end_date = st.date_input(
            label='Rentang Waktu (Maksimal 7 hari)',
            min_value=min_date_A,
            max_value=max_date_A,
            value=[min_date_A, min_date_A + datetime.timedelta(days=6)]
        )
    else:
        min_date_B = AQI_B['Date Time'].min().date() 
        max_date_B = AQI_B['Date Time'].max().date()
        
        start_date, end_date = st.date_input(
            label='Rentang Waktu (Maksimal 7 hari)',
            min_value=min_date_B,
            max_value=max_date_B,
            value=[min_date_B, min_date_B + datetime.timedelta(days=6)]
        )

    # Jika rentang tanggal lebih dari 7 hari, tampilkan pesan kesalahan
    if (end_date - start_date).days > 6:
        st.error("Rentang waktu maksimal adalah 7 hari. Silakan sesuaikan kembali tanggal yang dipilih.")
        st.stop()

# Filter data berdasarkan rentang tanggal yang dipilih
if station_choice == "Station Aotizhongxin":
    filtered_data = AQI_A[(AQI_A['Date Time'].dt.date >= start_date) & (AQI_A['Date Time'].dt.date <= end_date)]
else:
    filtered_data = AQI_B[(AQI_B['Date Time'].dt.date >= start_date) & (AQI_B['Date Time'].dt.date <= end_date)]

# Resample hanya untuk kolom numerik
numeric_cols = filtered_data.select_dtypes(include=[np.number]).columns
daily_avg_numeric = filtered_data.resample('D', on='Date Time')[numeric_cols].mean()

# Untuk kolom 'Kategori', kita ambil mode (kategori yang paling sering muncul)
daily_avg_string = filtered_data.resample('D', on='Date Time')['Kategori'].agg(lambda x: x.mode()[0] if not x.mode().empty else None)

# Gabungkan data numerik dan string kembali
daily_avg = pd.concat([daily_avg_numeric, daily_avg_string], axis=1)

# Reset index to bring 'Date Time' back as a column
daily_avg.reset_index(inplace=True)
st.title("Air Quality In Station Aotzhongxin and Station Dongsi")
# Display the pollutant data per day in a bar chart
average_pollutants = daily_avg[['PM2.5', 'PM10', 'O3', 'NO2', 'SO2']].mean()
st.subheader("Pollutant and Concentration per Day")
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(average_pollutants.index, average_pollutants.values, color=['blue', 'orange', 'green', 'red', 'purple'])
ax.set_title("Pollutant and Concentration (Average for Selected Week)", fontsize=16)
ax.set_xlabel("Pollutants", fontsize=12)
ax.set_ylabel("Concentration (µg/m³)", fontsize=12)
st.pyplot(fig)

st.subheader("Forecast Air Quality in one week")
# Loop through each day to create a visually engaging forecast display
for i, row in daily_avg.iterrows():
    # Tentukan warna berdasarkan kategori AQI
    if row['Kategori'] == 'Good':
        bg_color = '#00e400'  # Hijau
    elif row['Kategori'] == 'Moderate':
        bg_color = '#ffff00'  # Kuning
    elif row['Kategori'] == 'Unhealthy for Sensitive Groups':
        bg_color = '#ff7e00'  # Oranye
    elif row['Kategori'] == 'Unhealthy':
        bg_color = '#ff0000'  # Merah
    elif row['Kategori'] == 'Very Unhealthy':
        bg_color = '#99004c'  # Ungu
    elif row['Kategori'] == 'Hazardous':
        bg_color = '#7e0023'  # Coklat tua
    else:
        bg_color = '#f0f0f5'  # Default (warna abu-abu terang jika kategori tidak dikenali)

    # Menampilkan setiap row dengan warna background sesuai kategorinya
    st.markdown(f"""
    <div style="background-color:{bg_color};padding:5px;border-radius:2.5px;margin-bottom:5px;">
        <h3 style="color:#0073e6; display: inline-block;">AQI Category: <b>{row['Kategori']}</b></h3>
        <p style="font-size:16px;">Date: {row['Date Time'].strftime('%Y-%m-%d')}</p>
        <p style="font-size:16px;">Temperature: <b>{row['TEMP']:.2f} °C</b></p>
        <p style="font-size:16px;">Pressure: <b>{row['PRES']:.2f} hPa</b></p>
    </div>
    """, unsafe_allow_html=True)

# Optional: Display the daily average data in a table format as well if needed
st.write("Daily Forecast Details:")
st.dataframe(daily_avg[['Date Time', 'Kategori', 'TEMP', 'PRES']])

st.subheader("Tren Rata Rata AQI based on PM2.5 on Station Aotizhonxin")
Annual_avg_pm25 = AQI_A.groupby( 'year')['AQI'].mean().reset_index()
plt.figure(figsize=(8, 8))
plt.plot(Annual_avg_pm25['year'], Annual_avg_pm25['AQI'], marker='o', linewidth=1, color='red')
plt.title('Tren Rata-Rata AQI based on PM2.5 per Tahun')
plt.xlabel('Tahun')
plt.ylabel('Rata Rata AQI')
plt.grid(axis='y')
st.pyplot(plt)


st.subheader("Rata Rata AQI per bulan dalam rentang tahun 2013 - 2016")
Monthly_Average_AQI_Aotizhongxin = AQI_A.groupby(['year', 'month'])['PM2.5'].mean().reset_index() if station_choice == "Station Aotizhongxin" else AQI_B.groupby(['year', 'month'])['PM2.5'].mean().reset_index()

fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(60, 20))
years = [2013, 2014, 2015, 2016]

for i, year in enumerate(years):
    # Filter data untuk tahun yang sesuai
    data_year = Monthly_Average_AQI_Aotizhongxin[Monthly_Average_AQI_Aotizhongxin['year'] == year]

    # Buat list untuk menyimpan warna berdasarkan kondisi AQI
    colors = []
    for value in data_year['PM2.5']:
        if value >= 0 and value <= 50:
            colors.append('green')
        elif value >= 51 and value <= 100:
            colors.append('yellow')
        elif value >= 101 and value <= 150:
            colors.append('orange')
        elif value >= 151 and value <= 200:
            colors.append('red')
        elif value >= 201 and value <= 300:
            colors.append('purple')
        else:
            colors.append('black')

    # Membuat bar plot dengan warna yang sesuai
    sns.barplot(x='month', y='PM2.5', data=data_year, palette=colors, ax=ax[i])

    ax[i].set_title(f'Trend Kualitas Udara per Bulan {year}')
    ax[i].set_xlabel('Bulan')
    ax[i].set_ylabel('Rata-rata AQI PM2.5')

plt.tight_layout()
st.pyplot(plt)

st.subheader("Persentase Pollutant di station Aotizhongxin")
category_counts = AQI_A['Kategori'].value_counts()
# Mengambil kategori dan jumlahnya
categories = category_counts.index  # Indeks dari Series category_counts
counts = category_counts.values      # Nilai dari Series category_counts
colors = []
for kategori in categories:
    if kategori == 'Good':
        colors.append('green')
    elif kategori == 'Moderate':
        colors.append('yellow')
    elif kategori == 'Unhealthy for Sensitive Groups':
        colors.append('orange')
    elif kategori == 'Unhealthy':
        colors.append('red')
    elif kategori == 'Very Unhealthy':
        colors.append('purple')
    elif kategori == 'Hazardous':
        colors.append('maroon')
    else:
        colors.append('gray')

# Membuat pie chart
plt.figure(figsize=(8, 8))
plt.pie(counts, labels=categories, autopct='%1.1f%%', colors=colors)
plt.title('Distribution of PM2.5 Levels by AQI Category')

# Menampilkan pie chart
plt.show()
st.pyplot(plt)


RataRataTahunan = AQI_A.groupby('year')['PM10'].mean().reset_index()
Annual_AvarageAQI_inDongsi = AQI_B.groupby('year')['PM10'].mean().reset_index()
def ComparisonAirQuality():
    plt.figure(figsize=(11,7))
    plt.plot(RataRataTahunan['year'],RataRataTahunan['PM10'],label = 'Station Aoxtinghin' , color ='blue')
    plt.plot(Annual_AvarageAQI_inDongsi['year'],Annual_AvarageAQI_inDongsi['PM10'],label = 'Station Dongsi', color ='red')
    plt.xlabel('Month')
    plt.ylabel('Average PM2.5')
    plt.title('Comparison of Air Quality (PM10) Between Station A and B')
    plt.legend()
    plt.show()

ComparisonAirQuality()
st.pyplot(plt)