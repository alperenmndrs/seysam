import React from 'react';

const Projects: React.FC = () => {
    const projectList = [
        {
            title: 'Proje 1',
            description: 'Bu proje Seysa Medya tarafından gerçekleştirilen ilk projedir.',
            imageUrl: '/path/to/image1.jpg',
        },
        {
            title: 'Proje 2',
            description: 'Bu proje, dijital pazarlama alanında önemli bir başarıdır.',
            imageUrl: '/path/to/image2.jpg',
        },
        {
            title: 'Proje 3',
            description: 'Bu proje, sosyal medya yönetimi hizmetlerimizi kapsamaktadır.',
            imageUrl: '/path/to/image3.jpg',
        },
    ];

    return (
        <section className="projects">
            <h2>Projelerimiz</h2>
            <div className="project-list">
                {projectList.map((project, index) => (
                    <div key={index} className="project-item">
                        <img src={project.imageUrl} alt={project.title} />
                        <h3>{project.title}</h3>
                        <p>{project.description}</p>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default Projects;