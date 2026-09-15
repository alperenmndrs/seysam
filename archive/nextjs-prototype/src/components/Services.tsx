import React from 'react';

const servicesData = [
    {
        title: 'Sosyal Medya Yönetimi',
        description: 'Sosyal medya hesaplarınızın yönetimi ve içerik planlaması.'
    },
    {
        title: 'Prodüksiyon',
        subServices: [
            { title: 'Fotoğraf Çekimi', description: 'Profesyonel fotoğraf çekimi hizmetleri.' },
            { title: 'Video Çekimi', description: 'Kurumsal ve tanıtım videoları çekimi.' },
            { title: 'Drone Çekimi', description: 'Havadan görüntüleme hizmetleri.' },
            { title: 'Reels / Reklam Filmi', description: 'Kısa tanıtım videoları ve reklam filmleri.' },
            { title: 'Kurgu & Post Prodüksiyon', description: 'Video düzenleme ve post prodüksiyon hizmetleri.' }
        ]
    },
    {
        title: 'Marka & Tasarım',
        subServices: [
            { title: 'Logo Tasarımı', description: 'Özgün logo tasarım hizmetleri.' },
            { title: 'Kurumsal Kimlik', description: 'Marka kimliğinizi oluşturan tasarımlar.' },
            { title: 'Ambalaj Tasarımı', description: 'Ürünleriniz için etkileyici ambalaj tasarımları.' },
            { title: 'Sosyal Medya Tasarımları', description: 'Sosyal medya paylaşımlarınız için grafik tasarımlar.' },
            { title: 'Basılı Materyaller', description: 'Kartvizit, broşür gibi basılı materyal tasarımları.' }
        ]
    },
    {
        title: 'Web & Dijital',
        subServices: [
            { title: 'Kurumsal Web Sitesi', description: 'Kurumsal ihtiyaçlarınıza uygun web siteleri.' },
            { title: 'E-Ticaret Sitesi', description: 'Online satış için e-ticaret çözümleri.' },
            { title: 'Landing Page', description: 'Hedef odaklı açılış sayfaları.' },
            { title: 'Domain & Hosting', description: 'Alan adı ve hosting hizmetleri.' },
            { title: 'Kurumsal E-Posta', description: 'Kurumsal e-posta çözümleri.' },
            { title: 'Teknik Bakım / Destek', description: 'Web siteniz için teknik destek hizmetleri.' }
        ]
    },
    {
        title: 'Dijital Pazarlama',
        subServices: [
            { title: 'Meta Reklamları', description: 'Facebook ve Instagram reklam yönetimi.' },
            { title: 'Google Ads', description: 'Google reklam kampanyaları yönetimi.' },
            { title: 'Kampanya Yönetimi', description: 'Rekabetçi kampanya yönetimi hizmetleri.' },
            { title: 'İçerik Planlaması', description: 'Düzenli içerik planlaması ve takibi.' },
            { title: 'Raporlama & Analiz', description: 'Kampanya performans raporları ve analizleri.' }
        ]
    },
    {
        title: 'Marka Kurulum Hizmetleri',
        subServices: [
            { title: 'Marka İsmi / Konumlandırma', description: 'Marka ismi ve konumlandırma stratejileri.' },
            { title: 'Görsel Kimlik', description: 'Marka görsel kimliğinin oluşturulması.' },
            { title: 'Dijital Altyapı Kurulumu', description: 'Dijital altyapı kurulumu ve entegrasyonu.' },
            { title: 'Sosyal Medya Hesaplarının Kurulumu', description: 'Sosyal medya hesaplarınızın kurulumu.' },
            { title: 'Şirket Kurulum Sürecine Destek', description: 'Şirket kurulum süreçlerinde rehberlik.' }
        ]
    }
];

const Services = () => {
    return (
        <section className="services">
            <h2>Hizmetlerimiz</h2>
            <div className="services-list">
                {servicesData.map((service, index) => (
                    <div key={index} className="service-item">
                        <h3>{service.title}</h3>
                        {service.description && <p>{service.description}</p>}
                        {service.subServices && (
                            <ul>
                                {service.subServices.map((subService, subIndex) => (
                                    <li key={subIndex}>
                                        <strong>{subService.title}:</strong> {subService.description}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                ))}
            </div>
        </section>
    );
};

export default Services;