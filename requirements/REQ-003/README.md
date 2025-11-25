# REQ-003: Dynamic UI Rendering System

Sistema de renderizado dinámico de UI integrado con MCP-UI para transformar Argus en una plataforma de Document Intelligence visual e interactiva.

---

## 📂 Estructura de Archivos

```
REQ-003/
├── README.md                      # Este archivo (navegación)
├── EXECUTIVE_SUMMARY.md           # Resumen ejecutivo + checklist
├── REQ-003.md                     # Especificación formal del requirement
├── REQ-003_domain_analysis.md     # Investigación ADK + MCP-UI + arquitectura
└── REQ-003_quant_breakdown.md     # 18 tareas atómicas (4 ADK + 14 MCP-UI) con código
```

---

## 🚀 Quick Start

### 1. Leer Contexto
```bash
# Resumen ejecutivo (5 min)
cat EXECUTIVE_SUMMARY.md

# Especificación completa (15 min)
cat REQ-003.md
```

### 2. Revisar Investigación
```bash
# Análisis de MCP-UI (20 min)
cat REQ-003_domain_analysis.md
```

### 3. Implementar Tareas
```bash
# Ver tareas QUANT (10 min)
cat REQ-003_quant_breakdown.md

# Ejecutar primera tarea
# QUANT-032: Install Dependencies
cd backend && uv add mcp-ui-server
cd frontend && npm install @mcp-ui/client
```

---

## 📊 Estado Actual

**Status**: ✅ READY FOR EXECUTION  
**Progress**: 0/14 QUANT tasks completed  
**Phase**: Foundation (Week 1)  
**Next Task**: QUANT-032 (Install Dependencies)

---

## 🎯 Objetivos Clave

1. **Dashboard Basal**: Dashboard automático al entrar a la plataforma
2. **Chat Dinámico**: Respuestas del chatbot insertan visualizaciones
3. **MCP-UI Integration**: Backend genera UIResource, frontend renderiza

---

## 🧩 Componentes Principales

### Backend (Python)
- `domain/value_objects/ui_resource.py`: UIResource, UIAction models
- `infrastructure/visualization/ui_resource_factory.py`: Factory para crear UIResources
- `infrastructure/visualization/chart_generators.py`: Generadores de HTML (recharts)
- `infrastructure/visualization/table_generators.py`: Generadores de tablas (TailwindCSS)
- `api/v1/dashboard.py`: Endpoint GET /dashboard

### Frontend (React/Next.js)
- `types/ui-resource.ts`: TypeScript types
- `components/ui-resource/UIResourceRenderer.tsx`: Wrapper de @mcp-ui/client
- `app/dashboard/page.tsx`: Página de dashboard
- `components/chat/MessageRenderer.tsx`: Renderizador de mensajes con UIResources

---

## 📝 QUANT Tasks Overview

| ID        | Task                      | Status    | Time | Dependencies |
| --------- | ------------------------- | --------- | ---- | ------------ |
| QUANT-032 | Install Dependencies      | ⏳ Pending | 1h   | -            |
| QUANT-033 | UIResource Infrastructure | ⏳ Pending | 2h   | 032          |
| QUANT-034 | Chart Generators          | ⏳ Pending | 4h   | 033          |
| QUANT-035 | UIResourceRenderer        | ⏳ Pending | 2h   | 033          |
| QUANT-036 | Dashboard Endpoint        | ⏳ Pending | 3h   | 034          |
| QUANT-037 | Dashboard View            | ⏳ Pending | 2h   | 035, 036     |
| QUANT-038 | Dashboard Generators      | ⏳ Pending | 3h   | 036          |
| QUANT-039 | SSE UIResource Events     | ⏳ Pending | 4h   | 034          |
| QUANT-040 | Chat Message Renderer     | ⏳ Pending | 3h   | 035          |
| QUANT-041 | Bidirectional Comm        | ⏳ Pending | 4h   | 040          |
| QUANT-042 | Visualization Mapping     | ⏳ Pending | 3h   | 039          |
| QUANT-043 | Responsive Design         | ⏳ Pending | 3h   | 038, 042     |
| QUANT-044 | Error Handling            | ⏳ Pending | 4h   | 043          |
| QUANT-045 | Performance Optimization  | ⏳ Pending | 5h   | 044          |

**Total**: 43 hours (~1 week focused work)

---

## 🔗 Links Útiles

