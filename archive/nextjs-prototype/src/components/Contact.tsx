import React from 'react';

const Contact: React.FC = () => {
    return (
        <section id="contact" className="contact-section">
            <div className="container">
                <h2>İletişim</h2>
                <p>Bize ulaşmak için aşağıdaki formu doldurun veya iletişim bilgilerimizi kullanarak bize ulaşın.</p>
                <form>
                    <div className="form-group">
                        <label htmlFor="name">Adınız</label>
                        <input type="text" id="name" name="name" required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">E-posta</label>
                        <input type="email" id="email" name="email" required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="message">Mesajınız</label>
                        <textarea id="message" name="message" required></textarea>
                    </div>
                    <button type="submit">Gönder</button>
                </form>
                <div className="contact-info">
                    <h3>İletişim Bilgilerimiz</h3>
                    <p>Email: info@seysamedya.com</p>
                    <p>Telefon: +90 123 456 7890</p>
                </div>
            </div>
        </section>
    );
};

export default Contact;