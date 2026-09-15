/* =========================================================
   INIT — GSAP PLUGINS
========================================================= */
gsap.registerPlugin(ScrollTrigger);

/* =========================================================
   LENIS SMOOTH SCROLL + GSAP TICKER SYNC (NO JITTER)
========================================================= */
const lenis = new Lenis({
  duration: 1.15,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
  wheelMultiplier: 1,
  touchMultiplier: 1.5,
  infinite: false,
});

lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});

gsap.ticker.lagSmoothing(0);

/* =========================================================
   REC TIMECODE COUNTER
========================================================= */
(function initTimecode() {
  const tcEl = document.getElementById('timecodeValue');
  if (!tcEl) return;

  let ff = 2, ss = 18, mm = 24, hh = 0;

  function pad(n) {
    return n.toString().padStart(2, '0');
  }

  function tick() {
    ff += 1;
    if (ff >= 24) {
      ff = 0;
      ss += 1;
      if (ss >= 60) {
        ss = 0;
        mm += 1;
        if (mm >= 60) {
          mm = 0;
          hh += 1;
        }
      }
    }
    tcEl.textContent = `${pad(hh)}:${pad(mm)}:${pad(ss)}:${pad(ff)}`;
  }

  setInterval(tick, 1000 / 24);
})();

/* =========================================================
   MAGNETIC BUTTON
========================================================= */
(function initMagneticButton() {
  const btn = document.querySelector('[data-magnetic]');
  if (!btn) return;

  const strength = 0.4;

  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const relX = e.clientX - rect.left - rect.width / 2;
    const relY = e.clientY - rect.top - rect.height / 2;

    gsap.to(btn, {
      x: relX * strength,
      y: relY * strength,
      duration: 0.5,
      ease: 'power3.out',
    });
  });

  btn.addEventListener('mouseleave', () => {
    gsap.to(btn, {
      x: 0,
      y: 0,
      duration: 0.6,
      ease: 'elastic.out(1, 0.4)',
    });
  });
})();

/* =========================================================
   SPLIT TEXT — HERO TITLE
========================================================= */
let heroSplit;

function setupHeroSplit() {
  if (typeof SplitType !== 'undefined') {
    heroSplit = new SplitType('.hero-title', {
      types: 'lines,words',
      lineClass: 'hero-line',
    });
  }
}

