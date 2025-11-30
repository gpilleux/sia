# Q5: Purchase Layout Integration

## Metadata

**Quant ID**: Q5  
**Horas**: 2h  
**Estado**: 🔴 Pending  
**Dependencias**: Q3, Q4 (Components ready)  

---

## Objetivo

Integrar TutorialOverlay en el módulo de compras con detección automática de primer uso.

---

## Files to Modify

```
frontend/src/
├── components/purchase/PurchaseLayout.jsx    # Add TutorialOverlay
├── contexts/UserContext.jsx                  # Add tutorial state
└── pages/PurchasePage.jsx                    # Tutorial trigger
```

---

## Integration Points

### 1. UserContext Enhancement

```jsx
// frontend/src/contexts/UserContext.jsx

// Add to context state
const [showTutorial, setShowTutorial] = useState(false);
const [tutorialModule, setTutorialModule] = useState(null);

// Add to context value
const contextValue = {
  // ... existing values
  showTutorial,
  setShowTutorial,
  tutorialModule,
  startTutorial: (module) => {
    setTutorialModule(module);
    setShowTutorial(true);
  },
  dismissTutorial: () => {
    setShowTutorial(false);
    setTutorialModule(null);
  },
};
```

### 2. First Visit Detection

```jsx
// frontend/src/hooks/useTutorialTrigger.js

export function useTutorialTrigger(module) {
  const { startTutorial } = useContext(UserContext);
  
  useEffect(() => {
    const key = `tutorial_${module}_completed`;
    const completed = localStorage.getItem(key);
    
    if (!completed) {
      // Small delay to let page render first
      const timer = setTimeout(() => {
        startTutorial(module);
      }, 500);
      
      return () => clearTimeout(timer);
    }
  }, [module, startTutorial]);
}
```

### 3. PurchaseLayout Integration

```jsx
// frontend/src/components/purchase/PurchaseLayout.jsx

import { useContext } from 'react';
import { UserContext } from '../../contexts/UserContext';
import TutorialOverlay from '../tutorial/TutorialOverlay';
import { purchaseTutorialSteps } from '../../data/purchaseTutorialSteps';
import { useTutorialTrigger } from '../../hooks/useTutorialTrigger';

export default function PurchaseLayout({ children }) {
  const { showTutorial, tutorialModule, dismissTutorial } = useContext(UserContext);
  
  // Auto-trigger on first visit
  useTutorialTrigger('purchase');
  
  const handleComplete = () => {
    localStorage.setItem('tutorial_purchase_completed', 'true');
    dismissTutorial();
  };
  
  const handleSkip = () => {
    dismissTutorial();
  };
  
  return (
    <div className="purchase-layout">
      {/* Tutorial Overlay */}
      {showTutorial && tutorialModule === 'purchase' && (
        <TutorialOverlay
          steps={purchaseTutorialSteps}
          onComplete={handleComplete}
          onSkip={handleSkip}
        />
      )}
      
      {/* Existing layout content */}
      <header className="purchase-header">
        <h1>Purchase Module</h1>
        {/* Add restart tutorial button */}
        <button 
          onClick={() => {
            localStorage.removeItem('tutorial_purchase_completed');
            startTutorial('purchase');
          }}
          className="restart-tutorial-btn"
        >
          📚 Restart Tutorial
        </button>
      </header>
      
      <main className="purchase-content">
        {children}
      </main>
    </div>
  );
}
```

### 4. Settings Menu Option

```jsx
// Add to Settings or User Menu
<MenuItem onClick={() => {
  localStorage.removeItem('tutorial_purchase_completed');
  startTutorial('purchase');
}}>
  🔄 Restart Purchase Tutorial
</MenuItem>
```

---

## Route Configuration

```jsx
// frontend/src/App.jsx or routes config

<Route path="/purchase/*" element={
  <PurchaseLayout>
    <Outlet />
  </PurchaseLayout>
}>
  <Route path="requisitions" element={<RequisitionsPage />} />
  <Route path="rfq" element={<RFQPage />} />
  <Route path="orders" element={<PurchaseOrdersPage />} />
  {/* ... other purchase routes */}
</Route>
```

---

## Local Storage Keys

| Key | Type | Description |
|-----|------|-------------|
| `tutorial_purchase_completed` | boolean | Tutorial finished flag |
| `tutorial_purchase_current_step` | number | Resume position |
| `tutorial_purchase_skipped` | boolean | User skipped (optional) |

---

## Edge Cases

1. **User navigates away mid-tutorial**
   - Save current step to localStorage
   - Resume on return (if within same session)
   
2. **DOM element not found**
   - Log warning
   - Skip to next step automatically
   
3. **Tutorial interrupted by modal/dialog**
   - Pause tutorial
   - Resume when modal closes

```jsx
// Handle interruptions
useEffect(() => {
  const handleVisibilityChange = () => {
    if (document.hidden) {
      // Pause tutorial
      setIsPaused(true);
    }
  };
  
  document.addEventListener('visibilitychange', handleVisibilityChange);
  return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
}, []);
```

---

## Acceptance Criteria

- [ ] Tutorial auto-starts on first /purchase visit
- [ ] Tutorial persists state on page refresh
- [ ] "Restart Tutorial" button works
- [ ] Tutorial doesn't restart after completion
- [ ] Works with existing PurchaseLayout content
- [ ] No visual regression in purchase pages
