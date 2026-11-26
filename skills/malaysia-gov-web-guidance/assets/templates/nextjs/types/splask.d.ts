// `timestamp` has no hyphen, so TypeScript rejects it on HTML elements unless declared once.
// Hyphenated splwpk-* attributes pass through JSX without a declaration.
import 'react';

declare module 'react' {
  interface HTMLAttributes<T> {
    timestamp?: string;
  }
}
