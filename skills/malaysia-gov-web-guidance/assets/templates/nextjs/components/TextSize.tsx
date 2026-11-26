'use client';
// Text-size control for splwpk-w3c. Client components are still server-rendered in the App Router,
// so the tag is in the first HTML; the handlers are added after hydration. Same behaviour as the
// splask-tagging guide snippet: data-fs scale, aria-pressed state, remembered in localStorage.
import { useEffect, useState } from 'react';

const SIZES = [
  { fs: '0.875', label: 'A-', ms: 'Kecilkan tulisan', en: 'Smaller text' },
  { fs: '1', label: 'A', ms: 'Saiz tulisan biasa', en: 'Normal text size' },
  { fs: '1.25', label: 'A+', ms: 'Besarkan tulisan', en: 'Larger text' },
];

export function TextSize({ label, lang = 'ms' }: { label: string; lang?: 'ms' | 'en' }) {
  const [current, setCurrent] = useState('1');
  const apply = (fs: string) => {
    document.documentElement.style.fontSize = `${16 * parseFloat(fs)}px`;
    setCurrent(fs);
    try { localStorage.setItem('fs', fs); } catch {}
  };
  useEffect(() => {
    try { const saved = localStorage.getItem('fs'); if (saved) apply(saved); } catch {}
  }, []);
  return (
    <div role="group" aria-label={label} splwpk-w3c="splwpk-w3c">
      {SIZES.map((s) => (
        <button key={s.fs} type="button" data-fs={s.fs} aria-label={lang === 'en' ? s.en : s.ms} aria-pressed={current === s.fs} onClick={() => apply(s.fs)}>
          {s.label}
        </button>
      ))}
    </div>
  );
}
