/* Page behaviour: navbar, typing roles, scroll reveal, scroll-spy, cursor glow. */
(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- Navbar background once the page is scrolled ----
  const nav = document.querySelector('.site-nav');
  const onScroll = () => nav && nav.classList.toggle('scrolled', window.scrollY > 40);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Close the mobile menu after choosing a link
  document.querySelectorAll('#navMenu a').forEach((link) => {
    link.addEventListener('click', () => {
      const menu = document.getElementById('navMenu');
      if (menu && menu.classList.contains('show') && window.bootstrap) {
        window.bootstrap.Collapse.getOrCreateInstance(menu).hide();
      }
    });
  });

  // ---- Typing effect for the role line ----
  const typed = document.getElementById('typed');
  const rolesEl = document.getElementById('roles-data');
  if (typed && rolesEl && !reduceMotion) {
    let roles = [];
    try { roles = JSON.parse(rolesEl.textContent); } catch (e) { /* keep static text */ }
    if (roles.length > 1) {
      let r = 0, c = roles[0].length, deleting = true;
      const tick = () => {
        const word = roles[r];
        typed.textContent = word.slice(0, c);
        if (deleting) {
          c -= 1;
          if (c < 0) { deleting = false; r = (r + 1) % roles.length; c = 0; }
          return setTimeout(tick, 45);
        }
        c += 1;
        if (c > word.length) { deleting = true; c = word.length; return setTimeout(tick, 1600); }
        setTimeout(tick, 85);
      };
      setTimeout(tick, 1800);
    }
  }

  // ---- Scroll reveal (staggered within each group) ----
  const revealEls = Array.from(document.querySelectorAll('.reveal'));
  revealEls.forEach((el) => {
    const siblings = Array.from(el.parentElement.children).filter((n) => n.classList.contains('reveal'));
    el.style.setProperty('--d', `${Math.min(siblings.indexOf(el), 6) * 70}ms`);
    el.querySelectorAll('.chips li').forEach((li, i) => li.style.setProperty('--i', i));
  });
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add('is-in'); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-in'));
  }

  // ---- Highlight the nav link of the section in view ----
  const links = new Map();
  document.querySelectorAll('#navMenu .nav-link').forEach((a) => links.set(a.getAttribute('href').slice(1), a));
  const sections = Array.from(links.keys()).map((id) => document.getElementById(id)).filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((a) => a.classList.remove('active'));
        const active = links.get(entry.target.id);
        if (active) active.classList.add('active');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach((s) => spy.observe(s));
  }

  // ---- Soft glow that follows the mouse (desktop only) ----
  const glow = document.querySelector('.cursor-glow');
  if (glow && !reduceMotion && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    let x = 0, y = 0, tx = 0, ty = 0, running = false;
    const loop = () => {
      x += (tx - x) * 0.12; y += (ty - y) * 0.12;
      glow.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      if (Math.abs(tx - x) > 0.5 || Math.abs(ty - y) > 0.5) requestAnimationFrame(loop); else running = false;
    };
    window.addEventListener('mousemove', (e) => {
      tx = e.clientX; ty = e.clientY; glow.classList.add('on');
      if (!running) { running = true; requestAnimationFrame(loop); }
    }, { passive: true });
    document.addEventListener('mouseleave', () => glow.classList.remove('on'));
  }

  // ---- Gallery console: types commands, then streams the project list ----
  const consoleBody = document.getElementById('console-body');
  const consoleDataEl = document.getElementById('console-data');
  if (consoleBody && consoleDataEl) {
    let data = { count: 0, titles: [], hosts: [] };
    try { data = JSON.parse(consoleDataEl.textContent); } catch (e) { /* keep defaults */ }
    const box = consoleBody.closest('.console');
    let visible = false;

    const el = (cls, text) => {
      const node = document.createElement('span');
      if (cls) node.className = cls;
      if (text !== undefined) node.textContent = text;
      return node;
    };
    const cursor = el('c-cursor');
    const prompt = document.createElement('div');
    prompt.className = 'c-line';
    prompt.append(el('c-prompt', '$'), cursor);
    consoleBody.appendChild(prompt);

    const addLine = (...parts) => {
      const line = document.createElement('div');
      line.className = 'c-line';
      line.append(...parts);
      consoleBody.insertBefore(line, prompt);
      while (consoleBody.children.length > 40) consoleBody.removeChild(consoleBody.firstChild);
      return line;
    };
    const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    const pace = async (ms) => {          // wait, and stay paused while offscreen or in a hidden tab
      await sleep(ms);
      while (!visible || document.hidden) await sleep(250);
    };

    const commands = [
      { cmd: 'cd ~/portfolio/projects', out: null },
      { cmd: 'ls | wc -l', out: String(data.count) },
    ];
    if (data.hosts.length) commands.push({ cmd: './deploy --hosts', out: data.hosts.join('  ·  ') });
    commands.push({ cmd: 'tail -f gallery.log', out: null });

    const typeCommand = async (text) => {
      const typed = el('c-cmd');
      const line = addLine(el('c-prompt', '$'), typed);
      line.appendChild(cursor);
      prompt.style.visibility = 'hidden';
      for (const ch of text) { typed.textContent += ch; await pace(reduceMotion ? 0 : 38); }
      cursor.remove();
      prompt.appendChild(cursor);
      prompt.style.visibility = '';
    };

    const streamLine = (title) => addLine(el('c-ok', '✓'), el('c-name', title), el('c-note', 'ready'));

    const run = async () => {
      for (const step of commands) {
        await typeCommand(step.cmd);
        await pace(reduceMotion ? 0 : 260);
        if (step.out) addLine(el('c-out', step.out));
        await pace(reduceMotion ? 0 : 320);
      }
      if (!data.titles.length) return;
      if (reduceMotion) { data.titles.slice(0, 6).forEach(streamLine); return; }   // static snapshot
      for (let i = 0; ; i = (i + 1) % data.titles.length) {
        streamLine(data.titles[i]);
        await pace(i === data.titles.length - 1 ? 1600 : 850);
      }
    };

    // Count-up for the stat tiles once the console is on screen
    const countUp = () => box.querySelectorAll('.stat-num').forEach((n) => {
      const target = parseInt(n.dataset.count, 10) || 0;
      if (reduceMotion || target < 1) return;
      const t0 = performance.now();
      const step = (now) => {
        const k = Math.min((now - t0) / 1100, 1);
        n.textContent = Math.round(target * (1 - Math.pow(1 - k, 3)));
        if (k < 1) requestAnimationFrame(step);
      };
      n.textContent = '0';
      requestAnimationFrame(step);
    });

    let started = false;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        visible = entries[0].isIntersecting;
        if (visible && !started) { started = true; countUp(); run(); }
      }, { threshold: 0.25 }).observe(box);
    } else {
      visible = true; started = true; run();
    }
  }

  // ---- After a contact-form error, jump back to the form ----
  const target = document.body.dataset.scroll;
  if (target) {
    const el = document.getElementById(target);
    if (el) requestAnimationFrame(() => el.scrollIntoView({ behavior: 'auto', block: 'start' }));
  }
})();