/* =========================================================
   MAIN SCROLLYTELLING TIMELINE — PORTAL DOORS
========================================================= */
function initPortalTimeline() {
  setupHeroSplit();

  const portalSection = document.querySelector('.portal-section');
  const doorLeft = document.getElementById('doorLeft');
  const doorRight = document.getElementById('doorRight');
  const lightLeak = document.getElementById('lightLeak');
  const lightLeakRadial = document.querySelector('.light-leak__radial');
  const lightLeakBeam = document.querySelector('.light-leak__beam');
  const portalHeadline = document.getElementById('portalHeadline');
  const showreelVideo = document.getElementById('showreelVideo');
  const showreelLayer = document.querySelector('.showreel-layer');
  const scrollCue = document.querySelector('.scroll-cue');

  if (showreelVideo) {
    showreelVideo.play().catch(() => {});
  }

  if (!portalSection || !doorLeft || !doorRight) return;

  const master = gsap.timeline({
    scrollTrigger: {
      trigger: portalSection,
      start: 'top top',
      end: '+=3800',
      scrub: 1,
      pin: true,
      anticipatePin: 1,
      invalidateOnRefresh: true,
    },
  });

  /* Fade out scroll cue almost immediately */
  if (scrollCue) {
    master.to(scrollCue, {
      opacity: 0,
      duration: 0.3,
    }, 0);
  }

  /* ---------- ADIM 1: Başlık yukarı süzülüp solarak çıkar ---------- */
  master.to('.hero-line', {
    yPercent: -140,
    opacity: 0,
    stagger: 0.08,
    ease: 'power2.in',
    duration: 1.2,
  }, 0.1);

  master.to('.hero-subtitle', {
    y: -40,
    opacity: 0,
    duration: 1,
    ease: 'power2.in',
  }, 0.1);

  /* ---------- ADIM 2: Light leak maksimuma ulaşır ---------- */
  if (lightLeak) {
    master.to(lightLeak, {
      opacity: 1,
      duration: 1.2,
      ease: 'power1.inOut',
    }, 0.6);
  }

  if (lightLeakRadial) {
    master.to(lightLeakRadial, {
      scale: 2.6,
      duration: 1.8,
      ease: 'power2.inOut',
    }, 0.6);
  }

  if (lightLeakBeam) {
    master.to(lightLeakBeam, {
      scaleX: 40,
      opacity: 0.9,
      duration: 1.6,
      ease: 'power2.inOut',
    }, 0.7);
  }

  /* ---------- ADIM 3: Kapılar 3D olarak sonuna kadar açılır ---------- */
  master.to(doorLeft, {
    rotateY: -115,
    xPercent: -40,
    duration: 2.4,
    ease: 'power2.inOut',
  }, 1.4);

  master.to(doorRight, {
    rotateY: 115,
    xPercent: 40,
    duration: 2.4,
    ease: 'power2.inOut',
  }, 1.4);

  /* Door depth push for realism as they swing */
  master.to([doorLeft, doorRight], {
    z: -260,
    duration: 2.4,
    ease: 'power2.inOut',
  }, 1.4);

  /* Light leak recedes as the doors fully open and video takes over */
  if (lightLeak) {
    master.to(lightLeak, {
      opacity: 0,
      duration: 1,
      ease: 'power1.in',
    }, 3.2);
  }

  /* ---------- ADIM 4: Showreel videosu kameraya doğru büyür ---------- */
  if (showreelVideo) {
    master.to(showreelVideo, {
      scale: 3,
      filter: 'saturate(1.2) contrast(1.05) brightness(1)',
      duration: 3,
      ease: 'power2.inOut',
    }, 1.6);
  }

  master.to('.showreel-tint', {
    opacity: 0,
    duration: 2,
    ease: 'power1.inOut',
  }, 2.2);

  /* Push doors fully off-screen so the viewer feels "inside" the video */
  master.to(doorLeft, {
    xPercent: -160,
    duration: 1.4,
    ease: 'power3.in',
  }, 3.0);

  master.to(doorRight, {
    xPercent: 160,
    duration: 1.4,
    ease: 'power3.in',
  }, 3.0);

  /* ---------- ADIM 5: Sahne içerik akışına pürüzsüzce devredilir ---------- */
  if (showreelLayer) {
    master.to(showreelLayer, {
      opacity: 1,
      duration: 0.6,
    }, 3.6);
  }

  if (portalHeadline) {
    master.to(portalHeadline, {
      opacity: 0,
      duration: 0.4,
    }, 1.5);
  }
}

/* =========================================================
   CONTENT SCROLLTRIGGERS — FADE UP REVEALS
========================================================= */
function initContentReveals() {
  gsap.utils.toArray('.fade-up-text').forEach((el) => {
    gsap.fromTo(
      el,
      { y: 60, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 1.1,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 82%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  gsap.utils.toArray('.fade-up-card').forEach((el, i) => {
    gsap.fromTo(
      el,
      { y: 70, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 1,
        delay: i * 0.12,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  gsap.utils.toArray('.fade-up-row').forEach((el, i) => {
    gsap.fromTo(
      el,
      { y: 40, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.9,
        delay: i * 0.08,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 90%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });
}

/* =========================================================
   WORK CARD VIDEO HOVER PLAY
========================================================= */
function initWorkCardVideos() {
  document.querySelectorAll('.work-card').forEach((card) => {
    const video = card.querySelector('.work-card__video');
    if (!video) return;

    card.addEventListener('mouseenter', () => {
      video.play().catch(() => {});
    });

    card.addEventListener('mouseleave', () => {
      video.pause();
      video.currentTime = 0;
    });
  });
}

/* =========================================================
   BOOTSTRAP
========================================================= */
window.addEventListener('DOMContentLoaded', () => {
  initPortalTimeline();
  initContentReveals();
  initWorkCardVideos();

  ScrollTrigger.refresh();
});

window.addEventListener('load', () => {
  ScrollTrigger.refresh();
});
