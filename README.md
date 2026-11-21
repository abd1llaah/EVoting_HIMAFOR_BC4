# 🗳️ E-Voting Terdesentralisasi (DApp) - HIMAFOR

Aplikasi pemungutan suara digital berbasis *blockchain* yang dikembangkan menggunakan **Solidity (Hardhat)** sebagai *Smart Contract* dan **Python (Streamlit & Web3.py)** sebagai antarmuka pengguna (*User Interface*). Sistem ini dirancang untuk menjamin transparansi, keamanan data, serta mencegah kecurangan pemilihan ganda (*double voting*) karena setiap suara dicatat secara permanen di jaringan *blockchain*.

🔗 **Link Repositori GitHub:** <https://github.com/cndyamee/evoting-dapp-blockchain>

## 👥 Anggota Kelompok

* **Cindy Amelia** (NIM: *Isi NIM*)
* **Nama Anggota 2** (NIM: *Isi NIM*)
* **Nama Anggota 3** (NIM: *Isi NIM*)

## 🛠️ Teknologi & Struktur Proyek

* **Smart Contract:** Solidity (`contracts/EVotingHIMAFOR.sol`)
* **Blockchain Environment:** Hardhat (Local Ethereum Network)
* **Frontend / UI:** Python & Streamlit (`app.py`)
* **Blockchain Bridge:** Web3.py
* **Visualisasi Data:** Pandas & Plotly Express

```text
evoting-dapp-blockchain/
├── artifacts/               # Hasil kompilasi Smart Contract (ABI & Bytecode)
├── contracts/
│   └── EVotingHIMAFOR.sol   # Smart Contract utama E-Voting
├── scripts/
│   └── deploy.js            # Skrip deployment kontrak ke jaringan Hardhat
├── uploads/                 # Direktori penyimpanan lokal foto kandidat
├── app.py                   # Aplikasi utama Frontend Streamlit & Web3.py
├── deployment.json          # Menyimpan alamat kontrak hasil deploy
├── hardhat.config.js        # Konfigurasi jaringan Hardhat
├── package.json             # Dependensi Node.js / Hardhat
├── requirements.txt         # Dependensi Python (Streamlit, Web3.py, dll.)
└── README.md                # Dokumentasi proyek
```

## 🚀 Cara Menjalankan Aplikasi (VS Code & Terminal)

Pastikan komputer Anda sudah terinstal **Node.js (versi LTS)** dan **Python (versi 3.9 ke atas)**.

### 1. Clone Repositori & Buka di VS Code

Buka terminal / Command Prompt, unduh proyek dari GitHub, lalu buka foldernya di **VS Code**:

```bash
git clone https://github.com/cndyamee/evoting-dapp-blockchain.git
cd evoting-dapp-blockchain
code .
```

### 2. Instal Dependensi

Buka terminal di VS Code (`Ctrl + ~`), lalu instal pustaka Node.js dan Python:

```bash
npm install
pip install -r requirements.txt
```

### 3. Jalankan Node Lokal Blockchain (Terminal 1)

Pada terminal pertama di VS Code, jalankan jaringan *blockchain* lokal Hardhat:

```bash
npx hardhat node
```

> **Penting:** Biarkan terminal pertama ini tetap berjalan. Di terminal ini akan muncul daftar 20 akun *wallet* beserta alamatnya (`Account #0` sampai `Account #19`):
> * **Account #0:** Otomatis menjadi alamat **Admin**.
> * **Account #1, #2, dst.:** Digunakan sebagai alamat **Wallet Pemilih**.

### 4. Compile & Deploy Smart Contract (Terminal 2)

Buka **terminal kedua** (klik ikon `+` di panel terminal VS Code), lalu jalankan perintah berikut untuk mengompilasi dan men-*deploy* smart contract ke jaringan lokal:

