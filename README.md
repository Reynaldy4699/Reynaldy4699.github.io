# Reynard Kamadjaja, S.Kom. — Portfolio Website

Website portofolio bergaya **Zenless Zone Zero (ZZZ) / Neo-Brutalist Kinetic UI** dengan tema warna **Hijau Mint & Biru Muda (Green & Light Blue)**, dibangun menggunakan **React + Vite**.

## ✨ Fitur Utama
- **Animasi Teks Bergerak Kiri & Kanan (ZZZ Style Marquee):** Teks raksasa di latar belakang dan pita ticker bergerak secara dinamis ke kiri dan kanan.
- **Bilingual Toggle (`ID ⇄ EN`):** Mendukung Bahasa Indonesia dan Bahasa Inggris secara instan di seluruh bagian halaman.
- **Dark Mode & Light Mode Toggle (`DARK ⇄ LIGHT`):** Beralih antara mode gelap dan terang dengan tetap mempertahankan kontras neo-brutalist.
- **Integrasi Credly Resmi:** Terhubung langsung ke [credly.com/users/rey-kamadjaya](https://www.credly.com/users/rey-kamadjaya).
- **Siap Deploy ke GitHub Pages / Vercel / Netlify:** Konfigurasi `vite.config.js` sudah menggunakan relative base path (`./`).

## 🚀 Cara Menjalankan di Localhost
```bash
npm install
npm run dev
```

## 🌐 Cara Menghubungkan ke GitHub & Hosting untuk LinkedIn
1. Buat repository baru di GitHub (misalnya `portofolio` atau `reynard-portfolio`).
2. Jalankan perintah berikut di terminal folder ini:
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio website commit"
   git branch -M main
   git remote add origin https://github.com/USERNAME_KAMU/NAMA_REPO.git
   git push -u origin main
   ```
3. Untuk langsung online gratis, hubungkan repository GitHub tersebut ke **Vercel** atau **GitHub Pages** (via GitHub Actions Vite workflow), lalu tempelkan URL hasilnya di bagian **Featured / Contact Info** profil LinkedIn kamu.
