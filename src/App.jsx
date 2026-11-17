import React, { useState, useEffect } from 'react';
import {
  Bot,
  Smartphone,
  Globe,
  Terminal,
  Cpu,
  Mail,
  Phone,
  Award,
  ExternalLink,
  Sun,
  Moon,
  Languages,
  GraduationCap,
  MapPin,
  Sparkles,
  FolderGit2,
} from 'lucide-react';
import { profileInfo, translations } from './data/portfolioData';

function TickerStrip({ items, reverse = false }) {
  const repeated = [...items, ...items, ...items, ...items];
  return (
    <div className={`ticker-strip ${reverse ? 'reverse-strip' : ''}`}>
      <div className={`ticker-track ${reverse ? 'reverse' : ''}`}>
        {repeated.map((text, idx) => (
          <span className="ticker-item" key={idx}>
            <span>{text}</span>
            <span className="ticker-sep" />
          </span>
        ))}
      </div>
    </div>
  );
}

function SectionKineticBg({ words }) {
  const row1 = [...words, ...words, ...words, ...words];
  const row2 = [...words].reverse();
  const repeatedRow2 = [...row2, ...row2, ...row2, ...row2];

  return (
    <div className="bg-kinetic-layer" aria-hidden="true">
      <div className="bg-kinetic-row left">
        {row1.map((w, i) => (
          <span className="bg-kinetic-word" key={`r1-${i}`}>
            {w}
          </span>
        ))}
      </div>
      <div className="bg-kinetic-row right">
        {repeatedRow2.map((w, i) => (
          <span className="bg-kinetic-word" key={`r2-${i}`}>
            {w}
          </span>
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [lang, setLang] = useState('id');
  const [theme, setTheme] = useState('dark');
  const [scrollPct, setScrollPct] = useState(38);

  const t = translations[lang];

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight =
        document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (docHeight <= 0) {
        setScrollPct(38);
      } else {
        const pct = Math.min(100, Math.max(8, Math.round((scrollTop / docHeight) * 100)));
        setScrollPct(pct);
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleLang = () => {
    setLang((prev) => (prev === 'en' ? 'id' : 'en'));
  };

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const renderServiceIcon = (iconName) => {
    switch (iconName) {
      case 'bot':
        return <Bot size={26} strokeWidth={2.4} />;
      case 'smartphone':
        return <Smartphone size={26} strokeWidth={2.4} />;
      case 'globe':
        return <Globe size={26} strokeWidth={2.4} />;
      case 'terminal':
        return <Terminal size={26} strokeWidth={2.4} />;
      case 'cpu':
      default:
        return <Cpu size={26} strokeWidth={2.4} />;
    }
  };

  const contactLine1 = [...t.contact.marqueeRow1, ...t.contact.marqueeRow1, ...t.contact.marqueeRow1];
  const contactLine2 = [...t.contact.marqueeRow2, ...t.contact.marqueeRow2, ...t.contact.marqueeRow2];
  const contactLine3 = [...t.contact.marqueeRow3, ...t.contact.marqueeRow3, ...t.contact.marqueeRow3];

  return (
    <div className="app-shell">
      {/* Top Progress Bar (matches reference screenshot top bar) */}
      <div className="top-progress-shell" aria-hidden="true">
        <div className="top-progress-track">
          <div className="top-progress-fill" style={{ width: `${scrollPct}%` }} />
        </div>
      </div>

      {/* Sticky ZZZ HUD Navbar */}
      <header className="zzz-navbar">
        <div className="zzz-navbar-inner">
          <a href="#top" className="brand-badge">
            <span className="brand-pill">RK // AI</span>
            <span>REYNARD KAMADJAJA</span>
          </a>

          <nav className="nav-links" aria-label="Primary Navigation">
            <a href="#about" className="nav-link">
              {t.nav.about}
            </a>
            <a href="#services" className="nav-link">
              {t.nav.services}
            </a>
            <a href="#skills" className="nav-link">
              {t.nav.skills}
            </a>
            <a href="#projects" className="nav-link">
              {t.nav.projects}
            </a>
            <a href="#credentials" className="nav-link">
              {t.nav.credentials}
            </a>
            <a href="#contact" className="nav-link">
              {t.nav.contact}
            </a>
          </nav>

          <div className="nav-controls">
            <button
              type="button"
              onClick={toggleLang}
              className="control-btn lang-btn"
              title="Switch Language (English / Bahasa Indonesia)"
              aria-label="Switch Language"
            >
              <Languages size={16} />
              <span>{lang === 'en' ? 'EN ▸ ID' : 'ID ▸ EN'}</span>
            </button>

            <button
              type="button"
              onClick={toggleTheme}
              className="control-btn"
              title="Toggle Dark / Light Mode"
              aria-label="Toggle Dark or Light Mode"
            >
              {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
              <span>{theme === 'dark' ? 'LIGHT' : 'DARK'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* HERO SECTION — Split Card like Reference Image */}
      <main id="top">
        <section className="hero-section">
          <div className="section-container">
            <div className="status-pill-bar">
              <span className="status-dot" />
              <span>{t.statusBadge}</span>
            </div>

            <div className="hero-dossier-card">
              {/* Left Column: Portrait Photo */}
              <div className="hero-photo-column">
                <img
                  src={profileInfo.photoUrl}
                  alt={profileInfo.fullName}
                  className="hero-photo-img"
                />
              </div>

              {/* Right Column: Green & Light Blue ZZZ Dossier Block */}
              <div className="hero-info-column">
                <div>
                  <div className="hero-agent-tag">{t.hero.agentTag}</div>
                  <h1 className="hero-name-title">{profileInfo.fullName}</h1>

                  <div className="hero-role-chips">
                    <span className="hero-chip">{t.hero.roleBadge}</span>
                    <span className="hero-chip blue-chip">{t.hero.degreeBadge}</span>
                  </div>

                  <p className="hero-headline">{t.hero.headline}</p>
                  <p className="hero-subheadline">{t.hero.subheadline}</p>
                </div>

                <div>
                  <div className="hero-stats-grid">
                    {t.hero.stats.map((st, idx) => (
                      <div className="hero-stat-box" key={idx}>
                        <span className="hero-stat-label">{st.label}</span>
                        <span className="hero-stat-value">{st.value}</span>
                      </div>
                    ))}
                  </div>

                  <div className="hero-cta-row">
                    <a href="#projects" className="zzz-btn primary">
                      <FolderGit2 size={17} />
                      <span>{t.hero.ctaProjects}</span>
                    </a>
                    <a
                      href={profileInfo.cvUrl}
                      download="CV_Reynard_Kamadjaja.pdf"
                      className="zzz-btn secondary"
                    >
                      <Sparkles size={17} />
                      <span>{t.hero.ctaDownloadCv}</span>
                    </a>
                    <a href="#contact" className="zzz-btn secondary">
                      <Mail size={17} />
                      <span>{t.hero.ctaContact}</span>
                    </a>
                    <a
                      href={profileInfo.credlyUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="zzz-btn credly"
                    >
                      <Award size={17} />
                      <span>{t.hero.ctaCredly}</span>
                      <ExternalLink size={14} />
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ZZZ Kinetic Ticker Tape 1 (Left & Right) */}
        <TickerStrip items={t.hero.marqueeTop} />
        <TickerStrip items={t.hero.marqueeBottom} reverse />

        {/* 01. ABOUT ME SECTION */}
        <section id="about" className="section-wrapper">
          <SectionKineticBg words={t.about.marqueeBg} />
          <div className="section-container">
            <div className="section-header">
              <span className="section-tag">{t.about.tag}</span>
              <h2 className="section-title">{t.about.title}</h2>
            </div>

            <div className="about-card">
              <p className="about-summary-text">{t.about.summary}</p>
            </div>

            <div className="about-highlights-grid">
              {t.about.highlights.map((hl) => (
                <div className="highlight-box" key={hl.code}>
                  <span className="highlight-code">{hl.code}</span>
                  <h3 className="highlight-title">{hl.label}</h3>
                  <p className="highlight-desc">{hl.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 02. SERVICES / WHAT I CAN DO */}
        <section id="services" className="section-wrapper">
          <SectionKineticBg words={t.services.marqueeBg} />
          <div className="section-container">
            <div className="section-header">
              <span className="section-tag">{t.services.tag}</span>
              <h2 className="section-title">{t.services.title}</h2>
              <p className="section-subtitle">{t.services.subtitle}</p>
            </div>

            <div className="services-grid">
              {t.services.items.map((srv) => (
                <article className="service-card" key={srv.id}>
                  <div className="service-card-top">
                    <div className={`service-icon-box ${srv.accent}`}>
                      {renderServiceIcon(srv.icon)}
                    </div>
                    <span className="service-id">{srv.id}</span>
                  </div>
                  <h3 className="service-title">{srv.title}</h3>
                  <ul className="service-list">
                    {srv.points.map((pt, i) => (
                      <li key={i}>{pt}</li>
                    ))}
                  </ul>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* 03. TECHNICAL SKILLS & TECH STACK */}
        <section id="skills" className="section-wrapper">
          <SectionKineticBg words={t.skills.marqueeBg} />
          <div className="section-container">
            <div className="section-header">
              <span className="section-tag">{t.skills.tag}</span>
              <h2 className="section-title">{t.skills.title}</h2>
              <p className="section-subtitle">{t.skills.subtitle}</p>
            </div>

            <div className="skills-grid">
              {t.skills.categories.map((cat) => (
                <div className="skill-category-card" key={cat.code}>
                  <div className={`skill-cat-header ${cat.accent}`}>
                    <span className="skill-cat-title">{cat.name}</span>
                    <span className="skill-cat-code">{cat.code}</span>
                  </div>
                  <div className="skill-tags-wrap">
                    {cat.skills.map((sk) => (
                      <span className="skill-pill" key={sk}>
                        {sk}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ZZZ Kinetic Ticker Tape Divider */}
        <TickerStrip items={t.projects.marqueeBg} />

        {/* 04. FEATURED PROJECTS */}
        <section id="projects" className="section-wrapper">
          <SectionKineticBg words={t.projects.marqueeBg} />
          <div className="section-container">
            <div className="section-header">
              <span className="section-tag">{t.projects.tag}</span>
              <h2 className="section-title">{t.projects.title}</h2>
              <p className="section-subtitle">{t.projects.subtitle}</p>
            </div>

            <div className="projects-stack">
              {t.projects.items.map((proj) => (
                <article className="project-card" key={proj.id}>
                  <div className={`project-side-banner ${proj.accent}`}>
                    <div>
                      <div className="project-id-giant">{proj.id}</div>
                      <span className="project-type-badge">{proj.badge}</span>
                    </div>
                    <div className="project-role-box">{proj.role}</div>
                  </div>

                  <div className="project-main-body">
                    <div>
                      <h3 className="project-title">{proj.title}</h3>
                      <p className="project-desc">{proj.description}</p>
                    </div>

                    <div>
                      <span className="project-features-label">
                        {t.projects.keyFeaturesLabel}
                      </span>
                      <ul className="project-features-list">
                        {proj.features.map((feat, i) => (
                          <li key={i}>{feat}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="project-footer-row">
                      <div>
                        <span className="project-tech-label">{t.projects.techStackLabel}</span>
                        <div className="project-tech-chips">
                          {proj.techStack.map((tech) => (
                            <span className="project-tech-chip" key={tech}>
                              {tech}
                            </span>
                          ))}
                        </div>
                      </div>

                      {proj.liveUrl && (
                        <div style={{ marginTop: '16px' }}>
                          <a
                            href={proj.liveUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="zzz-btn credly"
                          >
                            <Globe size={16} />
                            <span>{t.projects.liveSiteBtn}</span>
                            <ExternalLink size={14} />
                          </a>
                        </div>
                      )}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* 05. EDUCATION, CERTIFICATIONS & CREDLY */}
        <section id="credentials" className="section-wrapper">
          <SectionKineticBg words={t.education.marqueeBg} />
          <div className="section-container">
            <div className="section-header">
              <span className="section-tag">{t.education.tag}</span>
              <h2 className="section-title">{t.education.title}</h2>
            </div>

            <div className="edu-credly-grid">
              {/* University Education Card */}
              <div className="edu-card">
                <span className="edu-badge">
                  <GraduationCap
                    size={15}
                    style={{ verticalAlign: 'middle', marginRight: '6px' }}
                  />
                  {t.education.eduCard.badge}
                </span>
                <h3 className="edu-degree">{t.education.eduCard.degree}</h3>
                <p className="edu-inst">{t.education.eduCard.institution}</p>
                <div className="edu-meta-row">
                  <span className="edu-meta-pill">
                    <MapPin size={14} style={{ verticalAlign: 'middle', marginRight: '4px' }} />
                    {t.education.eduCard.location}
                  </span>
                  <span className="edu-meta-pill">{t.education.eduCard.graduation}</span>
                  <span className="edu-meta-pill">{t.education.eduCard.details}</span>
                </div>
              </div>

              {/* Official Credly Profile Card */}
              <div className="credly-spotlight-card">
                <div>
                  <span className="credly-badge-tag">
                    <Sparkles size={14} />
                    <span>{t.education.credlyBanner.badge}</span>
                  </span>
                  <h3 className="credly-title" style={{ marginTop: '10px' }}>
                    {t.education.credlyBanner.title}
                  </h3>
                  <p className="credly-desc" style={{ marginTop: '6px' }}>
                    {t.education.credlyBanner.description}
                  </p>
                </div>

                <div>
                  <a
                    href={profileInfo.credlyUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="zzz-btn primary"
                  >
                    <Award size={18} />
                    <span>{t.education.credlyBanner.buttonText}</span>
                    <ExternalLink size={15} />
                  </a>
                </div>
              </div>
            </div>

            <div className="certs-grid">
              {t.education.certifications.map((cert) => (
                <div className="cert-card" key={cert.code}>
                  <span className="cert-issuer">
                    {cert.code} // {cert.issuer}
                  </span>
                  <h4 className="cert-title">{cert.title}</h4>
                  <p className="cert-detail">{cert.detail}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 06. CONTACT SECTION — Matches Reference Image Bottom Block with ZZZ Moving Text */}
        <section id="contact" className="contact-zzz-section">
          {/* Giant Outlined Text Moving Left & Right in Background */}
          <div className="contact-marquee-backdrop" aria-hidden="true">
            <div className="contact-marquee-line move-left">
              {contactLine1.map((word, idx) => (
                <span className="contact-marquee-item" key={`c1-${idx}`}>
                  {word}
                </span>
              ))}
            </div>
            <div className="contact-marquee-line move-right">
              {contactLine2.map((word, idx) => (
                <span className="contact-marquee-item" key={`c2-${idx}`}>
                  {word}
                </span>
              ))}
            </div>
            <div className="contact-marquee-line move-left">
              {contactLine3.map((word, idx) => (
                <span className="contact-marquee-item" key={`c3-${idx}`}>
                  {word}
                </span>
              ))}
            </div>
          </div>

          <div className="contact-inner">
            <span className="contact-mono-tag">{t.contact.tag}</span>
            <h2 className="contact-giant-heading">{t.contact.title}</h2>
            <p className="contact-subtitle">{t.contact.subtitle}</p>

            <div className="contact-cards-grid">
              {/* Email Card */}
              <a href={`mailto:${profileInfo.email}`} className="contact-brutal-card">
                <div className="contact-icon-square">
                  <Mail size={24} />
                </div>
                <div className="contact-card-details">
                  <span className="contact-card-label">{t.contact.emailLabel}</span>
                  <span className="contact-card-value">{profileInfo.email}</span>
                </div>
              </a>

              {/* Phone / WhatsApp Card */}
              <a
                href={profileInfo.whatsappUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="contact-brutal-card"
              >
                <div className="contact-icon-square">
                  <Phone size={24} />
                </div>
                <div className="contact-card-details">
                  <span className="contact-card-label">{t.contact.phoneLabel}</span>
                  <span className="contact-card-value">{profileInfo.phoneDisplay}</span>
                </div>
              </a>

              {/* Credly Official Link Card */}
              <a
                href={profileInfo.credlyUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="contact-brutal-card"
              >
                <div className="contact-icon-square">
                  <Award size={24} />
                </div>
                <div className="contact-card-details">
                  <span className="contact-card-label">{t.contact.credlyLabel}</span>
                  <span className="contact-card-value">credly.com/users/rey-kamadjaya</span>
                </div>
              </a>
            </div>
          </div>
        </section>
      </main>

      {/* Footer (matches reference screenshot footer) */}
      <footer className="zzz-footer">
        <p>
          © 2026 <strong>{profileInfo.shortName}</strong> ({profileInfo.fullName},{' '}
          {profileInfo.degreeShort}). &nbsp;// {t.contact.footerNote}{' '}
          <span className="heart">♥</span>
        </p>
      </footer>
    </div>
  );
}