```bash
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

### 5. Jalankan Antarmuka Web Streamlit (Terminal 2)

Masih di terminal kedua, jalankan aplikasi Streamlit:

```bash
streamlit run app.py
```

Aplikasi web akan otomatis terbuka di browser pada alamat `http://localhost:8501`.

## 🧭 Panduan Penggunaan & Alur Aplikasi (Step-by-Step)

Setelah aplikasi terbuka di browser dan indikator di sidebar menunjukkan **`🟢 Hardhat Node Connected`**, ikuti urutan penggunaan berikut:

### Tahap 1: Persiapan Admin (`6. Admin Panel`)

1. Salin alamat **Account #0 (Admin)** dari Terminal 1 VS Code, tempelkan ke kolom **Alamat Wallet (Hardhat)** di sidebar kiri, lalu **tekan `Enter`**.
2. Buka menu **`6. Admin Panel`**.
3. **Registrasi & Verifikasi Pemilih 1:**
   * Salin alamat **Account #1** (pemilih ke-1) dari terminal, tempel di kolom *Registrasi Pemilih*, lalu klik **Daftarkan Pemilih**.
   * Setelah berhasil didaftarkan, langsung tempelkan alamat **Account #1** tersebut ke kolom *Verifikasi Pemilih* di bawahnya, lalu klik **Verifikasi Pemilih**.
4. **Registrasi & Verifikasi Pemilih 2:**
   * Ulangi langkah yang sama untuk pemilih berikutnya: tempel alamat **Account #2** ke kolom *Registrasi Pemilih* -> klik **Daftarkan Pemilih**, lalu langsung tempel ke kolom *Verifikasi Pemilih* -> klik **Verifikasi Pemilih**.
5. **Buka Pemilihan:** Scroll ke bagian paling bawah pada halaman Admin Panel, lalu klik tombol **`🟢 Buka Pemilihan`**.

### Tahap 2: Pendaftaran & Melihat Kandidat (`3. Form Input Kandidat` & `2. Candidate List & Detail`)

