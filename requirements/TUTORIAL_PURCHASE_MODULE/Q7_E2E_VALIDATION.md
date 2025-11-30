# Q7: E2E Validation

## Metadata

**Quant ID**: Q7  
**Horas**: 2h  
**Estado**: 🔴 Pending  
**Dependencias**: Q5 (Integration complete)  

---

## Objetivo

Validación E2E usando Playwright MCP (protocolo manual).

---

## Protocol Reference

See: `docs/testing/protocols/PLAYWRIGHT_MCP.md`

---

## Test Scenarios

### Scenario 1: First Visit Auto-Start

**Steps**:
1. Clear localStorage (`localStorage.clear()`)
2. Navigate to `/purchase/requisitions`
3. Wait 500ms (tutorial delay)
4. **Verify**: Tutorial overlay visible
5. **Verify**: Step 1 popup ("Requisitions Menu")
6. **Verify**: Dimmed background visible
7. **Verify**: Focus highlight on nav element

**Expected**: Tutorial auto-starts on first visit

---

### Scenario 2: Complete Tutorial Flow

**Steps**:
1. Start fresh (localStorage cleared)
2. Navigate to `/purchase`
3. Click "Next" → Verify Step 2 visible
4. Click "Next" → Verify Step 3 visible
5. Continue clicking "Next" through all 20 steps
6. On last step, click "Complete"
7. **Verify**: Tutorial dismissed
8. **Verify**: `localStorage.tutorial_purchase_completed === 'true'`

**Expected**: Full flow completes without errors

---

### Scenario 3: Skip Tutorial

**Steps**:
1. Start fresh
2. Navigate to `/purchase`
3. Click "Skip Tutorial" button
4. **Verify**: Tutorial dismissed
5. **Verify**: localStorage step saved (for resume)
6. Reload page
7. **Verify**: Tutorial does NOT restart (skip respected)

**Expected**: Skip saves state, doesn't restart

---

### Scenario 4: Keyboard Navigation

**Steps**:
1. Start tutorial
2. Press `ArrowRight` → Verify next step
3. Press `ArrowLeft` → Verify previous step
4. Press `Escape` → Verify tutorial skipped
5. Press `Tab` → Verify focus moves to controls
6. Press `Enter` on "Next" → Verify advances

**Expected**: All keyboard shortcuts work

---

### Scenario 5: Resume After Refresh

**Steps**:
1. Start tutorial at step 1
2. Click "Next" 5 times (reach step 6)
3. Reload page (F5)
4. **Verify**: Tutorial resumes at step 6
5. **Verify**: Progress bar shows correct position

**Expected**: State persists across refresh

---

### Scenario 6: Restart Tutorial

**Steps**:
1. Complete tutorial (localStorage flag set)
2. Navigate to `/purchase`
3. **Verify**: Tutorial does NOT start
4. Click "Restart Tutorial" button (in header/settings)
5. **Verify**: Tutorial starts from step 1
6. **Verify**: localStorage cleared

**Expected**: Restart works after completion

---

### Scenario 7: Missing Target Handling

**Steps**:
1. Manually remove a target element from DOM
2. Advance tutorial to that step
3. **Verify**: Console warning logged
4. **Verify**: Tutorial skips to next valid step
5. **Verify**: No crash or infinite loop

**Expected**: Graceful degradation

---

### Scenario 8: Responsive Behavior

**Steps**:
1. Set viewport to desktop (1280px)
2. Start tutorial → Verify popup positions correctly
3. Resize to tablet (768px)
4. **Verify**: Popup repositions (no overflow)
5. Resize to mobile (375px)
6. **Verify**: Tutorial shows simplified view OR text guide

**Expected**: Responsive layout maintained

---

## Playwright Commands (MCP Protocol)

```javascript
// Using Playwright MCP tools

// Navigate
mcp_playwright_browser_navigate({ url: 'http://localhost:5173/purchase/requisitions' });

// Take snapshot (accessibility tree)
mcp_playwright_browser_snapshot();

// Click Next button
mcp_playwright_browser_click({ element: 'Next button', ref: '[data-testid="tutorial-next-btn"]' });

// Type in field (if needed)
mcp_playwright_browser_type({ element: 'Input field', ref: 'input[name="field"]', text: 'value' });

// Press key
mcp_playwright_browser_press_key({ key: 'ArrowRight' });
mcp_playwright_browser_press_key({ key: 'Escape' });

// Evaluate localStorage
mcp_playwright_browser_evaluate({ 
  function: '() => localStorage.getItem("tutorial_purchase_completed")' 
});

// Clear localStorage
mcp_playwright_browser_evaluate({ 
  function: '() => localStorage.clear()' 
});

// Resize viewport
mcp_playwright_browser_resize({ width: 768, height: 1024 });

// Screenshot for validation
mcp_playwright_browser_take_screenshot({ filename: 'tutorial-step-1.png' });
```

---

## Validation Checklist

### Visual Checks

- [ ] Focus highlight visible (zoom effect)
- [ ] Pulse animation running (subtle scale)
- [ ] Popup positioned correctly (not off-screen)
- [ ] Arrow points to target element
- [ ] Background dimmed (blur + opacity)
- [ ] Progress bar shows correct step

### Functional Checks

- [ ] Auto-start on first visit
- [ ] Next/Previous navigation works
- [ ] Skip dismisses tutorial
- [ ] Complete sets localStorage flag
- [ ] Keyboard shortcuts functional
- [ ] State persists on refresh
- [ ] Restart clears and begins fresh

### Accessibility Checks

- [ ] ARIA labels present on controls
- [ ] Focus trap within tutorial
- [ ] Tab order logical
- [ ] Screen reader announces step changes
- [ ] High contrast mode visible

### Performance Checks

- [ ] Animation smooth (60 FPS)
- [ ] No layout shift on step change
- [ ] Tutorial loads < 100ms
- [ ] No memory leaks (check DevTools)

---

## Bug Report Template

```markdown
### Bug: [Title]

**Scenario**: [Which test scenario]
**Step**: [At which step in the scenario]
**Expected**: [What should happen]
**Actual**: [What actually happened]
**Screenshot**: [If applicable]
**Console**: [Any errors]
```

---

## Acceptance Criteria

- [ ] All 8 scenarios pass
- [ ] No console errors
- [ ] Visual checks confirmed
- [ ] Accessibility audit passed
- [ ] Performance metrics met
- [ ] Screenshots documented
