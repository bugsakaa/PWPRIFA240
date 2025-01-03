# aplikasi-pwp

## Fitur Aplikasi

### 1. Halaman Registrasi
- Form HTML untuk registrasi pengguna.
- Data yang dimasukkan akan disimpan ke database dengan hash password.

### 2. Halaman Login
- Form HTML untuk login pengguna.
- Jika login berhasil, simpan informasi pengguna ke **session**.

### 3. Halaman Dashboard (Hanya untuk Pengguna Login)
- Menampilkan daftar semua pengguna.
- Memiliki tombol untuk menambahkan, mengedit, dan menghapus pengguna.

### 4. Fitur CRUD
- **Tambah Pengguna**: Form untuk menambahkan pengguna baru.
- **Edit Pengguna**: Form untuk mengedit data pengguna berdasarkan ID.
- **Hapus Pengguna**: Tombol untuk menghapus pengguna.

### 5. Halaman Logout
- Tombol untuk logout pengguna dan menghapus session.

### 6. Model Database

### User
- `id`
- `username`
- `role`
- `email`
- `password_hash`



---
Buat virtual environment
```
python -m venv venv
```

Aktifkan virtual environment
```
.\venv\Scripts\activate
```

Install Dependencies
```
pip install -r requirements.txt
```


```
python app.py
```


