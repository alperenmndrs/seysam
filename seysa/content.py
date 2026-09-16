"""Public service catalogue. Every entry has its own canonical URL."""
GROUPS = [
    ('sosyal-medya-yonetimi', 'Sosyal Medya Yönetimi', 'İçerik planlama, tasarım, yayın ve hesap yönetimini birlikte yürütüyoruz.', [
        ('İçerik planı', 'Markanıza uygun içerik başlıklarını ve yayın takvimini hazırlıyoruz.'),
        ('Hesap yönetimi', 'Paylaşımları, gelen etkileşimleri ve hesap düzenini takip ediyoruz.'),
        ('Değerlendirme', 'İçerik performansını raporluyor, sonraki ayın planını oluşturuyoruz.')], [
        ('strateji-icerik-plani', 'Strateji & İçerik Planı', 'Markanızın sosyal medyada neyi, kime ve nasıl anlatacağını planlıyoruz.', ['Hedef kitle ve mevcut hesapların değerlendirilmesi', 'İçerik başlıkları ve iletişim dili', 'Aylık yayın takvimi']),
        ('paylasim-hikaye-tasarimi', 'Paylaşım & Hikâye Tasarımı', 'Akış, hikâye ve kaydırmalı paylaşımlar için markanıza uygun görseller hazırlıyoruz.', ['Markaya uygun tasarım şablonları', 'Paylaşım metinleri ve görsel yerleşimi', 'Platforma uygun dosya teslimi']),
        ('reels-kisa-video', 'Reels & Kısa Video', 'Sosyal kanallarınız için izlenebilir, mesajı net kısa videolar üretiyoruz.', ['İçerik fikri ve kısa senaryo', 'Çekim ihtiyacı ve üretim planı', 'Dikey kurgu, altyazı ve kapak tasarımı']),
        ('hesap-topluluk-yonetimi', 'Hesap & Topluluk Yönetimi', 'Hesaplarınızın günlük düzenini, yayınlarını ve etkileşimlerini takip ediyoruz.', ['Profil ve hesap düzeni', 'İçeriklerin planlanması ve yayınlanması', 'Yorum ve mesajlar için yanıt akışı']),
        ('analiz-raporlama', 'Analiz & Raporlama', 'İçeriklerin sonuçlarını değerlendiriyor, sonraki dönem için somut öneriler hazırlıyoruz.', ['Erişim ve etkileşim değerlendirmesi', 'İçerik türlerine göre performans analizi', 'Dönem raporu ve yeni içerik önerileri'])]),
    ('produksiyon', 'Prodüksiyon', 'Fotoğraf ve video çekiminden kurguya kadar tüm üretim sürecini yönetiyoruz.', [], [
        ('fotograf', 'Fotoğraf Çekimi', 'Ürün, mekân, kurumsal portre ve etkinlik fotoğrafları çekiyoruz.', ['Çekim planı ve hazırlık', 'Stüdyo veya yerinde çekim', 'Seçim, düzenleme ve teslim']),
        ('video', 'Video Çekimi', 'Markanızı, ürününüzü ve hizmetinizi anlatan videolar hazırlıyoruz.', ['Senaryo ve çekim planı', 'Görüntü ve ses kaydı', 'Kurgu ve yayın formatları']),
        ('drone', 'Drone Çekimi', 'Mekân, tesis ve etkinlikler için havadan görüntüler üretiyoruz.', ['Lokasyon ve uçuş planlaması', 'Gerekli izinlerin değerlendirilmesi', 'Havadan çekim ve görüntü teslimi']),
        ('reels-reklam-filmi', 'Reels / Reklam Filmi', 'Sosyal medya ve reklam kampanyaları için kısa, amaca uygun filmler hazırlıyoruz.', ['Fikir ve senaryo', 'Çekim ve prodüksiyon', 'Dikey, yatay ve kısa versiyonlar']),
        ('kurgu-post-produksiyon', 'Kurgu & Post Prodüksiyon', 'Çekilen görüntüleri kurgu, renk ve ses düzenlemeleriyle yayına hazırlıyoruz.', ['Video kurgusu', 'Renk ve ses düzenleme', 'Altyazı, grafik ve çıktı formatları'])]),
    ('marka-tasarim', 'Marka & Tasarım', 'Markanızın görsel kimliğini ve iletişim materyallerini tasarlıyoruz.', [], [
        ('logo', 'Logo Tasarımı', 'Markanızı temsil eden, farklı alanlarda kullanılabilen logolar tasarlıyoruz.', ['Marka ve sektör değerlendirmesi', 'Tasarım önerileri ve revizyon', 'Vektörel dosyalar ve kullanım versiyonları']),
        ('kurumsal-kimlik', 'Kurumsal Kimlik', 'Logo, renk, yazı karakteri ve kurumsal materyalleri tutarlı bir yapıda birleştiriyoruz.', ['Renk ve tipografi', 'Kurumsal materyal tasarımları', 'Kimlik kullanım kılavuzu']),
        ('ambalaj', 'Ambalaj Tasarımı', 'Ürününüzün kullanımına ve baskı gereksinimlerine uygun ambalajlar tasarlıyoruz.', ['Ambalaj yapısı ve içerik yerleşimi', 'Görsel tasarım', 'Baskıya hazırlık']),
        ('sosyal-medya-tasarimi', 'Sosyal Medya Tasarımı', 'Paylaşım, hikâye ve reklamlar için markanıza uygun tasarımlar hazırlıyoruz.', ['İçerik şablonları', 'Kampanya görselleri', 'Platforma uygun boyutlandırma']),
        ('basili-materyaller', 'Basılı Materyaller', 'Katalog, broşür, afiş ve diğer basılı iletişim materyallerini hazırlıyoruz.', ['Sayfa düzeni ve tasarım', 'İçerik yerleşimi', 'Baskıya uygun dosya teslimi'])]),
    ('web-dijital', 'Web & Dijital', 'Web siteleri ve işletmenizin ihtiyaç duyduğu dijital altyapıyı kuruyoruz.', [], [
        ('kurumsal-web-sitesi', 'Kurumsal Web Sitesi', 'Hizmetlerinizi açıkça anlatan, mobil uyumlu kurumsal web siteleri geliştiriyoruz.', ['Sayfa ve içerik planı', 'Tasarım ve geliştirme', 'Yayın ve temel kullanım desteği']),
        ('e-ticaret', 'E-Ticaret', 'Ürünlerinizi internetten satabileceğiniz e-ticaret siteleri kuruyoruz.', ['Ürün ve kategori yapısı', 'Ödeme ve kargo entegrasyonları', 'Sipariş yönetimi ve kullanım desteği']),
        ('landing-page', 'Landing Page', 'Tek bir kampanya, ürün veya hizmet için odaklı açılış sayfaları hazırlıyoruz.', ['Kampanya içeriği', 'Mobil uyumlu tasarım', 'Form ve ölçüm entegrasyonları']),
        ('domain-hosting', 'Domain & Hosting', 'Alan adı, barındırma ve yayın süreçlerinde teknik destek sağlıyoruz.', ['Alan adı ve barındırma seçimi', 'DNS ve SSL kurulumu', 'Yedekleme ve teknik takip']),
        ('kurumsal-e-posta', 'Kurumsal E-Posta', 'Alan adınızla çalışan kurumsal e-posta hesaplarını kuruyoruz.', ['E-posta hizmeti ve hesap kurulumu', 'Alan adı doğrulamaları', 'Cihaz kurulumu ve geçiş desteği'])]),
    ('digital-marketing', 'Digital Marketing', 'Dijital reklam kampanyalarını planlıyor, yönetiyor ve raporluyoruz.', [], [
        ('meta-ads', 'Meta Ads', 'Instagram ve Facebook reklamlarınızı hedeflerinize göre yönetiyoruz.', ['Hedef kitle ve kampanya planı', 'Reklam kurulumu ve takibi', 'Bütçe ve performans değerlendirmesi']),
        ('google-ads', 'Google Ads', 'Google reklamlarıyla ürün ve hizmetlerinizi arayan kişilere ulaşmanıza yardımcı oluyoruz.', ['Anahtar kelime ve kampanya planı', 'Reklam ve dönüşüm kurulumu', 'Düzenli optimizasyon']),
        ('kampanya-yonetimi', 'Kampanya Yönetimi', 'Reklam hedeflerini, bütçeyi ve yayın planını tek bir süreçte yönetiyoruz.', ['Hedef ve bütçe planı', 'Kanal ve içerik koordinasyonu', 'Sonuçların değerlendirilmesi']),
        ('icerik-uretimi', 'İçerik Üretimi', 'Dijital kanallarınız için metin, görsel ve video içerikleri hazırlıyoruz.', ['İçerik başlıkları ve planlama', 'Metin ve görsel üretimi', 'Kanala uygun düzenleme']),
        ('raporlama', 'Raporlama', 'Reklam ve içerik sonuçlarını anlaşılır raporlarla takip etmenizi sağlıyoruz.', ['Ölçüm hedeflerinin belirlenmesi', 'Verilerin düzenlenmesi', 'Sonuçlar ve sonraki adımlar'])]),
    ('brand-setup', 'Brand Setup', 'Yeni markanızın ismini, kimliğini ve dijital başlangıcını birlikte hazırlıyoruz.', [], [
        ('isimlendirme-konumlandirma', 'İsimlendirme & Konumlandırma', 'Markanızın hedef kitlesini, sunduğu değeri ve ismini netleştiriyoruz.', ['Hedef kitle ve rakip incelemesi', 'İsim önerileri', 'Marka konumlandırması']),
        ('gorsel-kimlik', 'Görsel Kimlik', 'Yeni markanız için logo, renk ve temel tasarım dilini oluşturuyoruz.', ['Logo ve görsel yön', 'Renk ve yazı karakterleri', 'Temel kullanım dosyaları']),
        ('dijital-altyapi', 'Dijital Altyapı', 'Markanızın internette ihtiyaç duyacağı temel sistemleri kuruyoruz.', ['Alan adı ve barındırma', 'Web sitesi ve e-posta', 'Ölçüm araçlarının kurulumu']),
        ('hesap-kurulumlari', 'Hesap Kurulumları', 'Sosyal medya ve reklam hesaplarınızı markanıza uygun şekilde düzenliyoruz.', ['Kurumsal hesapların açılması', 'Profil ve erişim düzeni', 'Reklam hesaplarının bağlanması']),
        ('startup-destegi', 'Startup Desteği', 'Yeni girişimlerin marka ve dijital iletişim çalışmalarına destek veriyoruz.', ['İhtiyaçların belirlenmesi', 'Marka ve iletişim planı', 'Lansman hazırlığı'])])
]
SERVICES = {}
for slug, title, description, scope, children in GROUPS:
    path = '/hizmetler/' + slug
    SERVICES[path] = dict(path=path, title=title, description=description, scope=scope, children=[], parent='/hizmetler')
    for child_slug, child_title, child_desc, steps in children:
        child_path = path + '/' + child_slug
        child = dict(path=child_path, title=child_title, description=child_desc, scope=[(s, '') for s in steps], children=[], parent=path)
        SERVICES[child_path] = child
        SERVICES[path]['children'].append(child)
NAV = [('/', 'Ana Sayfa'), ('/hizmetler', 'Hizmetler'), ('/projeler', 'Projeler'), ('/referanslar', 'Referanslar'), ('/paketler', 'Paketler / Teklif Al'), ('/icerik-rehberi', 'İçerik Rehberi'), ('/hakkimizda', 'Hakkımızda'), ('/iletisim', 'İletişim')]
PACKAGES = [
    ('Sosyal Medya', 'Düzenli içerik ve hesap yönetimi.', ['İçerik planlama', 'Görsel tasarım ve yayın', 'Hesap yönetimi ve raporlama']),
    ('Prodüksiyon', 'Çekim ve içerik üretimi.', ['Fotoğraf ve video çekimi', 'Reels ve reklam içerikleri', 'Kurgu ve teslim']),
    ('Marka & Dijital', 'Yeni marka veya yenilenme süreci.', ['Marka kimliği', 'Web sitesi ve dijital altyapı', 'Lansman içerikleri'])
]