### Documentación Externa
- [MCP-UI GitHub](https://github.com/MCP-UI-Org/mcp-ui)
- [MCP-UI Docs](https://mcpui.dev)
- [Recharts](https://recharts.org/en-US/examples)
- [TailwindCSS](https://tailwindcss.com/docs)

### Investigación Realizada
- DeepWiki Query 1: [MCP-UI Overview](https://deepwiki.com/search/what-is-mcpui-and-what-are-its_1c7a37ab-53d8-4be0-b6d0-3ae340a80e4d)
- DeepWiki Query 2: [React Client SDK](https://deepwiki.com/search/how-does-the-react-client-sdk_16753f28-da1a-4051-b191-49e0fb96495d)
- DeepWiki Query 3: [Python Server SDK](https://deepwiki.com/search/how-does-the-python-server-sdk_e2377be7-19cc-49a7-81bd-eeddc595f217)

### Código de Referencia
- [MCP-UI Examples](https://github.com/MCP-UI-Org/mcp-ui/tree/main/examples)
- [Cloudflare Worker Example](https://github.com/MCP-UI-Org/mcp-ui/tree/main/examples/cloudflare-worker-server)

---

## 🧪 Testing Strategy

### Unit Tests
```bash
# Backend
cd backend
uv run pytest tests/infrastructure/test_ui_resource_factory.py
uv run pytest tests/infrastructure/test_chart_generators.py

# Frontend
cd frontend
npm test -- UIResourceRenderer.test.tsx
```

### Integration Tests
```bash
# Backend API
uv run pytest tests/api/test_dashboard_endpoint.py

# Frontend
npm test -- dashboard.test.tsx
```

### E2E Tests (Playwright)
```bash
cd frontend
npx playwright test e2e/dashboard.spec.ts
npx playwright test e2e/chat-visualization.spec.ts
```

---

## 📈 Progress Tracking

### Week 1: Foundation + Dashboard
- [ ] Day 1-2: QUANT-032 to QUANT-035
- [ ] Day 3-4: QUANT-036 to QUANT-038
- [ ] Day 5: Testing + Documentation
- [ ] **Gate 1**: Dashboard MVP working

### Week 2: Chat Integration
- [ ] Day 1-2: QUANT-039 to QUANT-040
- [ ] Day 3: QUANT-041
- [ ] Day 4: QUANT-042
- [ ] Day 5: Integration Testing
- [ ] **Gate 2**: Chat visualizations working

### Week 3: Polish
- [ ] Day 1: QUANT-043
- [ ] Day 2: QUANT-044
- [ ] Day 3: QUANT-045
- [ ] Day 4-5: Final Testing + Documentation
- [ ] **Gate 3**: Production ready

---

## 🎓 Knowledge Base

### MCP-UI Core Concepts

**UIResource**: JSON object con contenido HTML/URL para renderizar
```python
{
  "uri": "ui://argus/chart/bar",
  "mimeType": "text/html",
  "text": "<html>...</html>"
}
```

**UIAction**: Comando enviado desde iframe a host
```typescript
{
  type: "tool",
  payload: { toolName: "get_data", params: {...} }
}
```

**Security**: Todo se renderiza en sandboxed iframes (XSS prevention)

### Architecture Patterns

**Factory Pattern**: `UIResourceFactory` crea UIResources
```python
factory = UIResourceFactory()
resource = factory.create_html_resource(uri, html)
```

**Strategy Pattern**: Diferentes generadores para cada tipo de viz
```python
ChartGenerators.generate_bar_chart_html(data)
TableGenerators.generate_statistics_table_html(headers, rows)
```

**Observer Pattern**: SSE para notificar nuevas UIResources
```typescript
eventSource.addEventListener('ui_resource', (event) => {
  const resource = JSON.parse(event.data);
  renderUIResource(resource);
});
```

---

## 🐛 Troubleshooting

### Problema: Iframe no renderiza
**Solución**: Verificar CSP headers, asegurar `frame-src 'self' blob:`

### Problema: postMessage no funciona
**Solución**: Verificar `window.parent.postMessage(...)` en iframe

### Problema: Recharts no se carga
**Solución**: Verificar CDN accesible, implementar fallback local

---

## 📞 Contacto

**Super Agent**: SIA Framework  
**Requirement Owner**: System Architect  
**Created**: 2025-11-24  
**Last Updated**: 2025-11-24

---

**NEXT STEP**: Ejecutar QUANT-032 (Install Dependencies)
