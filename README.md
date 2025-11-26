Autocropping & Perspective Warping untuk KTP Indonesia

Repository ini berisi implementasi Python untuk melakukan autocropping dan perspective warping pada gambar KTP (Kartu Tanda Penduduk) Indonesia.
Tujuan utamanya adalah meningkatkan akurasi OCR (Optical Character Recognition) dengan memastikan posisi KTP lurus, bersih, dan hanya area penting yang diproses.

--------------------------------------------------

STRUKTUR FILE

- main.py
- preprocess.py
- threshold_process.py
- coordinate_process.py
- KTP.jpg

--------------------------------------------------

FUNGSI SINGKAT FILE

main.py
Mengendalikan seluruh alur program utama dari awal hingga akhir.

preprocess.py
Tahap awal pengolahan citra:
- Pemisahan channel warna (Blue & Red)
- Gaussian Blur
- Threshold awal
- Erosi
- Deteksi kontur terbesar
- Cropping area KTP
- Rotasi otomatis
- Resize ke 900x600

threshold_process.py
Tahap lanjutan:
- Threshold dinamis berdasarkan mean value kanal biru
- Gaussian Blur lanjutan
- Penggabungan hasil threshold

coordinate_process.py
Tahap penentuan koordinat:
- Menentukan 4 titik sudut KTP
- Perspective warping
- Penentuan hasil akhir

--------------------------------------------------

CARA MENGGUNAKAN

1. Simpan gambar sebagai: KTP.jpg
2. Pastikan semua file ada di folder yang sama
3. Jalankan program dengan:

   python main.py

--------------------------------------------------

PERSYARATAN

- Python 3.x
- OpenCV
- NumPy

Install library:

pip install numpy opencv-python

--------------------------------------------------

HASIL AKHIR

Gambar KTP menjadi:
- Lurus (tidak miring)
- Ter-crop otomatis
- Bersih dari area tidak relevan
- Siap untuk OCR

--------------------------------------------------

Author : Muhammad Ilham
