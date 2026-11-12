# Proyek Analisis Data: Bike Sharing Dashboard 🚲

Dashboard analisis penyewaan sepeda (Capital Bikeshare, Washington D.C., 2011-2012) menggunakan Streamlit.

**Nama:** M. Waliyul Ahdy

## Struktur Proyek
```
submission
├───dashboard
│   ├───main_data.csv
│   ├───hour_data.csv
│   └───dashboard.py
├───data
│   ├───day.csv
│   └───hour.csv
├───Proyek_Analisis_Data_final_asli.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
Jalankan dari folder utama proyek (folder yang berisi `dashboard/`):
```
streamlit run dashboard/dashboard.py
```
Jika berhasil, terminal akan menampilkan:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```
Buka **Local URL** tersebut di browser. Untuk menghentikan dashboard, tekan `Ctrl + C` di terminal.

## Catatan
- Notebook dijalankan di Google Colab (data dibaca dari `/content/day.csv` dan `/content/hour.csv`).
- `main_data.csv` dan `hour_data.csv` adalah hasil data cleaning dari notebook dan digunakan oleh dashboard.
