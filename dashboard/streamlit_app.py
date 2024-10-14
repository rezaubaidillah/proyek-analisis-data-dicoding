import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.ticker as mticker
import matplotlib.dates as mdates


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule="D", on="dteday").agg(
        {
            "instant": "nunique",
            "cnt": "sum",
        }
    )
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(
        columns={"instant": "order_count", "cnt": "counts"}, inplace=True
    )
    return daily_orders_df
# Fungsi untuk mengklasifikasikan waktu berdasarkan jam


def time_of_day_cluster(row):
    if 5 <= row['hr'] < 12:
        return "Morning"
    elif 12 <= row['hr'] < 18:
        return "Afternoon"
    elif 18 <= row['hr'] < 21:
        return "Evening"
    else:
        return "Night"

# Fungsi clustering berdasarkan temperature


def temp_cluster(row):
    if row['temp'] < 0.3:
        return 'Low Temp'
    elif 0.3 <= row['temp'] < 0.7:
        return 'Medium Temp'
    else:
        return 'High Temp'

# Fungsi clustering berdasarkan humidity


def humidity_cluster(row):
    if row['hum'] < 0.4:
        return 'Low Humidity'
    elif 0.4 <= row['hum'] < 0.7:
        return 'Medium Humidity'
    else:
        return 'High Humidity'

# Fungsi clustering berdasarkan windspeed


def windspeed_cluster(row):
    if row['windspeed'] < 0.2:
        return 'Low Wind'
    elif 0.2 <= row['windspeed'] < 0.5:
        return 'Medium Wind'
    else:
        return 'High Wind'

# Fungsi clustering berdasarkan musim


def season_cluster(row):
    if row['season'] == 1:
        return 'Spring Season'
    elif row['season'] == 2:
        return 'Summer Season'
    elif row['season'] == 3:
        return 'Fall Season'
    else:
        return 'Winter Season'

# Fungsi clustering berdasarkan kondisi cuaca


def weather_cluster(row):
    if row['weathersit'] == 1:
        return 'Clear Weather'
    elif row['weathersit'] == 2:
        return 'Mist Weather'
    elif row['weathersit'] == 3:
        return 'Light Weather'
    else:
        return 'Heavy Weather'

# Fungsi clustering hari libur


def is_holiday_cluster(row):
    if row['holiday'] == 1:
        return 'Holiday'
    else:
        return 'Not Holiday'

# Fungsi clustering hari kerja


def is_workingday_cluster(row):
    if row['workingday'] == 1:
        return 'Workingday'
    else:
        return 'Not Workingday'

# Fungsi clustering hari dalam seminggu


def day_cluster(row):
    if row['weekday'] == 0:
        return 'Minggu'
    elif row['weekday'] == 1:
        return 'Senin'
    elif row['weekday'] == 2:
        return 'Selasa'
    elif row['weekday'] == 3:
        return 'Rabu'
    elif row['weekday'] == 4:
        return 'Kamis'
    elif row['weekday'] == 5:
        return 'Jumat'
    else:
        return 'Sabtu'

# Fungsi untuk menghitung statistik


def calculate_statistic(data, column, statistic_select):
    if statistic_select == 'Max':
        return data.groupby(column)['cnt'].max().reset_index()
    elif statistic_select == 'Mean':
        return data.groupby(column)['cnt'].mean().round(4).reset_index()
    elif statistic_select == 'Sum':
        return data.groupby(column)['cnt'].sum().reset_index()
    elif statistic_select == 'percentile_q1':
        # contoh percentile 25%
        return data.groupby(column)['cnt'].quantile(0.25).reset_index()
    elif statistic_select == 'Median':
        return data.groupby(column)['cnt'].median().reset_index()
    elif statistic_select == 'percentile_q3':
        # contoh percentile 75%
        return data.groupby(column)['cnt'].quantile(0.75).reset_index()
    elif statistic_select == 'variance':
        return data.groupby(column)['cnt'].var().reset_index()
    elif statistic_select == 'standar_deviation':
        return data.groupby(column)['cnt'].std().reset_index()

# Fungsi plot bar chart dengan warna highlight


def plot_with_highlight(data, x_column, title, statistic_select):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Hitung statistik yang dipilih pengguna
    count_data = calculate_statistic(data, x_column, statistic_select)

    # Cari nilai maksimal
    max_value = count_data['cnt'].max()

    # Buat warna berdasarkan logika pewarnaan
    colors = ['orange' if x ==
              max_value else 'skyblue' for x in count_data['cnt']]

    # Plot menggunakan seaborn dengan pewarnaan custom
    sns.barplot(x=x_column, y='cnt', data=count_data, palette=colors, ax=ax)

    # Set judul
    ax.set_title(f"{title} ({statistic_select})", fontsize=16)

    # Label sumbu
    ax.set_xlabel(x_column.replace('_', ' ').capitalize(), fontsize=12)
    ax.set_ylabel(f'Total Rentals ({statistic_select})', fontsize=12)

    # Menambahkan angka di atas setiap batang
    for index, row in count_data.iterrows():
        ax.text(index, row['cnt'] / 2,  # Letakkan di tengah batang
                f'{row["cnt"]:,}', ha='center', va='center', fontsize=12, color='black')

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

