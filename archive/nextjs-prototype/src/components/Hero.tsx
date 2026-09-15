import React from 'react';

const Hero: React.FC = () => {
    return (
        <section className="hero">
            <div className="hero-content">
                <h1>Hoş Geldiniz Seysa Medya</h1>
                <p>Yaratıcı çözümlerle markanızı güçlendirin.</p>
                <a href="#services" className="cta-button">Hizmetlerimizi Keşfedin</a>
            </div>
        </section>
    );
};

export default Hero;