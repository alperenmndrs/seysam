import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer style={{ backgroundColor: '#ffffff', color: '#ff7f50', padding: '20px', textAlign: 'center' }}>
            <div>
                <p>&copy; {new Date().getFullYear()} Seysa Medya. Tüm Hakları Saklıdır.</p>
            </div>
            <div>
                <a href="/hizmetler" style={{ margin: '0 10px', color: '#ff7f50' }}>Hizmetler</a>
                <a href="/projeler" style={{ margin: '0 10px', color: '#ff7f50' }}>Projeler</a>
                <a href="/referanslar" style={{ margin: '0 10px', color: '#ff7f50' }}>Referanslar</a>
                <a href="/hakkimizda" style={{ margin: '0 10px', color: '#ff7f50' }}>Hakkımızda</a>
                <a href="/iletisim" style={{ margin: '0 10px', color: '#ff7f50' }}>İletişim</a>
            </div>
        </footer>
    );
};

export default Footer;