1. Dengan masih menggunakan alamat wallet **Admin (Account #0)** di sidebar, buka menu **`3. Form Input Kandidat`**.
2. Isi **Nama Lengkap Kandidat**, **Visi**, **Misi**, dan unggah **Foto Kandidat (JPG/PNG)**, lalu klik **Simpan Kandidat ke Blockchain**. Ulangi untuk menambahkan kandidat kedua dan seterusnya.
3. Buka menu **`2. Candidate List & Detail`** untuk memastikan seluruh profil, foto, dan visi-misi kandidat sudah tampil dan tercatat di blockchain.

### Tahap 3: Proses Pemungutan Suara (`4. Voting Page`)

1. Ganti alamat wallet di sidebar kiri dengan alamat **Account #1 (Pemilih 1)**, lalu **jangan lupa tekan `Enter`** hingga muncul status *Wallet Valid*.
2. Buka menu **`4. Voting Page`**, pilih salah satu kandidat dengan menekan tombol **Pilih Kandidat**, lalu konfirmasi dengan menekan **Ya, Kirim Suara** hingga muncul notifikasi **Pemilihan Berhasil** beserta *Transaction Hash*-nya.
3. Ulangi langkah di atas menggunakan alamat **Account #2 (Pemilih 2)** (tempel di sidebar -> tekan **`Enter`** -> pilih kandidat -> konfirmasi suara).
4. *(Opsional)* Jika mencoba memilih ulang menggunakan wallet yang sudah memilih, sistem akan otomatis memblokir dengan pesan *"Wallet ini sudah menggunakan hak pilih"*.

### Tahap 4: Penutupan Sesi & Melihat Hasil Akhir (`6. Admin Panel` -> `5. Results & Verification`)

1. Untuk melihat rekapitulasi hasil akhir, masukkan kembali alamat **Admin (Account #0)** di sidebar (tekan **`Enter`**), lalu buka menu **`6. Admin Panel`**.
2. Scroll ke bagian paling bawah dan klik tombol **`🔴 Tutup Pemilihan`**.
3. Setelah pemilihan resmi ditutup, buka menu **`5. Results & Verification`**. Hasil akhir perolehan suara (tabel rekapitulasi & grafik batang) serta **Riwayat Transaksi Voting** (*Tx ID* dan waktu pemilihan) akan otomatis tampil di halaman tersebut.

## 📱 Penjelasan Fungsi Setiap Halaman & Hubungan UI dengan Smart Contract

Antarmuka `app.py` terhubung ke *Smart Contract* `EVotingHIMAFOR.sol` melalui pustaka **Web3.py** menggunakan alamat kontrak dari `deployment.json` dan ABI dari folder `artifacts/`. Interaksi terbagi menjadi **Call** (membaca data tanpa biaya *gas*) dan **Transact** (mengirim transaksi perubahan data ke *blockchain*).

### 1. Dashboard (`1. Dashboard`)

* **Fungsi:** Menampilkan ringkasan statistik pemilihan secara *real-time* (jumlah kandidat, total suara masuk, jumlah pemilih unik, status pemilihan, serta info alamat kontrak dan jaringan RPC).
* **Hubungan dengan Smart Contract:** Memanggil fungsi *view* `candidateCount()` dan membaca log *event* `VoteCast` untuk menghitung total partisipasi.

### 2. Candidate List & Detail (`2. Candidate List & Detail`)

* **Fungsi:** Menampilkan kartu profil seluruh kandidat (foto, nama, visi, misi, dan perolehan suara sementara), tabel daftar kandidat, serta pencarian detail kandidat berdasarkan ID.
* **Hubungan dengan Smart Contract:** Melakukan perulangan memanggil fungsi `getCandidate(id)` untuk mengambil data kandidat dari penyimpanan *blockchain* dan menggabungkannya dengan foto lokal di folder `uploads/`.

### 3. Form Input Kandidat (`3. Form Input Kandidat`)

* **Fungsi:** Formulir bagi Admin untuk mendaftarkan kandidat baru beserta pengunggahan foto kandidat.
* **Hubungan dengan Smart Contract:** Memvalidasi hak akses menggunakan fungsi `admin()`, lalu mengeksekusi transaksi `registerCandidate(nama, visi, misi)` untuk menyimpan data kandidat ke *blockchain*.

### 4. Voting Page (`4. Voting Page`)

* **Fungsi:** Bilik pemungutan suara digital tempat pemilih memberikan hak suaranya setelah melakukan konfirmasi pilihan.
* **Hubungan dengan Smart Contract:** Memeriksa kelayakan pemilih lewat `getVoterStatus(address)` dan status sesi lewat `electionOpen()`. Saat suara dikonfirmasi, UI mengirim transaksi `vote(candidateId)` untuk menambah suara kandidat sekaligus mengunci *wallet* pemilih agar tidak bisa memilih dua kali.

### 5. Results & Verification (`5. Results & Verification`)

* **Fungsi:** Menampilkan tabel dan grafik batang hasil akhir pemilihan setelah sesi ditutup, fitur pengecekan status hak pilih suatu *wallet*, serta tabel audit riwayat transaksi voting.
* **Hubungan dengan Smart Contract:** Memanggil fungsi `getResults()` ketika `electionOpen()` bernilai `false` (ditutup), serta menarik riwayat *event* `VoteCast` dari blok awal hingga terbaru untuk menampilkan *Transaction Hash (`Tx ID`)* dan *timestamp* sebagai bukti transparansi.

### 6. Admin Panel (`6. Admin Panel`)

* **Fungsi:** Pusat kendali panitia/admin untuk mendaftarkan pemilih, memverifikasi pemilih, serta membuka dan menutup sesi pemilihan.
* **Hubungan dengan Smart Contract:** Dilindungi validasi `admin()`. Tombol-tombol aksinya memanggil fungsi transaksi `registerVoter(address)`, `verifyVoter(address)`, `openElection()`, dan `closeElection()`.