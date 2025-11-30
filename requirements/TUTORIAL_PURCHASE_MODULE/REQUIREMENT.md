# REQUIREMENT: Interactive Tutorial - Purchase Module

## METADATA

**ID**: REQ-TUTORIAL-001  
**Module**: Purchase  
**Priority**: Medium  
**Phase**: 4 (AI Agents Integration)  
**Target Users**: Company administrators (50+ age, low tech literacy)  
**Complexity**: Medium (Frontend focus, no domain logic changes)

---

## USER STORY

**As** a non-technical company administrator (50+ years old)  
**I want** a guided interactive tutorial for the purchase module  
**So that** I can learn the workflow step-by-step with visual focus and minimal text

**Acceptance Criteria**:
1. Tutorial follows purchase workflow sequence (Requisition → RFQ → PO → Receipt)
2. Focus animation highlights interactive zones (zoom in/out effect)
3. Popup with brief explanation (<20 words) per step
4. "Next" button advances to next step
5. Platform visible in background (dimmed/blurred)
6. Tutorial can be skipped or restarted
7. Tutorial triggers on first login to purchase module
8. Respects accessibility standards (keyboard navigation, screen readers)

---

## FUNCTIONAL REQUIREMENTS

### FR1: Tutorial Workflow Sequence

**Sequence** (matches purchase flow documented in `docs/testing/suites/E2E_PURCHASE.spr.md`):

1. **Requisition Creation**
   - Focus: "New Requisition" button (Requisitions List)
   - Popup: "Create purchase requests for needed items"
   - Next → Form fields (Item, Quantity, Justification)
   - Next → "Submit" button
   
2. **Requisition Approval**
   - Focus: Requisition row in list (status: Pending)
   - Popup: "Manager approves or rejects requests"
   - Next → "Approve" button
   
3. **RFQ Creation**
   - Focus: "Create RFQ from Requisition" button
   - Popup: "Request quotes from suppliers"
   - Next → RFQ form (Select suppliers, due date)
   - Next → "Send RFQ" button
   
4. **RFQ Response**
   - Focus: RFQ row → "Add Quote" button
   - Popup: "Suppliers submit their quotes"
   - Next → Quote form (Price, delivery time, notes)
   
5. **RFQ Evaluation**
   - Focus: "Accept Quote" button
   - Popup: "Choose best supplier quote"
   
6. **PO Creation**
   - Focus: "Create PO from RFQ" button
   - Popup: "Generate purchase order"
   - Next → PO form (Terms, delivery address)
   
7. **PO Approval**
   - Focus: PO row → "Approve" button
   - Popup: "Final approval before sending to supplier"
   
8. **PO Receipt**
   - Focus: PO row → "Mark as Received" button
   - Popup: "Confirm items received"

**Total Steps**: ~15-20 (granular focus per UI element)

---

### FR2: Visual Animation Behavior

**Focus Animation** (CSS + React):
- **Zoom In**: 
  - Scale focused element 1.05x
  - Drop shadow (0 0 20px rgba(primary, 0.6))
  - Transition: 300ms ease-in-out
  - Background: Dimmed (opacity 0.3, blur 4px)
  
- **Zoom Out**:
  - Restore normal scale (1x)
  - Remove shadow
  - Transition: 200ms ease-in-out
  
- **Cycle**:
  - Focus → Hold 2s → Zoom out → Wait 500ms → Next step (on "Next" click)
  - Pulse effect (subtle scale 1.0 → 1.02 → 1.0) every 1.5s while focused

**Popup Position**:
- Auto-calculate position (top/bottom/left/right) based on element location
- Arrow pointing to focused element
- Max width: 300px
- Font size: 16px (readable for older users)

---

### FR3: Tutorial State Management

**Local Storage**:
- `tutorial_purchase_completed`: boolean (skip on subsequent logins)
- `tutorial_purchase_current_step`: number (resume if interrupted)

**User Actions**:
- "Skip Tutorial" button (top-right corner)
- "Restart Tutorial" button (in purchase module settings)
- "Previous" button (go back one step)
- "Next" button (advance)

**Edge Cases**:
- If user navigates away → Save current step
- If element not found (DOM changes) → Skip to next valid step
- If tutorial completed → Show "✓ Tutorial Completed" badge

---

## NON-FUNCTIONAL REQUIREMENTS

### NFR1: Performance
- Animation FPS ≥ 60 (no jank)
- Tutorial script lazy-loaded (<50KB bundle)
- No backend calls (pure frontend)

### NFR2: Accessibility
- ARIA labels for screen readers
- Keyboard navigation (Tab, Enter, Esc)
- High contrast mode support
- Skip link (Esc key to exit tutorial)

