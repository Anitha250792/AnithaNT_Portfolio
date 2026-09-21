/*
 * AI voice guide
 * --------------
 * Reads the portfolio aloud with the browser's built-in speech (Web Speech API):
 * free, no API key, nothing leaves the visitor's device, and it never starts by itself.
 *
 * How it finds what to say:
 *   - every section carries data-topic="intro|about|skills|projects|journey|contact"
 *   - inside it, each element with a data-say attribute is one spoken chunk.
 *     data-say="some text" is spoken as written; data-say="" reads the element's visible text.
 * The element being read is highlighted and scrolled into view.
 */
(() => {
  'use strict';

  const dock = document.getElementById('ai-dock');
  if (!dock) return;

  const $ = (id) => document.getElementById(id);
  const fab = $('ai-fab');
  const panel = $('ai-panel');
  const closeBtn = $('ai-close');
  const statusEl = $('ai-status');
  const caption = $('ai-caption');
  const progress = $('ai-progress');
  const playBtn = $('ai-play');
  const prevBtn = $('ai-prev');
  const nextBtn = $('ai-next');
  const stopBtn = $('ai-stop');
  const rateSel = $('ai-rate');
  const voiceSel = $('ai-voice');
  const unsupportedNote = $('ai-unsupported');
  const chips = Array.from(dock.querySelectorAll('[data-ai-topic]'));

  const synth = window.speechSynthesis;
  const supported = !!synth && typeof window.SpeechSynthesisUtterance === 'function';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const IDLE_TEXT = caption.textContent;
  const CLOSING = "That's the full tour. Thanks for listening!";
  const LABELS = {
    intro: 'Intro', about: 'About', skills: 'Skills', projects: 'Projects',
    journey: 'Journey', contact: 'Contact', tour: 'Full tour',
  };

  let queue = [];        // [{ el, text, topic }]
  let index = 0;         // current chunk
  let topic = null;
  let state = 'idle';    // 'idle' | 'playing' | 'paused'
  let session = 0;       // bumped on every (re)start so stale speech callbacks are ignored
  let utterance = null;  // keep a reference: some browsers garbage-collect it mid-speech
  let voices = [];
  let lit = null;
  let startTimer = 0;

  // ---------- saved preferences ----------
  const prefs = {
    read() { try { return JSON.parse(localStorage.getItem('aiGuide') || '{}'); } catch (e) { return {}; } },
    save(patch) { try { localStorage.setItem('aiGuide', JSON.stringify({ ...prefs.read(), ...patch })); } catch (e) { /* private mode */ } },
  };

  // ---------- panel ----------
  const openPanel = () => { panel.hidden = false; fab.setAttribute('aria-expanded', 'true'); };
  const closePanel = () => { panel.hidden = true; fab.setAttribute('aria-expanded', 'false'); };
  fab.addEventListener('click', () => (panel.hidden ? openPanel() : closePanel()));
  closeBtn.addEventListener('click', () => { closePanel(); fab.focus(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !panel.hidden) closePanel(); });

  if (!supported) {
    unsupportedNote.hidden = false;
    [playBtn, prevBtn, nextBtn, stopBtn, rateSel, voiceSel].forEach((el) => { el.disabled = true; });
    chips.forEach((c) => { c.disabled = true; });
  }

  // ---------- voices ----------
  function loadVoices() {
    if (!supported) return;
    const rank = (v) => {
      const l = v.lang.replace('_', '-').toLowerCase();
      return l === 'en-in' ? 0 : l === 'en-gb' ? 1 : l === 'en-us' ? 2 : 3;
    };
    const quality = (v) => (/natural|neural|online|google/i.test(v.name) ? 0 : 1);
    voices = synth.getVoices()
      .filter((v) => /^en([-_]|$)/i.test(v.lang))
      .sort((a, b) => rank(a) - rank(b) || quality(a) - quality(b) || a.name.localeCompare(b.name));

    voiceSel.innerHTML = '';
    if (!voices.length) {
      voiceSel.innerHTML = '<option value="">Default voice</option>';
      return;
    }
    voices.forEach((v) => {
      const o = document.createElement('option');
      o.value = v.voiceURI;
      o.textContent = `${v.name} (${v.lang})`;
      voiceSel.appendChild(o);
    });
    const saved = prefs.read().voice;
    voiceSel.value = (voices.find((v) => v.voiceURI === saved) || voices[0]).voiceURI;
  }
  if (supported) {
    loadVoices();
    synth.addEventListener('voiceschanged', loadVoices);
  }
  const rateSaved = parseFloat(prefs.read().rate);
  if (rateSaved && Array.from(rateSel.options).some((o) => parseFloat(o.value) === rateSaved)) rateSel.value = String(rateSaved);

  const chosenVoice = () => voices.find((v) => v.voiceURI === voiceSel.value) || null;

  // ---------- reading the page ----------
  function textOf(el) {
    const said = (el.getAttribute('data-say') || '').trim();
    return (said || el.textContent).replace(/\s+/g, ' ').trim();
  }

  function collect(t) {
    const selector = t === 'tour' ? '[data-topic] [data-say]' : `[data-topic="${t}"] [data-say]`;
    const items = Array.from(document.querySelectorAll(selector))
      .map((el) => ({ el, text: textOf(el), topic: el.closest('[data-topic]').dataset.topic }))
      .filter((item) => item.text);
    if (t === 'tour' && items.length) items.push({ el: null, text: CLOSING, topic: 'contact' });
    return items;
  }

  // Long chunks are spoken sentence by sentence (long single utterances stall in some browsers).
  function splitText(text) {
    if (text.length <= 220) return [text];
    const sentences = [];
    let start = 0;
    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      if ((ch === '.' || ch === '!' || ch === '?') && (i === text.length - 1 || /\s/.test(text[i + 1]))) {
        sentences.push(text.slice(start, i + 1).trim());
        start = i + 1;
      }
    }
    if (start < text.length && text.slice(start).trim()) sentences.push(text.slice(start).trim());

    const parts = [];
    let buf = '';
    sentences.forEach((s) => {
      if (buf && (buf + ' ' + s).length > 220) { parts.push(buf); buf = s; } else { buf = buf ? buf + ' ' + s : s; }
    });
    if (buf) parts.push(buf);
    return parts;
  }

  // ---------- highlight + captions ----------
  function clearHighlight() {
    if (lit) lit.classList.remove('is-speaking');
    lit = null;
  }

  function highlight(el) {
    clearHighlight();
    if (!el) return;
    el.classList.add('is-speaking');
    lit = el;
    el.scrollIntoView({
      behavior: reduceMotion ? 'auto' : 'smooth',
      block: window.innerWidth >= 992 ? 'center' : 'start',
    });
  }

  function showCaption(parts) {
    caption.textContent = '';
    parts.forEach((p) => {
      const span = document.createElement('span');
      span.textContent = p + ' ';
      if (parts.length === 1) span.className = 'on';
      caption.appendChild(span);
    });
    caption.scrollTop = 0;
  }

  function markPart(i) {
    const spans = Array.from(caption.children);
    spans.forEach((s, k) => s.classList.toggle('on', spans.length === 1 || k === i));
    const on = spans[i];
    if (on) {
      const top = on.getBoundingClientRect().top - caption.getBoundingClientRect().top + caption.scrollTop;
      caption.scrollTo({ top: Math.max(0, top - 6), behavior: reduceMotion ? 'auto' : 'smooth' });
    }
  }

  // ---------- UI state ----------
  function updateUI() {
    const playing = state === 'playing';
    dock.classList.toggle('is-talking', playing);
    document.body.classList.toggle('ai-speaking', playing);

    playBtn.innerHTML = playing ? '<i class="fa-solid fa-pause"></i>' : '<i class="fa-solid fa-play"></i>';
    playBtn.setAttribute('aria-label', playing ? 'Pause' : state === 'paused' ? 'Resume' : 'Play');

    const item = queue[index];
    const label = LABELS[item ? item.topic : topic] || '';
    statusEl.textContent = state === 'idle' ? 'Ready'
      : `${state === 'paused' ? 'Paused' : 'Speaking'} · ${label} · ${Math.min(index + 1, queue.length)} of ${queue.length}`;

    chips.forEach((c) => c.setAttribute('aria-pressed', String(state !== 'idle' && c.dataset.aiTopic === topic)));
    [prevBtn, nextBtn, stopBtn].forEach((b) => { b.disabled = !supported || state === 'idle'; });
    progress.style.setProperty('--p', state === 'idle' || !queue.length ? '0%' : `${(index / queue.length) * 100}%`);
  }

  // ---------- speaking ----------
  function speakPart(parts, i, sid) {
    if (sid !== session || state !== 'playing') return;
    if (i >= parts.length) { index += 1; speakItem(); return; }

    markPart(i);
    const u = new window.SpeechSynthesisUtterance(parts[i]);
    const voice = chosenVoice();
    try {
      if (voice) { u.voice = voice; u.lang = voice.lang; } else { u.lang = 'en-IN'; }
    } catch (e) { /* stale voice: fall back to the browser default */ }
    u.rate = parseFloat(rateSel.value) || 1;

    u.onstart = () => clearTimeout(startTimer);
    u.onend = () => speakPart(parts, i + 1, sid);
    u.onerror = (e) => {
      if (sid !== session) return;
      if (e.error === 'interrupted' || e.error === 'canceled') return;
      clearTimeout(startTimer);
      state = 'idle';
      clearHighlight();
      caption.textContent = 'The browser could not play this audio. Try another voice or browser.';
      updateUI();
    };

    utterance = u;
    clearTimeout(startTimer);
    startTimer = setTimeout(() => {
      if (sid === session && state === 'playing') statusEl.textContent = 'No sound? Check your volume or try another voice.';
    }, 4500);
    synth.speak(u);
  }

  function speakItem() {
    const item = queue[index];
    if (!item) { finish(); return; }
    highlight(item.el);
    const parts = splitText(item.text);
    showCaption(parts);
    updateUI();
    speakPart(parts, 0, session);
  }

  function finish() {
    clearHighlight();
    clearTimeout(startTimer);
    state = 'idle';
    index = 0;
    caption.textContent = 'Finished. Pick another topic to keep listening.';
    updateUI();
  }

  // (Re)start speaking from the current chunk.
  function restart() {
    const sid = (session += 1);
    state = 'playing';
    if (synth.speaking || synth.pending) {
      synth.cancel();
      setTimeout(() => { if (sid === session) speakItem(); }, 80); // Chrome drops speak() right after cancel()
    } else {
      speakItem();
    }
  }

  // ---------- controls ----------
  function startTopic(t) {
    openPanel();
    if (!supported) return;
    const items = collect(t);
    if (!items.length) return;
    topic = t;
    queue = items;
    index = 0;
    restart();
  }

  function pause() {
    session += 1;
    state = 'paused';
    clearTimeout(startTimer);
    synth.cancel();
    updateUI();
  }

  function stop() {
    session += 1;
    state = 'idle';
    topic = null;
    index = 0;
    queue = [];
    clearTimeout(startTimer);
    synth.cancel();
    clearHighlight();
    caption.textContent = IDLE_TEXT;
    updateUI();
  }

  function step(delta) {
    if (state === 'idle' || !queue.length) return;
    const next = index + delta;
    if (next < 0) { index = 0; } else if (next >= queue.length) { session += 1; synth.cancel(); finish(); return; } else { index = next; }
    restart();
  }

  playBtn.addEventListener('click', () => {
    if (state === 'playing') pause();
    else if (state === 'paused') restart();
    else startTopic(topic || 'tour');
  });
  prevBtn.addEventListener('click', () => step(-1));
  nextBtn.addEventListener('click', () => step(1));
  stopBtn.addEventListener('click', stop);
  chips.forEach((chip) => chip.addEventListener('click', () => startTopic(chip.dataset.aiTopic)));
  document.querySelectorAll('[data-listen]').forEach((btn) => btn.addEventListener('click', () => startTopic(btn.dataset.listen)));

  rateSel.addEventListener('change', () => { prefs.save({ rate: rateSel.value }); if (state === 'playing') restart(); });
  voiceSel.addEventListener('change', () => { prefs.save({ voice: voiceSel.value }); if (state === 'playing') restart(); });

  // Never leave the voice talking after the page is closed or reloaded.
  window.addEventListener('pagehide', () => { if (supported) synth.cancel(); });

  updateUI();
})();
