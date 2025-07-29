# Dermatell Projesi - Entegrasyon ve Kullanım Dökümantasyonu

## 1. Genel Bakış
Bu doküman, 29 Temmuz'te yapılan frontend-backend entegrasyonlarını, önemli kod değişikliklerini, kullanıcı akışlarını ve yapılacaklar listesini özetler.

---

## 2. Entegrasyonlar ve Yapılanlar

### 2.1. Login & Signup Akışı
- **Signup:**
  - Form alanları: Ad (name), Soyad (surname), Email, Şifre
  - Backend'e gönderilen JSON:
    ```json
    {
      "name": "string",
      "surname": "string",
      "email": "user@example.com",
      "password": "string"
    }
    ```
  - Başarılı kayıt sonrası otomatik olarak giriş sayfasına yönlendirme

- **Login:**
  - Form alanları: Email, Şifre
  - Backend'e gönderilen JSON:
    ```json
    {
      "email": "user@example.com",
      "password": "string"
    }
    ```
  - Başarılı giriş sonrası JWT token localStorage'a kaydedilir ve chat ekranına yönlendirilir.

- **CORS:**
  - Sadece `http://localhost:3000` ve Railway backend domaini izinli olacak şekilde backend'e CORS middleware eklendi.

### 2.2. Chat Ekranı & Model Entegrasyonu
- **JWT Kontrolü:**
  - Kullanıcı login değilse chat ekranına erişemez, otomatik olarak giriş sayfasına yönlendirilir.
- **Logout:**
  - Çıkış butonu ile localStorage'daki token silinir ve giriş sayfasına yönlendirilir.
- **Görsel Yükleme:**
  - "Mesajınızı yazın..." inputuna tıklanınca dosya seçici açılır, görsel seçilirse otomatik olarak modele gönderilir.
  - Modelden dönen json, Türkçe ve okunabilir şekilde chat baloncuğunda gösterilir.
  - Örnek çıktı:
    ```
    Hastalık: acne
    Olasılık: %27.34
    Açıklama: Akne, yani sivilce, ciltteki yağ bezlerinin tıkanmasıyla oluşan yaygın bir cilt sorunudur.
    ```

---

## 3. Dosya ve Kod Değişiklikleri

### Frontend (app/)
- `templates/signin.html`, `static/signin.js`: Login formu ve JS entegrasyonu
- `templates/signup.html`, `static/signup.js`: Signup formu ve JS entegrasyonu
- `templates/chat.html`, `static/chat.js`: Chat ekranı, görsel yükleme ve model entegrasyonu
- `static/signin.css`: Tüm formlarda modern ve tutarlı stil

### Backend (backend/app/)
- `main.py`: CORS middleware eklendi, sadece izinli originler açık bırakıldı

---

## 4. Kullanıcı Akışı
1. **Kayıt Ol:**
   - Ad, Soyad, Email ve Şifre ile kayıt olunur.
   - Başarılı kayıt sonrası giriş ekranına yönlendirilir.
2. **Giriş Yap:**
   - Email ve Şifre ile giriş yapılır.
   - Başarılı giriş sonrası chat ekranına yönlendirilir.
3. **Chat ve Tahmin:**
   - Chat ekranında mesaj kutusuna tıklanır, görsel seçilir ve otomatik olarak modele gönderilir.
   - Sonuç, bot mesajı olarak baloncukta gösterilir.
4. **Çıkış:**
   - Çıkış butonuna tıklanarak oturum sonlandırılır.

---

## 5. TODO Listesi
- [x] Signup formunu backend ile uyumlu hale getir
- [x] Login formunu backend ile uyumlu hale getir
- [x] JWT token ile chat ekranı koruması
- [x] Logout fonksiyonu
- [x] Görsel yükleme ve model entegrasyonu
- [x] Modelden dönen json'u düzgün Türkçe metin olarak göster
- [x] CORS ayarlarını sadece local ve canlı frontend için aç
- [x] Tüm formlarda modern ve tutarlı stil
- [ ] (Gelecek) Chat ekranında metin tabanlı AI asistanı
- [ ] (Gelecek) Kullanıcı profil ekranı

---

## 6. Notlar
- Tüm endpointler canlı backend'e (`https://bootcampprojectyzta-production.up.railway.app`) yönlendirilmiştir.
- CORS ayarları canlıya geçerken sadece gerçek frontend domainine açılmalıdır.
- Modelden dönen json formatı değişirse, chat.js'teki işleme fonksiyonu güncellenmelidir.

---

## 7. Geliştiriciye Notlar
- Frontend'i localde çalıştırmak için (örn. React ile):
  - CORS izinli port: `http://localhost:3000`
- Tüm JS dosyaları modern ES6+ ile yazılmıştır.
- Herhangi bir hata veya yeni özellik için bu doküman güncellenmelidir. 