### NFR3: Responsiveness
- Desktop primary target (≥1280px)
- Tablet support (768px-1279px, simplified layout)
- Mobile: Tutorial disabled (show text-based guide instead)

---

## TECHNICAL DESIGN

### Architecture

**Component Structure**:
```
frontend/src/components/tutorial/
├── TutorialOverlay.jsx          # Main orchestrator
├── FocusZone.jsx                # Highlight + animation
├── TutorialPopup.jsx            # Explanation card
├── TutorialControls.jsx         # Next/Prev/Skip buttons
└── useTutorial.js               # State management hook

frontend/src/data/
└── purchaseTutorialSteps.js     # Step definitions (array)
```

**Step Definition Schema**:
```javascript
{
  id: 'step-1-create-requisition',
  target: 'button[data-testid="new-requisition-btn"]', // CSS selector
  title: 'Create Requisition',
  description: 'Click here to request new items',
  position: 'bottom', // popup position
  action: 'click', // expected user action
  waitFor: null, // optional: wait for element to appear
}
```

**State Machine**:
```
IDLE → START_TUTORIAL → STEP_1 → STEP_2 → ... → COMPLETED
         ↑                ↓
         └─── SKIP/ESC ───┘
```

**Animation Implementation** (CSS Modules):
```css
/* FocusZone.module.css */
@keyframes focusPulse {
  0%, 100% { transform: scale(1.05); }
  50% { transform: scale(1.07); }
}

.focusedElement {
  position: relative;
  z-index: 9999;
  box-shadow: 0 0 0 4px var(--color-primary-500),
              0 0 20px 8px rgba(var(--color-primary-500-rgb), 0.6);
  animation: focusPulse 1.5s ease-in-out infinite;
  transition: all 300ms ease-in-out;
}

.dimmedBackground {
  backdrop-filter: blur(4px);
  background: rgba(0, 0, 0, 0.3);
}
```

---

### Integration Points

**Trigger** (first login detection):
```javascript
// frontend/src/contexts/UserContext.jsx
const checkTutorialStatus = () => {
  const completed = localStorage.getItem('tutorial_purchase_completed');
  if (!completed && location.pathname.includes('/purchase')) {
    setShowTutorial(true);
  }
};
```

**Purchase Module Entry**:
```javascript
// frontend/src/components/purchase/PurchaseLayout.jsx
import TutorialOverlay from '../tutorial/TutorialOverlay';

export default function PurchaseLayout() {
  const { showTutorial, setShowTutorial } = useContext(UserContext);
  
  return (
    <>
      {showTutorial && (
        <TutorialOverlay
          steps={purchaseTutorialSteps}
          onComplete={() => {
            localStorage.setItem('tutorial_purchase_completed', 'true');
            setShowTutorial(false);
          }}
          onSkip={() => setShowTutorial(false)}
        />
      )}
      {/* existing layout */}
    </>
  );
}
```

---

## TESTING STRATEGY

### Unit Tests
- `TutorialOverlay.test.jsx`: State transitions (start → complete)
- `FocusZone.test.jsx`: Element highlighting logic
- `useTutorial.test.js`: Step navigation, local storage

### E2E Tests (Playwright MCP)
- **Manual Validation** (following `docs/testing/protocols/PLAYWRIGHT_MCP.md`):
  1. Fresh user → Purchase module → Tutorial auto-starts
  2. Click "Next" through all steps → Verify focus animations
  3. Click "Skip" mid-tutorial → Verify state saved
  4. Reload page → Tutorial does not restart (completed flag)
  5. Click "Restart Tutorial" → Verify restart from step 1
  6. Test keyboard navigation (Tab, Enter, Esc)

**Expected Coverage**: 85%+ (TutorialOverlay + FocusZone + hook)

---

## DEPENDENCIES

**External Libraries** (evaluate):
- `react-joyride` (tour library, 11KB gzipped) - **Candidate**
- `driver.js` (lightweight, 5KB) - **Preferred** (KISS principle)
- `intro.js` (mature, 10KB) - **Alternative**

**Decision Criteria**:
1. Bundle size (<10KB)
2. Accessibility support (ARIA, keyboard)
3. Custom animation support (focus pulse)
4. No backend dependency
5. Active maintenance (updated in 2024+)

**Recommendation**: **driver.js** (KISS + lightweight)

---

## DEFERRED SCOPE (Phase 5+)

