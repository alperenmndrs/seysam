# Seysa Medya

Çok sayfalı şirket sitesi ve giriş korumalı yönetim paneli.

## Çalıştırma

Python 3.9 veya üzeri yeterlidir. Harici paket gerekmez.

```sh
python3 -B server.py
```

- Site: http://127.0.0.1:4173
- Panel: http://127.0.0.1:4173/admin

İlk açılışta panelden kullanıcı adınızı ve en az 12 karakterlik şifrenizi oluşturun. Varsayılan veya sabit şifre yoktur. İlk hesap yalnızca doğrudan bu bilgisayardaki yerel bağlantıdan oluşturulur; kurulumdan sonra tekrar hesap oluşturulamaz. Bu görev sırasında hesabınız sizin oluşturmanız için boş bırakılmıştır.

## Sayfalar

Ana sayfa, Hizmetler, Projeler, Referanslar, Paketler / Teklif Al, Hakkımızda ve İletişim birbirinden ayrı adreslerdedir. Alt gruplar dahil 31 hizmet sayfası vardır. Örneğin:

- `/hizmetler/produksiyon/fotograf`
- `/hizmetler/marka-tasarim/kurumsal-kimlik`
- `/hizmetler/web-dijital/e-ticaret`
- `/hizmetler/digital-marketing/meta-ads`
- `/hizmetler/brand-setup/isimlendirme-konumlandirma`

Hizmet ağacının içeriği `seysa/content.py` dosyasındadır. Bu sürümde panel şirket, proje ve referansları yönetir; sabit hizmet metinleri panelden düzenlenmez.

## Panel kullanımı

1. **Şirketler:** Kurum adını, sektörünü, isteğe bağlı web adresini ve logosunu ekleyin. PNG, JPG, WebP ve SVG desteklenir (en fazla 5 MB).
2. **Projeler:** Proje adını, şirketini, hizmetini, kısa/uzun açıklamasını ve görselini ekleyin. “Sitede yayınla” kapalıyken taslaktır. Yayınlanan proje ana sayfaya, proje listesine ve kendi detay sayfasına yansır.
3. **Referanslar:** Şirketi seçin; logo şirket kaydından alınır. İsteğe bağlı yorum, yorum sahibi ve gösterim sırası ekleyin. Yayınlanan logolar ana sayfada ve referanslarda kayar. Hareket durdurulabilir ve azaltılmış hareket tercihine uyar.
4. **Düzenleme / silme:** Listelerde ilgili işlemi seçin. Silmeden önce ayrı onay sayfası açılır. Şirket silinirse referansı kaldırılır, projeleri korunur ve şirket bağlantısı boşaltılır.
5. **Hesap:** Mevcut şifrenizle şifrenizi değiştirebilirsiniz; tüm oturumlar kapatılır.

Kayıtlar ve oturumlar sunucudaki SQLite veritabanında tutulur. Tarayıcı depolaması kullanılmaz. Paneldeki ekleme/silme sonuçları sayfa yenilendiğinde ve sunucu yeniden başlatıldığında korunur. Görseller `.data/uploads/` klasörüne kaydedilir.

## Örnek logolar ve marka

Gönderilen SVG, `assets/seysa-logo-original.svg` içinde aynen korunmuştur. `assets/seysa-logo.svg` yalnızca boş kenarları daraltılmış web sürümüdür; çizimler ve renkler değiştirilmemiştir. Orijinal SVG'deki MEDYA yazısı Carmen Sans fontuna referans verir; bu font dosyası sağlanmadığından bulunmadığı cihazlarda SVG'nin font yedeği kullanılır. Tüm cihazlarda birebir aynı sonuç için yazısı eğrilere çevrilmiş SVG sağlanabilir.

Kullanıcının isteğiyle ASKON, iki bakanlık, KOSGEB ve Kıyı Emniyeti logoları **örnek yerleşim** olarak eklenmiştir. Müşteri ilişkisi iddiası değildir. Panelde örnek kaydı düzenleyebilir, kaldırabilir veya yayın dışına alabilirsiniz. Kaynak adresleri `assets/references/SOURCES.md` içindedir. `python3 -B seed_samples.py` ilk örnekleri yalnızca bir kez ekler; silinen kayıtları geri getirmez.

## Veri ve yedek

- `.data/seysa.sqlite3`: şirketler, projeler, referanslar, yönetici hesabı ve oturumlar.
- `.data/uploads/`: yüklenen görseller.
- `.data/` web üzerinden sunulmaz ve sürüm kontrolünden dışlanır.
- Sunucuyu durdurduktan sonra `.data/` klasörünün tamamını güvenli bir konuma kopyalayarak yedek alın. Aktif sunucuda yedek almak için SQLite backup API'si kullanılmalıdır; yalnızca `.sqlite3` dosyasını çalışırken kopyalamayın.
- Eski tek sayfalık sürüm `archive/single-page-v1/` altında korunur.

## Güvenlik ve yayın

Şifreler tuzlu PBKDF2-SHA256 ile özetlenir. Oturum kimlikleri veritabanında özetlenerek saklanır; çerez HttpOnly ve SameSite=Strict kullanır. Form işlemlerinde oturum, CSRF ve origin kontrolü yapılır. Giriş denemeleri sınırlandırılır. SVG yüklemelerinde betik ve dış kaynaklar engellenir. Taslak proje görselleri yalnızca yöneticiye sunulur.

Bu sürüm yerelde çalışır; canlı yayın yapılmadı. Dinamik panel nedeniyle `index.html` açmak veya basit statik sunucu kullanmak yeterli değildir. Mevcut sunucu Python `ThreadingHTTPServer` ile yerel önizleme içindir; halka açık üretim için üretim sunucusu/proxy, HTTPS, süreç yönetimi, kalıcı disk ve yedekleme kurulmalıdır. `SITE_ORIGIN` tam site origin'ine ayarlanır; HTTPS origin'inde güvenli çerez açılır. `HOST`, `PORT`, `SEYSA_DATA_DIR` ortam değişkenleri desteklenir. Yönetici kurulumu önce yerelde tamamlanmalıdır.

İletişim formu kullanıcının e-posta uygulamasına aktarılacak taslak üretir. Otomatik e-posta gönderim servisi eklenmedi. Kaynakta bulunan `info@seysamedya.com` korunmuştur.

## Kontroller

```sh
python3 -B -m unittest discover -s tests -v
```

Testler geçici bir veritabanında çalışır; gerçek kayıtları değiştirmez. Sayfa adresleri, yetkilendirme, CSRF, giriş/çıkış, yükleme, taslak/yayın ayrımı, veri kalıcılığı ve ilişkili kayıt silme davranışı kontrol edilir.