# Fungsi plot untuk casual vs registered users


def plot_casual_vs_registered(data, statistic_select):
    if statistic_select == 'Sum':
        total_casual = data['casual'].sum()
        total_registered = data['registered'].sum()
    elif statistic_select == 'Mean':
        total_casual = data['casual'].mean()
        total_registered = data['registered'].mean()
    elif statistic_select == 'Max':
        total_casual = data['casual'].max()
        total_registered = data['registered'].max()

    # Membuat data untuk plot
    rental_data = pd.DataFrame({
        'User Type': ['Casual Users', 'Registered Users'],
        'Total Rentals': [total_casual, total_registered]
    })

    # Warna: orange untuk nilai tertinggi dan skyblue untuk yang lainnya
    max_value = rental_data['Total Rentals'].max()
    colors = ['orange' if x == max_value else 'skyblue' for x in rental_data['Total Rentals']]

    # Membuat bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='User Type', y='Total Rentals', data=rental_data, palette=colors, ax=ax)

    # Set judul dan label sumbu
    ax.set_title(f"Casual vs Registered Users ({statistic_select})", fontsize=16, pad=20)
    ax.set_xlabel("User Type", fontsize=12)
    ax.set_ylabel(f"Total Rentals ({statistic_select})", fontsize=12)

    # Menambahkan angka di dalam batang
    for i, value in enumerate(rental_data['Total Rentals']):
        ax.text(i, value / 2, f'{value:,.0f}', ha='center', va='center', fontsize=12, color='black')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)


# Memuat data
all_df = pd.read_csv(
    "/dashboard/hour.csv")
day_df = pd.read_csv(
    "/dashboard/day.csv")
# Konversi kolom tanggal ke datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])
day_df["dteday"] = pd.to_datetime(day_df["dteday"])


# Sidebar untuk memilih rentang tanggal
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/256/2972/2972215.png", width=100)
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Validasi input tanggal
if start_date > end_date:
    st.error("Tanggal mulai tidak boleh lebih besar dari tanggal akhir!")
