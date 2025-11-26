Proyek ini merupakan pemrosesan citra KTP (Kartu Tanda Penduduk) menggunakan OpenCV & NumPy yang telah dipisahkan ke dalam beberapa file agar lebih rapi, modular, dan mudah dipelihara, tanpa mengubah logika, variabel, maupun cara kerja aslinya.

Struktur file:

📁 project_folder
│
├── main.py
├── preprocess.py
├── threshold_process.py
├── coordinate_process.py
└── KTP.jpg

1. main.py – File Utama (Orchestrator)

File ini adalah pengendali utama. Tugasnya:

Membaca gambar KTP.jpg

Memanggil seluruh fungsi pemrosesan

Menampilkan output final

Alur kerja di main.py
image = cv2.imread("KTP.jpg")

resized_image, mean_value_b, blue_threshold = preprocess_image(image)

combined_threshold2, threshold_gray = threshold_processing(resized_image, mean_value_b)

final = get_final_image(resized_image, image, combined_threshold2, threshold_gray, blue_threshold)


✅ Tidak ada logika dipindahkan atau diubah
✅ Hanya memanggil fungsi dari file lain

2. preprocess.py – Tahap Preprocessing Awal

Fungsi utama:

preprocess_image(image)


Tugas file ini:

Mengambil channel biru (Blue) dan merah (Red)

Melakukan GaussianBlur

Melakukan threshold pada channel

Menggabungkan (subtract) untuk membentuk area KTP

Mencari kontur terbesar

Melakukan:

Crop gambar

Rotasi jika perlu

Resize ke (900 x 600)

Menghitung rata-rata channel biru (mean B)

Output:

return resized_image, mean_value_b, blue_threshold


✅ Fokus file: membersihkan & menormalkan citra awal

3. threshold_process.py – Threshold Adaptif Lanjutan

Fungsi utama:

threshold_processing(resized_image, mean_value_b)


File ini melakukan:

Penyesuaian blur berdasarkan mean_value_b

Konversi ke grayscale

Penentuan nilai threshold dinamis:

threshold_value

threshold_value_r

Threshold untuk:

Channel B

Channel R

Grayscale

Menggabungkan hasil threshold:

combined_threshold2 = cv2.subtract(crop_threshold_b, crop_threshold_r)


Output:

return combined_threshold2, threshold_gray


✅ Fokus file: mempertegas area penting menggunakan threshold dinamis

4. coordinate_process.py – Pendeteksian Titik & Transformasi

Fungsi utama:

get_final_image(resized_image, image, combined_threshold2, threshold_gray, blue_threshold)


Ini adalah bagian paling kompleks dan penting:

Berisi:

find_nearest_coordinates() → mencari titik terdekat

Mendeteksi titik atas, bawah, kiri, kanan

Menentukan 4 sudut utama KTP

Koreksi posisi

Melakukan Perspective Transform (Warp)

Menghasilkan citra final dengan posisi lurus

Pada akhirnya menghasilkan:

return final


✅ Fokus file: mengoreksi perspektif & menyusun hasil akhir

Alur Lengkap Sistem

Berikut alur sederhana sistemnya:

KTP.jpg
   ↓
preprocess.py → crop + rotate + resize + mean B
   ↓
threshold_process.py → adaptive threshold
   ↓
coordinate_process.py → find points + warp
   ↓
Result → final image (ditampilkan)

Cara Menjalankan

Pastikan kamu sudah menginstal library berikut:

pip install numpy opencv-python


Lalu jalankan:

python main.py


Pastikan file KTP.jpg berada di folder yang sama dengan file .py.
