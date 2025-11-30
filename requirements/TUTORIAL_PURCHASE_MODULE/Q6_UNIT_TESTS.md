# Q6: Unit Tests

## Metadata

**Quant ID**: Q6  
**Horas**: 2h  
**Estado**: 🔴 Pending  
**Dependencias**: Q3, Q4, Q5 (All components ready)  

---

## Objetivo

Tests unitarios con Jest + React Testing Library (RTL).

---

## Test Files

```
frontend/src/components/tutorial/__tests__/
├── TutorialOverlay.test.jsx
├── TutorialPopup.test.jsx
├── TutorialControls.test.jsx
├── FocusZone.test.jsx
└── useTutorial.test.js
```

---

## Test Coverage Target

| Component | Coverage |
|-----------|----------|
| TutorialOverlay | 90% |
| useTutorial | 95% |
| FocusZone | 85% |
| TutorialPopup | 85% |
| TutorialControls | 90% |

**Overall Target**: 85%+

---

## TutorialOverlay.test.jsx

```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { TutorialOverlay } from '../TutorialOverlay';

const mockSteps = [
  { id: 'step-1', target: '[data-testid="btn-1"]', title: 'Step 1', description: 'First step' },
  { id: 'step-2', target: '[data-testid="btn-2"]', title: 'Step 2', description: 'Second step' },
  { id: 'step-3', target: '[data-testid="btn-3"]', title: 'Step 3', description: 'Third step' },
];

describe('TutorialOverlay', () => {
  beforeEach(() => {
    localStorage.clear();
    // Add mock target elements
    document.body.innerHTML = `
      <button data-testid="btn-1">Button 1</button>
      <button data-testid="btn-2">Button 2</button>
      <button data-testid="btn-3">Button 3</button>
    `;
  });

  test('renders first step on mount', () => {
    render(<TutorialOverlay steps={mockSteps} onComplete={jest.fn()} onSkip={jest.fn()} />);
    expect(screen.getByText('Step 1')).toBeInTheDocument();
    expect(screen.getByText('First step')).toBeInTheDocument();
  });

  test('advances to next step on Next click', () => {
    render(<TutorialOverlay steps={mockSteps} onComplete={jest.fn()} onSkip={jest.fn()} />);
    fireEvent.click(screen.getByText('Next'));
    expect(screen.getByText('Step 2')).toBeInTheDocument();
  });

  test('goes back on Previous click', () => {
    render(<TutorialOverlay steps={mockSteps} onComplete={jest.fn()} onSkip={jest.fn()} initialStep={1} />);
    fireEvent.click(screen.getByText('Previous'));
    expect(screen.getByText('Step 1')).toBeInTheDocument();
  });

  test('calls onComplete on last step Next', () => {
    const onComplete = jest.fn();
    render(<TutorialOverlay steps={mockSteps} onComplete={onComplete} onSkip={jest.fn()} initialStep={2} />);
    fireEvent.click(screen.getByText('Complete'));
    expect(onComplete).toHaveBeenCalled();
  });

  test('calls onSkip when Skip clicked', () => {
    const onSkip = jest.fn();
    render(<TutorialOverlay steps={mockSteps} onComplete={jest.fn()} onSkip={onSkip} />);
    fireEvent.click(screen.getByText('Skip Tutorial'));
    expect(onSkip).toHaveBeenCalled();
  });

  test('keyboard navigation works (ArrowRight)', () => {
    render(<TutorialOverlay steps={mockSteps} onComplete={jest.fn()} onSkip={jest.fn()} />);
    fireEvent.keyDown(window, { key: 'ArrowRight' });
    expect(screen.getByText('Step 2')).toBeInTheDocument();
  });

  test('keyboard navigation works (Escape)', () => {
    const onSkip = jest.fn();
    render(<TutorialOverlay steps={mockSteps} onComplete={jest.fn()} onSkip={onSkip} />);
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(onSkip).toHaveBeenCalled();
  });
});
```

---

## useTutorial.test.js

