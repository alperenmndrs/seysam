import React from 'react';
import Header from '../components/Header';
import Hero from '../components/Hero';
import Services from '../components/Services';
import Projects from '../components/Projects';
import References from '../components/References';
import Packages from '../components/Packages';
import About from '../components/About';
import Contact from '../components/Contact';
import Footer from '../components/Footer';

const Page = () => {
    return (
        <div>
            <Header />
            <Hero />
            <Services />
            <Projects />
            <References />
            <Packages />
            <About />
            <Contact />
            <Footer />
        </div>
    );
};

export default Page;