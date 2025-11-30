# REQ-TUTORIAL-001: Interactive Tutorial - Purchase Module

## Overview

Tutorial interactivo para módulo de compras orientado a usuarios no técnicos (+50 años).

**Estimación Total**: 14h  
**Quants**: 7  
**Prioridad**: Medium  

---

## Quant Index

| Quant | Nombre | Horas | Estado | Dependencias |
|-------|--------|-------|--------|--------------|
| Q1 | Library Research | 1h | 🔴 Pending | - |
| Q2 | Step Definitions | 2h | 🔴 Pending | Q1 |
| Q3 | TutorialOverlay Component | 3h | 🔴 Pending | Q1 |
| Q4 | Focus Animation CSS | 2h | 🔴 Pending | Q3 |
| Q5 | Purchase Layout Integration | 2h | 🔴 Pending | Q3, Q4 |
| Q6 | Unit Tests | 2h | 🔴 Pending | Q3, Q4, Q5 |
| Q7 | E2E Validation | 2h | 🔴 Pending | Q5 |

---

## Dependency Graph

```
Q1 (Research)
 ├──→ Q2 (Step Definitions)
 └──→ Q3 (TutorialOverlay)
       └──→ Q4 (CSS Animation)
             └──→ Q5 (Integration)
                   └──→ Q6 (Unit Tests)
                         └──→ Q7 (E2E)
```

---

## Files

- `Q1_LIBRARY_RESEARCH.md` - Evaluación driver.js vs react-joyride
- `Q2_STEP_DEFINITIONS.md` - purchaseTutorialSteps.js estructura
- `Q3_TUTORIAL_OVERLAY.md` - Componente principal
- `Q4_FOCUS_ANIMATION.md` - CSS Modules + keyframes
- `Q5_INTEGRATION.md` - PurchaseLayout + UserContext
- `Q6_UNIT_TESTS.md` - Jest + RTL specs
- `Q7_E2E_VALIDATION.md` - Playwright MCP protocol

---

## Acceptance Criteria Summary

- [ ] Tutorial auto-starts on first purchase module visit
- [ ] Focus animation (zoom in/out pulse)
- [ ] Popup <20 words per step
- [ ] Next/Previous/Skip navigation
- [ ] Keyboard accessible (Tab, Enter, Esc)
- [ ] Local storage persistence
- [ ] Restart tutorial option