else:
    st.success("Tanggal Valid")

    # Filter berdasarkan rentang tanggal
    main_df = all_df[(all_df["dteday"] >= pd.to_datetime(start_date)) &
                     (all_df["dteday"] <= pd.to_datetime(end_date))]
    daily_orders_df = create_daily_orders_df(main_df)
    # Clustering berdasarkan faktor eksternal
    main_df['time_of_day_cluster'] = main_df.apply(time_of_day_cluster, axis=1)
    main_df['temp_cluster'] = main_df.apply(temp_cluster, axis=1)
    main_df['humidity_cluster'] = main_df.apply(humidity_cluster, axis=1)
    main_df['windspeed_cluster'] = main_df.apply(windspeed_cluster, axis=1)
    main_df['season_cluster'] = main_df.apply(season_cluster, axis=1)
    main_df['weather_cluster'] = main_df.apply(weather_cluster, axis=1)
    main_df['is_holiday_cluster'] = main_df.apply(is_holiday_cluster, axis=1)
    main_df['is_workingday_cluster'] = main_df.apply(
        is_workingday_cluster, axis=1)
    main_df['day_cluster'] = main_df.apply(day_cluster, axis=1)

    st.header("Rent Bike Dashboard :sparkles:")
    st.subheader("Daily Orders")

    with st.container():
        total_orders = daily_orders_df.order_count.sum()
        total_counts = daily_orders_df.counts.sum()
        st.metric("Total orders", value=total_orders)
        st.metric("Total People Rent", value=total_counts)

    # Menentukan interval berdasarkan rentang waktu
    date_diff = (end_date - start_date).days
    if date_diff > 365:       # Jika lebih dari 1 tahun
        interval = 30          # Tampilkan setiap 30 hari
    elif date_diff > 180:      # Jika lebih dari 6 bulan
        interval = 7           # Tampilkan setiap 7 hari
    elif date_diff > 120:       # Jika lebih dari 2 bulan
        interval = 5           # Tampilkan setiap 2 hari
    elif date_diff > 90:
        interval = 4
    elif date_diff > 60:       # Jika lebih dari 2 bulan
        interval = 3           # Tampilkan setiap 2 hari
    elif date_diff > 30:
        interval = 2
    else:
        interval = 1           # Default setiap hari

    # Visualisasi daily orders dengan y-axis sebagai bilangan bulat
    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot data daily orders sebagai line chart
    ax.plot(daily_orders_df["dteday"], daily_orders_df["counts"],
            marker="o", linewidth=2, color="#90CAF9")

    # Memastikan y-axis menampilkan bilangan bulat saja
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    # Mengatur format tanggal pada sumbu X
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))

    # Mengatur ukuran label
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)

    # Rotasi label tanggal agar tidak tumpang tindih
    plt.xticks(rotation=45, ha="right")

    # Menambahkan judul dan label sumbu
    ax.set_title("Daily Orders Over Time", fontsize=24)
    ax.set_xlabel("Date", fontsize=18)
    ax.set_ylabel("People Rent", fontsize=18)

    # Menambahkan grid untuk memudahkan pembacaan
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

    # Membuat selectbox untuk setiap faktor eksternal
    casual_register_select = st.selectbox(
        label="Casual Vs Register Cluster Filter",
        options=('Sum','Mean','Max',)
    )
    # Plot untuk faktor eksternal casual register
    plot_casual_vs_registered(main_df, casual_register_select)
    
    time_of_day_select = st.selectbox(
        label="Time Of Day Cluster Filter",
        options=('Sum','Mean','Max',
                 'percentile_q1', 'Median', 'percentile_q3', 'variance', 'standar_deviation')
    )
    # Plot untuk faktor eksternal temp
    plot_with_highlight(main_df, "time_of_day_cluster",
                        "Time Cluster", time_of_day_select)
    
    temp_statistic_select = st.selectbox(
        label="Temperature Cluster Filter",
        options=('Sum','Mean','Max',
                 'percentile_q1', 'Median', 'percentile_q3', 'variance', 'standar_deviation')
    )
    # Plot untuk faktor eksternal temp
    plot_with_highlight(main_df, "temp_cluster",
                        "Temperature Cluster", temp_statistic_select)
    humidity_statistic_select = st.selectbox(
        label="Humidity Cluster Filter",
        options=('Sum','Mean','Max',
                 'percentile_q1', 'Median', 'percentile_q3', 'variance', 'standar_deviation')
    )
    # Plot untuk faktor eksternal hum
    plot_with_highlight(main_df, "humidity_cluster",
                        "Humidity Cluster", humidity_statistic_select)
    
    windspeed_statistic_select = st.selectbox(
        label="Windspeed Cluster Filter",
        options=('Sum','Mean','Max',
                 'percentile_q1', 'Median', 'percentile_q3', 'variance', 'standar_deviation')
    )
    # Plot untuk faktor eksternal windspeed
    plot_with_highlight(main_df, "windspeed_cluster",
                        "Windspeed Cluster", windspeed_statistic_select)
    season_statistic_select = st.selectbox(
        label="Season Cluster Filter",
        options=('Sum','Mean','Max',
                 'percentile_q1', 'Median', 'percentile_q3', 'variance', 'standar_deviation')
    )
    # Plot untuk faktor eksternal season
    plot_with_highlight(main_df, "season_cluster",
                        "Season Cluster", season_statistic_select)
    weather_statistic_select = st.selectbox(
        label="Weather Condition Cluster Filter",
        options=('Sum','Mean','Max',
                 'percentile_q1', 'Median', 'percentile_q3', 'variance', 'standar_deviation')
    )
    # Plot untuk faktor eksternal weather
    plot_with_highlight(main_df, "weather_cluster",
                        "Weather Condition Cluster", weather_statistic_select)
    holiday_statistic_select = st.selectbox(
        label="Holiday Cluster Filter",
        options=('Sum','Mean','Max',
                 'percentile_q1', 'Median', 'percentile_q3', 'variance', 'standar_deviation')
    )
    # Plot untuk faktor eksternal is_holiday
    plot_with_highlight(main_df, "is_holiday_cluster",
                        "Holiday Cluster", holiday_statistic_select)
    workingday_statistic_select = st.selectbox(
        label="Workingday Cluster Filter",
        options=('Sum','Mean','Max',
                 'percentile_q1', 'Median', 'percentile_q3', 'variance', 'standar_deviation')
    )
    # Plot untuk faktor eksternal is_workingday
    plot_with_highlight(main_df, "is_workingday_cluster",
                        "Workingday Cluster", workingday_statistic_select)
    day_statistic_select = st.selectbox(
        label="Day of the Week Cluster Filter",
        options=('Sum','Mean','Max',
                 'percentile_q1', 'Median', 'percentile_q3', 'variance', 'standar_deviation')
    )
    # Plot untuk faktor eksternal
    plot_with_highlight(main_df, "day_cluster",
                        "Day of the Week Cluster", day_statistic_select)
    st.caption("Reza Ubaidillah (c)2024")
