# Q2: Step Definitions

## Metadata

**Quant ID**: Q2  
**Horas**: 2h  
**Estado**: 🔴 Pending  
**Dependencias**: Q1 (library selected)  

---

## Objetivo

Definir todos los pasos del tutorial siguiendo el flujo de compras.

---

## Output File

`frontend/src/data/purchaseTutorialSteps.js`

---

## Schema por Step

```javascript
{
  id: string,              // 'step-1-create-requisition'
  target: string,          // CSS selector or data-testid
  title: string,           // Max 5 words
  description: string,     // Max 20 words
  position: 'top' | 'bottom' | 'left' | 'right',
  action: 'click' | 'input' | 'observe',
  waitFor?: string,        // Optional: selector to wait for
}
```

---

## Steps por Workflow

### 1. Requisition Flow (Steps 1-5)

| Step | Target | Title | Description |
|------|--------|-------|-------------|
| 1 | `[data-testid="nav-requisitions"]` | Requisitions Menu | Access purchase requests here |
| 2 | `[data-testid="new-requisition-btn"]` | New Requisition | Click to create purchase request |
| 3 | `[data-testid="requisition-item-field"]` | Item Field | Enter what you need to buy |
| 4 | `[data-testid="requisition-quantity-field"]` | Quantity | How many items needed |
| 5 | `[data-testid="requisition-submit-btn"]` | Submit | Send request for approval |

### 2. Approval Flow (Steps 6-7)

| Step | Target | Title | Description |
|------|--------|-------|-------------|
| 6 | `.requisition-row.pending` | Pending Request | Manager reviews this request |
| 7 | `[data-testid="approve-btn"]` | Approve | Click to approve the request |

### 3. RFQ Flow (Steps 8-12)

| Step | Target | Title | Description |
|------|--------|-------|-------------|
| 8 | `[data-testid="create-rfq-btn"]` | Create RFQ | Request quotes from suppliers |
| 9 | `[data-testid="rfq-supplier-select"]` | Select Suppliers | Choose who to ask for quotes |
| 10 | `[data-testid="rfq-due-date"]` | Due Date | When you need responses |
| 11 | `[data-testid="send-rfq-btn"]` | Send RFQ | Send to selected suppliers |
| 12 | `[data-testid="add-quote-btn"]` | Add Quote | Suppliers submit their prices |

### 4. Quote Evaluation (Steps 13-14)

| Step | Target | Title | Description |
|------|--------|-------|-------------|
| 13 | `.quote-row` | Quote Received | Review supplier offers |
| 14 | `[data-testid="accept-quote-btn"]` | Accept Quote | Choose best supplier |

### 5. PO Flow (Steps 15-18)

| Step | Target | Title | Description |
|------|--------|-------|-------------|
| 15 | `[data-testid="create-po-btn"]` | Create PO | Generate purchase order |
| 16 | `[data-testid="po-terms-field"]` | Terms | Payment and delivery terms |
| 17 | `[data-testid="po-submit-btn"]` | Submit PO | Send for approval |
| 18 | `[data-testid="po-approve-btn"]` | Approve PO | Final approval before sending |

### 6. Receipt Flow (Steps 19-20)

| Step | Target | Title | Description |
|------|--------|-------|-------------|
| 19 | `.po-row.approved` | Approved PO | Ready for supplier |
| 20 | `[data-testid="mark-received-btn"]` | Mark Received | Confirm items delivered |

---

## data-testid Required

Asegurar que existen en componentes:

```javascript
// Components que necesitan data-testid
- RequisitionList.jsx
- RequisitionForm.jsx
- RFQList.jsx
- RFQForm.jsx
- QuoteList.jsx
- PurchaseOrderList.jsx
- PurchaseOrderForm.jsx
```

---

## Acceptance Criteria

- [ ] 20 steps definidos en archivo JS
- [ ] Todos los targets existen en DOM
- [ ] Descriptions ≤20 palabras
- [ ] data-testid agregados donde faltan
