import React from 'react';

const Packages = () => {
    return (
        <section className="packages">
            <h2>Hizmet Paketlerimiz</h2>
            <div className="package-list">
                <div className="package-item">
                    <h3>Paket 1</h3>
                    <p>Açıklama: Bu paket, temel sosyal medya yönetimi hizmetlerini içerir.</p>
                </div>
                <div className="package-item">
                    <h3>Paket 2</h3>
                    <p>Açıklama: Bu paket, prodüksiyon hizmetleri ile birlikte sosyal medya yönetimini içerir.</p>
                </div>
                <div className="package-item">
                    <h3>Paket 3</h3>
                    <p>Açıklama: Bu paket, marka tasarımı ve dijital pazarlama hizmetlerini kapsar.</p>
                </div>
                <div className="package-item">
                    <h3>Paket 4</h3>
                    <p>Açıklama: Bu paket, tüm hizmetleri bir arada sunar ve kapsamlı bir çözüm sağlar.</p>
                </div>
            </div>
        </section>
    );
};

export default Packages;