# Versiyon 1.0

- Birebir konuşabilme, sohbet edebilme
- Gündelik işlemleri halledebilme
  - Saat
  - Tarih
    - Bugünün tarihi, yarının tarihi, 30 gün sonrasının tarihi gibi detayları verebilme.
  - Alarm
  - Anımsatıcı (Zamanı gelince okuyabilme)
    - Hızlı anımsatıcı
    - Anımsatıcı okuma
    - Anımsatıcı bildirimi (Show Balloon)
    - Anımsatıcı tamamlandı geri bildirimi
    - Anımsatıcı silme
    - Anımsatıcı istatistikleri
  - Not Alma
    - Hızlı not alma
    - Panoya kopyalanan metni notlara ekleme
    - Notları okuma
      - Notları getirmeden önce MYSQL'deki LIKE Komutu sayesinde işlemler gerçekleştirebilme
      - SELECT * FROM niyetli.notes where note_title LIKE 'zmx%';	
    - Kaynak
    - Son & İlk 5(x) notu getirme
    - Not silme
    - Not güncelleme
  - Not sayısı öğrenme
- Hava Durumu Kontrolu
- Dosya operasyonları
    - Dosya operasyonlarında kopyalanan dosya yolu üzerindeki dosya isimlerini değiştirme hizalama
- Windows operasyonları
  - Metin okuma
  - PDF okuma
  - Fotoğraf görüntüleme
  - Video durdurma, oynatma, ses kısma ve açma
- İşletim Sistemi Operasyonları
  - Bilgisayar Kapatma/Bekletme/Yeniden Başlatma
    - Bu işlemlerin iptali
- Mail İşlemleri
  - Girilen mail adresine mail gönderme işlemi
- Ekran Süresi
  - Genel çalışır bir ekran zamanlayıcısı
  - Günde hangi programa kaç gere girildi? Sorusuna cevap bulabilme
  - Veritabanı ile senkronize çalışma
  - Kullanıcıya Ekran Süresi istatistiklerini verebilme.
- Tarayıcı işlemleri
  - Tarayıcıdaki belirli yerdeki metni seslendirme
    - Beautiful Soup kütüphanesi kullanarak bir web sitesindeki HTML etiketlerindeki yazıları çekebilme
  - Scroll Down - Up işlemleri
  - Sekme işlemleri (değiştirme, yeni sekme açma, kapama)
  - Arama motoru araması (DuckDuck Go)
  - Arama motorunda söylenen sonuca giriş yapabilme
- Arayüz hazırlama
  - Proje ile uyumlu çalışacak şekilde arayüz
  - Diyalogları ve Komutları kaydedecek şekilde arayüz üzerinde gösterim gerçekleştirebilme
  - Arayüz ile birçok işlem görüntülenebilmesi
    - Notlar, Anımsatıcılar, Ekran süresi istatistikleri, Komut geçmişi
  - Arayüzde buton ile aktifleştirme-pasifleştirme
  - Aktif-Pasif renk geçişleri
