'use client';
// Text-size control for splwpk-w3c. Client components are still server-rendered in the App Router,
// so the tag is in the first HTML; the click handlers are added after hydration.

export function TextSize({ label }: { label: string }) {
  const set = (step: number) => {
    document.documentElement.style.fontSize = step === 0 ? '' : `${100 + step * 12.5}%`;
  };
  return (
    <div role="group" aria-label={label} splwpk-w3c="splwpk-w3c">
      <button type="button" onClick={() => set(-1)}>A-</button>
      <button type="button" onClick={() => set(0)}>A</button>
      <button type="button" onClick={() => set(1)}>A+</button>
    </div>
  );
}