- ❌ Video tutorials (defer to external YouTube links)
- ❌ Multi-language support (English only Phase 4)
- ❌ Analytics tracking (which steps users skip)
- ❌ Tutorials for other modules (Sales, CRM, Accounting)
- ❌ AI-powered adaptive tutorials (adjust based on user behavior)

---

## ACCEPTANCE VALIDATION

**Demo Script** (for user approval):
1. Start app → Navigate to Purchase module
2. Tutorial auto-starts with welcome popup
3. Click "Next" → Focuses on "New Requisition" button (zoom in animation)
4. Click "Next" → Focuses on form fields (item, quantity)
5. Continue through 15-20 steps (full workflow)
6. Click "Complete Tutorial" → Badge appears
7. Reload page → Tutorial does not restart
8. Click "Restart Tutorial" (in settings) → Starts from step 1

**User Feedback Checkpoints**:
- ✅ Animation speed acceptable? (300ms)
- ✅ Text clarity (≤20 words per popup)?
- ✅ Focus visibility (shadow, pulse)?
- ✅ "Next" button easy to find?

---

## EFFORT ESTIMATION

**Implementation**:
- Research library (driver.js vs react-joyride): 1h
- TutorialOverlay component: 3h
- Step definitions (purchaseTutorialSteps.js): 2h
- Focus animation (CSS + transitions): 2h
- Integration with PurchaseLayout: 1h
- Unit tests: 2h
- E2E validation (Playwright MCP): 2h
- Documentation (SPR update): 1h

**Total**: ~14h (2 days)

**Dependencies**: None (pure frontend, no backend changes)

---

## DOCUMENTATION UPDATES

**Files to Update**:
1. `CONTINUE_HERE.spr.md`: Add "Tutorial system Phase 4" to current state
2. `frontend/DESIGN_SYSTEM.spr.md`: Add TutorialOverlay component pattern
3. `docs/testing/suites/E2E_PURCHASE.spr.md`: Add tutorial validation workflow
4. `docs/PATTERNS_LEARNED.spr.md`: Add pattern (if driver.js integration novel)

**Session Log**: Create only if >2h debugging or architecture decision

---

## CRITICAL LENS VALIDATION

**Universal Invariant?** ⚠️ **CONDITIONAL**
- Tutorial UX pattern = universal (onboarding best practice)
- Purchase workflow specific = domain-specific
- Low-tech users = target persona constraint

**KISS Principle**:
- ✅ Use existing library (driver.js) vs custom implementation
- ✅ Pure frontend (no backend tutorial tracking Phase 4)
- ✅ Local storage (simple, no DB persistence)
- ✅ Desktop-first (mobile deferred)

**DDD Alignment**:
- ✅ No domain logic changes (pure UI/UX layer)
- ✅ No entity modifications
- ✅ Infrastructure layer untouched

**Verdict**: ✅ **ACCEPT** (with library dependency evaluation first)

---

## NAVIGATION REFERENCES

**Similar Patterns**:
- Form validation tooltips: `frontend/src/components/common/FormField.jsx`
- Focus management: `frontend/src/components/sales/ProductCatalog.jsx` (search focus)
- Animation: `frontend/src/styles/tokens.css` (transition variables)

**Research Required**:
- Deepwiki: `mcp_deepwiki_ask_question --repoName "kamranahmedse/driver.js" --question "Custom animation hooks and focus management"`
- Deepwiki: `mcp_deepwiki_ask_question --repoName "gilbarbara/react-joyride" --question "Accessibility ARIA support and keyboard navigation"`

**E2E Protocol**: `docs/testing/protocols/PLAYWRIGHT_MCP.md`

---

## NEXT STEPS (AGENT PROTOCOL)

1. **Research Phase** (1h):
   - Deepwiki queries (driver.js, react-joyride)
   - Evaluate bundle size, accessibility, customization
   - Decision: driver.js vs react-joyride vs custom
   
2. **Design Phase** (2h):
   - Create step definitions (purchaseTutorialSteps.js)
   - Mock TutorialOverlay component structure
   - CSS animation keyframes
   
3. **Implementation Phase** (6h):
   - Install library (uv for any Python deps, npm for frontend)
   - Build TutorialOverlay + FocusZone components
   - Integrate with PurchaseLayout
   
4. **Testing Phase** (4h):
   - Unit tests (Jest + React Testing Library)
   - E2E validation (Playwright MCP manual protocol)
   
5. **Documentation Phase** (1h):
   - Update CONTINUE_HERE, DESIGN_SYSTEM, E2E_PURCHASE
   - Append PATTERNS_LEARNED if novel pattern

**Total**: 14h (ready for Phase 4 implementation)

---

**END OF REQUIREMENT**
