# Q4: Focus Animation CSS

## Metadata

**Quant ID**: Q4  
**Horas**: 2h  
**Estado**: 🔴 Pending  
**Dependencias**: Q3 (TutorialOverlay exists)  

---

## Objetivo

Implementar animaciones de focus (zoom in/out, pulse) con CSS Modules.

---

## Output Files

```
frontend/src/components/tutorial/
├── FocusZone.jsx
└── FocusZone.module.css
```

---

## Animation Specs

### 1. Focus Pulse (Loop)

```css
@keyframes focusPulse {
  0%, 100% {
    transform: scale(1.0);
    box-shadow: 0 0 0 4px var(--color-primary-500),
                0 0 20px 8px rgba(99, 102, 241, 0.4);
  }
  50% {
    transform: scale(1.03);
    box-shadow: 0 0 0 6px var(--color-primary-500),
                0 0 30px 12px rgba(99, 102, 241, 0.6);
  }
}

.focusedElement {
  position: relative;
  z-index: 10000;
  animation: focusPulse 1.5s ease-in-out infinite;
  border-radius: var(--radius-md);
}
```

### 2. Zoom In (Entry)

```css
@keyframes zoomIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.entering {
  animation: zoomIn 300ms ease-out forwards;
}
```

### 3. Zoom Out (Exit)

```css
@keyframes zoomOut {
  from {
    transform: scale(1);
    opacity: 1;
  }
  to {
    transform: scale(0.95);
    opacity: 0;
  }
}

.exiting {
  animation: zoomOut 200ms ease-in forwards;
}
```

### 4. Background Dim

```css
.dimmedBackground {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 9998;
  transition: opacity 300ms ease-in-out;
}

.dimmedBackground.entering {
  animation: fadeIn 300ms ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

---

## FocusZone.jsx Component

```jsx
import { useEffect, useRef, useState } from 'react';
import styles from './FocusZone.module.css';

export function FocusZone({ target, isActive }) {
  const [bounds, setBounds] = useState(null);
  const [phase, setPhase] = useState('entering'); // entering | active | exiting
  
  useEffect(() => {
    if (!target) return;
    
    const element = document.querySelector(target);
    if (!element) {
      console.warn(`Tutorial target not found: ${target}`);
      return;
    }
    
    // Get element bounds
    const rect = element.getBoundingClientRect();
    setBounds({
      top: rect.top - 8,
      left: rect.left - 8,
      width: rect.width + 16,
      height: rect.height + 16,
    });
    
    // Phase transitions
    setPhase('entering');
    const timer = setTimeout(() => setPhase('active'), 300);
    
    return () => clearTimeout(timer);
  }, [target]);
  
  if (!bounds || !isActive) return null;
  
  return (
    <>
      {/* Dimmed background with cutout */}
      <div className={styles.dimmedBackground} />
      
      {/* Focus highlight */}
      <div 
        className={`${styles.focusHighlight} ${styles[phase]}`}
        style={{
          top: bounds.top,
          left: bounds.left,
          width: bounds.width,
          height: bounds.height,
        }}
      />
    </>
  );
}
```

---

## CSS Variables (tokens.css additions)

```css
/* Tutorial-specific tokens */
--tutorial-pulse-duration: 1.5s;
--tutorial-transition-in: 300ms;
--tutorial-transition-out: 200ms;
--tutorial-highlight-padding: 8px;
--tutorial-highlight-color: var(--color-primary-500);
--tutorial-highlight-glow: rgba(99, 102, 241, 0.4);
--tutorial-dim-opacity: 0.5;
--tutorial-blur: 4px;
```

---

## Performance Considerations

1. **will-change**: Use sparingly (only on animated elements)
2. **transform**: Use for animations (GPU accelerated)
3. **opacity**: Prefer over visibility for transitions
4. **requestAnimationFrame**: For bounds calculation
5. **debounce**: Window resize handler

```jsx
// Optimized bounds update
useEffect(() => {
  let rafId;
  const updateBounds = () => {
    rafId = requestAnimationFrame(() => {
      const element = document.querySelector(target);
      if (element) {
        const rect = element.getBoundingClientRect();
        setBounds({ /* ... */ });
      }
    });
  };
  
  updateBounds();
  window.addEventListener('resize', updateBounds);
  window.addEventListener('scroll', updateBounds);
  
  return () => {
    cancelAnimationFrame(rafId);
    window.removeEventListener('resize', updateBounds);
    window.removeEventListener('scroll', updateBounds);
  };
}, [target]);
```

---

## Acceptance Criteria

- [ ] Focus pulse animation visible (1.5s loop)
- [ ] Zoom in/out transitions smooth (300ms/200ms)
- [ ] Background dim with blur
- [ ] 60 FPS performance (no jank)
- [ ] Bounds update on scroll/resize
- [ ] Graceful fallback if target not found
