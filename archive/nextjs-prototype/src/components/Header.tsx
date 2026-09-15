import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import logo from '../assets/logo.svg';

const Header: React.FC = () => {
    return (
        <header className="bg-white text-orange-600 shadow">
            <div className="container mx-auto flex justify-between items-center p-4">
                <div className="logo">
                    <Image src={logo} alt="Seysa Medya Logo" width={150} height={50} />
                </div>
                <nav className="flex space-x-4">
                    <Link href="/">Ana Sayfa</Link>
                    <Link href="/services">Hizmetler</Link>
                    <Link href="/projects">Projeler</Link>
                    <Link href="/references">Referanslar</Link>
                    <Link href="/packages">Paketler / Teklif Al</Link>
                    <Link href="/about">Hakkımızda</Link>
                    <Link href="/contact">İletişim</Link>
                </nav>
            </div>
        </header>
    );
};

export default Header;