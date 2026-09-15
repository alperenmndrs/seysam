import React from 'react';

const References: React.FC = () => {
    const testimonials = [
        {
            name: "Ahmet Yılmaz",
            feedback: "Seysa Medya ile çalışmak harika bir deneyimdi. Projelerimizi zamanında ve beklediğimizden daha iyi bir şekilde tamamladılar."
        },
        {
            name: "Elif Demir",
            feedback: "Profesyonel bir ekip! Sosyal medya yönetimimizde büyük bir fark yarattılar."
        },
        {
            name: "Mehmet Can",
            feedback: "Marka tasarımımız için Seysa Medya ile çalıştık ve sonuçtan son derece memnun kaldık."
        }
    ];

    return (
        <section className="references">
            <h2>Müşteri Referansları</h2>
            <div className="testimonials">
                {testimonials.map((testimonial, index) => (
                    <div key={index} className="testimonial">
                        <p>"{testimonial.feedback}"</p>
                        <h4>- {testimonial.name}</h4>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default References;