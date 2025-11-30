# Q3: TutorialOverlay Component

## Metadata

**Quant ID**: Q3  
**Horas**: 3h  
**Estado**: 🔴 Pending  
**Dependencias**: Q1 (library selected)  

---

## Objetivo

Componente principal que orquesta el tutorial.

---

## Output Files

```
frontend/src/components/tutorial/
├── TutorialOverlay.jsx
├── TutorialOverlay.module.css
├── TutorialPopup.jsx
├── TutorialPopup.module.css
├── TutorialControls.jsx
├── TutorialControls.module.css
└── useTutorial.js
```

---

## Component Structure

### TutorialOverlay.jsx

```jsx
// Props
{
  steps: Array<TutorialStep>,
  onComplete: () => void,
  onSkip: () => void,
  initialStep?: number,
}

// State (useTutorial hook)
{
  currentStep: number,
  isActive: boolean,
  direction: 'forward' | 'backward',
}

// Render
<>
  <DimmedBackground />
  <FocusHighlight target={steps[currentStep].target} />
  <TutorialPopup step={steps[currentStep]} />
  <TutorialControls 
    onNext={nextStep}
    onPrev={prevStep}
    onSkip={skip}
    progress={currentStep / steps.length}
  />
</>
```

### useTutorial.js (Custom Hook)

```javascript
export function useTutorial(steps, options = {}) {
  const [currentStep, setCurrentStep] = useState(options.initialStep ?? 0);
  const [isActive, setIsActive] = useState(true);
  
  // Local storage sync
  useEffect(() => {
    localStorage.setItem('tutorial_purchase_current_step', currentStep);
  }, [currentStep]);
  
  // Resume from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('tutorial_purchase_current_step');
    if (saved) setCurrentStep(parseInt(saved));
  }, []);
  
  const next = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(prev => prev + 1);
    } else {
      complete();
    }
  };
  
  const prev = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };
  
  const skip = () => {
    setIsActive(false);
    options.onSkip?.();
  };
  
  const complete = () => {
    localStorage.setItem('tutorial_purchase_completed', 'true');
    localStorage.removeItem('tutorial_purchase_current_step');
    setIsActive(false);
    options.onComplete?.();
  };
  
  return {
    currentStep,
    step: steps[currentStep],
    isActive,
    progress: (currentStep + 1) / steps.length,
    next,
    prev,
    skip,
    complete,
  };
}
```

### TutorialPopup.jsx

```jsx
// Props
{
  step: TutorialStep,
  position: 'top' | 'bottom' | 'left' | 'right',
}

// Features
- Auto-positioning based on target element
- Arrow pointing to target
- Max-width 300px
- Font-size 16px (readable)
- Close button (X)
```

### TutorialControls.jsx

```jsx
// Props
{
  onNext: () => void,
  onPrev: () => void,
  onSkip: () => void,
  progress: number, // 0-1
  canGoPrev: boolean,
  isLastStep: boolean,
}

// Buttons
- "Previous" (disabled on step 0)
- "Next" / "Complete" (last step)
- "Skip Tutorial" (always visible)
- Progress bar (step X of Y)
```

---

## Accessibility Requirements

```jsx
// ARIA attributes
<div role="dialog" aria-modal="true" aria-labelledby="tutorial-title">
  <h2 id="tutorial-title">{step.title}</h2>
  <p>{step.description}</p>
  <button aria-label="Previous step">Previous</button>
  <button aria-label="Next step">Next</button>
  <button aria-label="Skip tutorial">Skip</button>
</div>

// Keyboard handlers
useEffect(() => {
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') skip();
    if (e.key === 'ArrowRight') next();
    if (e.key === 'ArrowLeft') prev();
    if (e.key === 'Enter') next();
  };
  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []);
```

---

## Design Tokens

```css
/* Use existing tokens.css */
--tutorial-popup-bg: var(--color-white);
--tutorial-popup-shadow: var(--shadow-lg);
--tutorial-popup-radius: var(--radius-lg);
--tutorial-highlight-color: var(--color-primary-500);
--tutorial-dimmed-bg: rgba(0, 0, 0, 0.5);
--tutorial-transition: 300ms ease-in-out;
```

---

## Acceptance Criteria

- [ ] TutorialOverlay renderiza correctamente
- [ ] useTutorial maneja estado (next/prev/skip)
- [ ] Local storage persiste progreso
- [ ] Keyboard navigation funciona
- [ ] ARIA labels presentes
- [ ] Responsive (desktop/tablet)
