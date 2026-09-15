import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import '../app/globals.css';

const Layout = ({ children }) => {
    return (
        <div className="layout">
            <Header />
            <main>{children}</main>
            <Footer />
        </div>
    );
};

export default Layout;