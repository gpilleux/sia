# Q1: Library Research

## Metadata

**Quant ID**: Q1  
**Horas**: 1h  
**Estado**: 🔴 Pending  
**Dependencias**: Ninguna  

---

## Objetivo

Evaluar y seleccionar librería de tour/tutorial para React.

---

## Candidatos

| Librería | Bundle Size | Accesibilidad | Animación Custom | Mantenimiento |
|----------|-------------|---------------|------------------|---------------|
| driver.js | 5KB gzip | ✅ ARIA | ✅ CSS hooks | ✅ 2024 |
| react-joyride | 11KB gzip | ✅ ARIA | ⚠️ Limited | ✅ 2024 |
| intro.js | 10KB gzip | ⚠️ Partial | ✅ Full | ✅ 2024 |

---

## Research Queries

```bash
# Deepwiki research commands
mcp_deepwiki_ask_question --repoName "kamranahmedse/driver.js" \
  --question "Custom highlight animation and focus pulse effect"

mcp_deepwiki_ask_question --repoName "gilbarbara/react-joyride" \
  --question "Accessibility ARIA labels and keyboard navigation support"
```

---

## Decision Criteria (KISS)

1. **Bundle size**: <10KB (driver.js wins)
2. **Accessibility**: ARIA + keyboard required
3. **Custom animation**: Focus pulse (scale + shadow)
4. **React integration**: Hook-based preferred
5. **Learning curve**: <30min to implement basic tour

---

## Output Esperado

- [ ] Librería seleccionada
- [ ] Justificación documentada
- [ ] POC básico (3 steps) funcionando
- [ ] Actualizar README.md con decisión

---

## Acceptance Criteria

- [ ] POC con 3 pasos funcionando
- [ ] Animación de focus visible
- [ ] Popup con texto posicionado
- [ ] Keyboard navigation verificado