```jsx
import { renderHook, act } from '@testing-library/react';
import { useTutorial } from '../useTutorial';

const mockSteps = [
  { id: 'step-1', title: 'Step 1' },
  { id: 'step-2', title: 'Step 2' },
  { id: 'step-3', title: 'Step 3' },
];

describe('useTutorial', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('initializes at step 0', () => {
    const { result } = renderHook(() => useTutorial(mockSteps));
    expect(result.current.currentStep).toBe(0);
    expect(result.current.step.id).toBe('step-1');
  });

  test('next() advances step', () => {
    const { result } = renderHook(() => useTutorial(mockSteps));
    act(() => result.current.next());
    expect(result.current.currentStep).toBe(1);
  });

  test('prev() goes back', () => {
    const { result } = renderHook(() => useTutorial(mockSteps, { initialStep: 2 }));
    act(() => result.current.prev());
    expect(result.current.currentStep).toBe(1);
  });

  test('prev() at step 0 does nothing', () => {
    const { result } = renderHook(() => useTutorial(mockSteps));
    act(() => result.current.prev());
    expect(result.current.currentStep).toBe(0);
  });

  test('next() at last step calls complete', () => {
    const onComplete = jest.fn();
    const { result } = renderHook(() => useTutorial(mockSteps, { onComplete, initialStep: 2 }));
    act(() => result.current.next());
    expect(onComplete).toHaveBeenCalled();
  });

  test('skip() calls onSkip', () => {
    const onSkip = jest.fn();
    const { result } = renderHook(() => useTutorial(mockSteps, { onSkip }));
    act(() => result.current.skip());
    expect(onSkip).toHaveBeenCalled();
    expect(result.current.isActive).toBe(false);
  });

  test('saves progress to localStorage', () => {
    const { result } = renderHook(() => useTutorial(mockSteps));
    act(() => result.current.next());
    expect(localStorage.getItem('tutorial_purchase_current_step')).toBe('1');
  });

  test('resumes from localStorage', () => {
    localStorage.setItem('tutorial_purchase_current_step', '2');
    const { result } = renderHook(() => useTutorial(mockSteps));
    expect(result.current.currentStep).toBe(2);
  });

  test('complete() sets completed flag', () => {
    const { result } = renderHook(() => useTutorial(mockSteps, { initialStep: 2 }));
    act(() => result.current.next());
    expect(localStorage.getItem('tutorial_purchase_completed')).toBe('true');
  });

  test('progress calculation is correct', () => {
    const { result } = renderHook(() => useTutorial(mockSteps));
    expect(result.current.progress).toBeCloseTo(1/3);
    act(() => result.current.next());
    expect(result.current.progress).toBeCloseTo(2/3);
  });
});
```

---

## FocusZone.test.jsx

```jsx
import { render, screen } from '@testing-library/react';
import { FocusZone } from '../FocusZone';

describe('FocusZone', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <button data-testid="target-btn">Target</button>
    `;
  });

  test('renders dimmed background when active', () => {
    render(<FocusZone target="[data-testid='target-btn']" isActive={true} />);
    expect(document.querySelector('.dimmedBackground')).toBeInTheDocument();
  });

  test('does not render when inactive', () => {
    const { container } = render(<FocusZone target="[data-testid='target-btn']" isActive={false} />);
    expect(container.firstChild).toBeNull();
  });

  test('positions highlight over target element', () => {
    render(<FocusZone target="[data-testid='target-btn']" isActive={true} />);
    const highlight = document.querySelector('.focusHighlight');
    expect(highlight).toHaveStyle({ position: 'absolute' });
  });

  test('handles missing target gracefully', () => {
    const consoleSpy = jest.spyOn(console, 'warn').mockImplementation();
    render(<FocusZone target="[data-testid='nonexistent']" isActive={true} />);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('not found'));
    consoleSpy.mockRestore();
  });
});
```

---

## Run Commands

```bash
# Run tutorial tests
cd frontend && npm test -- --testPathPattern="tutorial"

# Run with coverage
cd frontend && npm test -- --coverage --testPathPattern="tutorial"

# Watch mode
cd frontend && npm test -- --watch --testPathPattern="tutorial"
```

---

## Acceptance Criteria

- [ ] All tests pass (0 failures)
- [ ] Coverage ≥85% per component
- [ ] Mock localStorage working
- [ ] Mock DOM elements for target detection
- [ ] Keyboard events tested
- [ ] Edge cases covered (missing target, last step, etc.)
