Este é o relatório de problemas de frontend do projeto, quero que resolva todos os problemas:

Auditoria Frontend — AIBE v2.0
Resumo Executivo
O frontend do AIBE existe em dois formatos paralelos e desconectados: um arquivo index.html monolítico com CSS/JS inline (~965 linhas) servido via Nginx, e um scaffold Next.js 15 praticamente vazio (apenas layout.tsx, providers.tsx, e utilitários — sem nenhuma página renderizável). O resultado é que o dashboard funcional é o HTML estático, enquanto o Next.js é uma casca sem conteúdo. A auditoria abaixo cobre ambos.

1. Problemas Técnicos e de Arquitetura
[CRÍTICO] Dois frontends sem convergência — investimento disperso
Onde: Dockerfile.frontend, index.html, aibe/ui/frontend/src/
O Problema: O Dockerfile.frontend copia apenas index.html para o Nginx e expõe na porta 3000. O projeto Next.js (com layout.tsx, stores, etc.) nunca é construído nem servido. Não há page.tsx em src/app/, logo o Next.js não renderiza absolutamente nada. O docker-compose.yml monta o frontend como build do Dockerfile.frontend, ou seja, só serve o HTML estático. Todo o investimento em Zustand, React Query, Tailwind config, e tipagem TypeScript está ocioso.
A Solução: Escolher um caminho e seguir. Dado o nível de investimento em Next.js (tipos, stores, API client), o caminho correto é:

1. Criar src/app/page.tsx como ponto de entrada real.
2. Atualizar o Dockerfile.frontend para fazer npm run build do Next.js e servir via standalone output.
3. Mover o index.html para uma rota de fallback ou descartá-lo.

dockerfileDownloadCopy code# Dockerfile.frontend corrigido
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 3000
CMD ["node", "server.js"]

[CRÍTICO] WebSocket store reconecta indefinidamente sem backoff exponencial
Onde: src/stores/ws-store.ts
O Problema: Na linha ws.onclose, o timer de reconexão é fixo em 3000ms. Em caso de servidor inativo prolongado, isso gera milhares de tentativas de conexão por hora, consumindo recursos do browser e potencialmente causando problemas de rate-limiting. Na onerror, não há tentativa de reconexão (o socket simplesmente para). Além disso, o reconnectTimer nunca é limpo antes de criar um novo, o que pode causar timers duplicados se onclose e onerror forem disparados em sequência rápida.
A Solução:
typescriptDownloadCopy code// ws-store.ts — reconexão com backoff exponencial
let reconnectAttempt = 0;
const MAX_RECONNECT_DELAY = 30_000;

function doConnect() {
  const url = /* ... */;
  try {
    ws = new WebSocket(url);
    ws.onopen = () => {
      reconnectAttempt = 0; // Reset on success
      set({ connected: true });
      ws?.send(JSON.stringify({ type: "subscribe", topics: ["*"] }));
    };
    ws.onclose = () => {
      set({ connected: false });
      if (reconnectTimer) clearTimeout(reconnectTimer);
      const delay = Math.min(1000 * 2 ** reconnectAttempt, MAX_RECONNECT_DELAY);
      reconnectAttempt++;
      reconnectTimer = setTimeout(doConnect, delay);
    };
    ws.onerror = () => {
      set({ connected: false });
      ws?.close(); // Triggers onclose which handles reconnection
    };
  } catch {
    set({ connected: false });
    if (reconnectTimer) clearTimeout(reconnectTimer);
    const delay = Math.min(1000 * 2 ** reconnectAttempt, MAX_RECONNECT_DELAY);
    reconnectAttempt++;
    reconnectTimer = setTimeout(doConnect, delay);
  }
}

[CRÍTICO] index.html — dados simulados mascaram problemas reais
Onde: index.html, linhas 952-962
O Problema: O heartbeat simulado via setInterval a cada 5 segundos injeta eventos falsos no feed. Isso significa que em produção, o dashboard parecerá "vivo" mesmo se o WebSocket nunca conectar e nenhum agente estiver realmente rodando. Isso viola um princípio fundamental de observabilidade: o dashboard deve refletir o estado real do sistema, não uma simulação.
A Solução: Remover o heartbeat simulado inteiramente. Adicionar um indicador visual claro de "sem dados" quando o WebSocket não está conectado ou quando nenhum evento real foi recebido:
javascriptDownloadCopy code// Remover este bloco inteiro:
// setInterval(() => { ... addEvent({ type: 'heartbeat', ... }) }, 5000);

// Substituir por verificação de dados reais:
let lastEventTime = 0;
setInterval(() => {
  if (Date.now() - lastEventTime > 60000) {
    document.getElementById('system-status').textContent = 'No Data';
    document.querySelector('.status-dot').style.background = '#f59e0b';
  }
}, 10000);

[CRÍTICO] api.ts — sem tratamento de erro granular e sem tipagem de erros
Onde: src/lib/api.ts
O Problema: A função fetcher faz throw new Error(...) com apenas o status code, descartando o corpo da resposta de erro que o backend retorna (e.g., {"detail": "Agent not found: xyz"}). Não há interceptor para erros 401/403 (redirecionar para login), 429 (rate limit), ou 500 (retry). Cada chamada à API requer que o consumidor faça seu próprio try/catch, sem nenhum padrão centralizado.
A Solução:
typescriptDownloadCopy codeclass ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public body: unknown,
  ) {
    super(`${status} ${statusText}`);
    this.name = "ApiError";
  }
}

async function fetcher<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!res.ok) {
    let body: unknown;
    try { body = await res.json(); } catch { body = null; }
    throw new ApiError(res.status, res.statusText, body);
  }
  return res.json();
}

[MODERADO] package.json — dependências sem lock file e sem versionamento preciso
Onde: aibe/ui/frontend/package.json
O Problema: Não há package-lock.json ou equivalente no repositório. As dependências usam ranges semver (^), o que significa que npm install em datas diferentes produz builds diferentes. Além disso, react, react-dom, e next não estão listados como dependências — presumivelmente são gerenciados pelo Next.js, mas isso precisa ser explícito. O @react-three/fiber e three estão listados mas não são usados em nenhum componente existente, adicionando peso morto ao bundle.
A Solução: Adicionar next, react, e react-dom explicitamente. Remover Three.js até que o Epic G (3D Virtual Office) seja implementado. Gerar e committar o package-lock.json.

[MODERADO] providers.tsx — connect() chamado sem cleanup no unmount
Onde: src/components/providers.tsx
O Problema: O useEffect chama connect() mas não retorna uma função de cleanup que chame disconnect(). Em desenvolvimento com React Strict Mode (habilitado no next.config.ts via reactStrictMode: true), o efeito roda duas vezes, criando duas conexões WebSocket. Em produção, se o componente Providers for remontado, a conexão anterior fica órfã.
A Solução:
typescriptDownloadCopy code"use client";
import { useEffect } from "react";
import { useWsStore } from "@/stores/ws-store";

export function Providers({ children }: { children: React.ReactNode }) {
  const connect = useWsStore((s) => s.connect);
  const disconnect = useWsStore((s) => s.disconnect);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return <>{children}</>;
}

[MODERADO] ws-store.ts — acúmulo ilimitado de eventos em memória
Onde: src/stores/ws-store.ts, linha 33
O Problema: Os eventos são limitados a 200 (slice(0, 200)), o que é razoável, mas o agentStatuses cresce indefinidamente — um mapa de status para cada agent_id já visto. Se houver agentes removidos ou renomeados, seus status permanecem. Mais importante, cada mensagem system_heartbeat faz Object.assign(agentStatuses, evt.data.statuses), que copia todos os status de todos os agentes, criando um novo objeto a cada heartbeat (a cada ~30s). Isso dispara re-renders desnecessários em todos os componentes que consomem agentStatuses, mesmo que nenhum status tenha mudado.
A Solução: Fazer comparação shallow antes de atualizar:
typescriptDownloadCopy codeif (evt.event === "system_heartbeat" && evt.data.statuses) {
  const incoming = evt.data.statuses as Record<string, string>;
  const current = s.agentStatuses;
  const hasChanges = Object.entries(incoming).some(
    ([id, status]) => current[id] !== status
  );
  if (hasChanges) {
    Object.assign(agentStatuses, incoming);
  }
}

[MODERADO] index.html — XSS potencial via dados do WebSocket
Onde: index.html, função addEvent(), linhas 846-853
O Problema: Os campos event.title e event.detail são interpolados diretamente no innerHTML sem sanitização. Se o backend (ou um atacante que consiga publicar no NATS) enviar um evento com title: "<img src=x onerror=alert(1)>", o código será executado no browser do operador.
A Solução: Sanitizar toda entrada antes de inserir no DOM:
javascriptDownloadCopy codefunction escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str || '';
  return div.innerHTML;
}

// Na função addEvent:
el.innerHTML = `
  <div class="event-icon" style="background: ${config.bg}">${config.icon}</div>
  <div class="event-content">
    <div class="event-title">${escapeHtml(event.title || event.type)}</div>
    <div class="event-detail">${escapeHtml(event.detail || '')}</div>
  </div>
  <div class="event-time">${time}</div>
`;

[MODERADO] tailwind.config.ts — plugin tailwindcss-animate referenciado mas possivelmente não instalado
Onde: tailwind.config.ts, linha 97
O Problema: A linha plugins: [require("tailwindcss-animate")] referencia um pacote que não está listado em package.json. Isso causa um erro silencioso ou crash durante o build do Tailwind, impedindo que qualquer animação definida no config funcione.
A Solução: Adicionar ao package.json:
jsonDownloadCopy code"devDependencies": {
  "tailwindcss-animate": "^1.0.7",
  // ...
}

[MODERADO] next.config.ts — rewrites proxy sem timeout nem error handling
Onde: next.config.ts
O Problema: O rewrite de /api/:path* para o backend não tem timeout configurado. Se o backend demorar, o Next.js ficará pendurado indefinidamente. Além disso, em produção, o NEXT_PUBLIC_API_URL pode não estar definido, fazendo o proxy apontar para http://localhost:8000 — o que falha silenciosamente em ambientes containerizados onde o backend roda em outro host.
A Solução: Para produção, o proxy deve ser feito pelo Nginx (já existe na infra), não pelo Next.js. Limitar o rewrite apenas ao desenvolvimento:
typescriptDownloadCopy codeasync rewrites() {
  if (process.env.NODE_ENV === "development") {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/:path*`,
      },
    ];
  }
  return [];
},

[SUGESTÃO] agents-data.ts — dados estáticos duplicam agents.yaml do backend
Onde: src/lib/agents-data.ts
O Problema: A lista de 41 agentes com tiers, nomes e roles está hardcoded no frontend. Qualquer alteração no backend (adicionar agente, mudar tier, renomear) requer atualização manual sincronizada. Isso é uma fonte inevitável de inconsistências.
A Solução: Consumir a lista de agentes via API (GET /api/agents) e usar agents-data.ts apenas como fallback para renderização durante o loading. Alternativa: gerar agents-data.ts automaticamente a partir de agents.yaml via script de build.

[SUGESTÃO] Ausência de error boundaries
Onde: src/app/layout.tsx
O Problema: Não há React Error Boundary em nenhum nível. Se qualquer componente filho lançar um erro durante render, toda a aplicação crasha com uma tela branca. Dado que o dashboard consome dados em tempo real de múltiplas fontes instáveis (WebSocket, API), erros de runtime são inevitáveis.
A Solução: Adicionar um error boundary no layout:
typescriptDownloadCopy code// src/components/error-boundary.tsx
"use client";
import { Component, type ReactNode } from "react";

interface Props { children: ReactNode; fallback?: ReactNode }
interface State { hasError: boolean; error?: Error }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }
  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="flex items-center justify-center h-screen text-red-400">
          <p>Something went wrong. Check console for details.</p>
        </div>
      );
    }
    return this.props.children;
  }
}

2. Melhorias de Design e UI/UX
[CRÍTICO] Acessibilidade (a11y) — ausência quase total
Onde: index.html inteiro, layout.tsx
O Problema:

* Zero uso de role, aria-label, aria-live, ou aria-describedby em qualquer elemento interativo.
* Os cards de agente são clicáveis (via onclick) mas são <div>, não <button> ou <a> — impossíveis de navegar por teclado.
* O feed de eventos usa aria-live zero — leitores de tela não sabem que novos eventos chegaram.
* O contraste de cor --text-muted: #5c5c72 sobre --bg-primary: #0a0a0f tem ratio de ~3.2:1, abaixo do mínimo WCAG AA de 4.5:1.
* Status é comunicado apenas por cor (dot verde/amarelo/vermelho) sem alternativa textual.

A Solução: No mínimo:
htmlDownloadCopy code<!-- Agent cards devem ser buttons -->
<button class="agent-card" onclick="selectAgent('${agent.id}')"
        aria-label="${agent.name} - ${agent.role} - Status: ${status}">
  <!-- ... -->
</button>

<!-- Event feed deve ser live region -->
<div class="event-feed" id="event-feed" 
     role="log" aria-live="polite" aria-label="Live system events">

<!-- Status dots precisam de texto alternativo -->
<span class="agent-status-dot status-${status}" 
      role="status" aria-label="Status: ${status}"></span>
Para o contraste, ajustar --text-muted para #8888a0 (~4.7:1 ratio).

[MODERADO] Responsividade — layout quebra em telas estreitas
Onde: index.html, CSS
O Problema: O .main-grid usa grid-template-columns: 1fr 380px com media query em 1024px. Mas entre 768px e 1024px, a coluna de 380px espreme a coluna principal a ponto de os cards de agente (min-width 200px) não caberem. O .kpi-strip usa repeat(auto-fit, minmax(220px, 1fr)) que funciona razoavelmente, mas em mobile (<400px), os KPI cards não têm padding lateral suficiente e encostam nas bordas.
A Solução: Adicionar breakpoint intermediário e padding:
cssDownloadCopy code@media (max-width: 768px) {
  .container { padding: 0 12px; }
  .kpi-strip { gap: 10px; }
  .kpi-card { padding: 14px; }
  .agent-grid { grid-template-columns: 1fr; }
}

@media (min-width: 768px) and (max-width: 1024px) {
  .main-grid { grid-template-columns: 1fr 320px; }
}

[MODERADO] Ausência de loading states e feedback visual
Onde: index.html, funções refreshAgents() e refreshCosts()
O Problema: Quando o usuário clica "Refresh" ou quando o fetch periódico roda, não há nenhum indicador visual de loading. Se a API demorar 5 segundos, o usuário não sabe se algo está acontecendo. Se falhar, não há feedback — a interface simplesmente não atualiza.
A Solução:
javascriptDownloadCopy codeasync function refreshAgents() {
  const btn = document.querySelector('#agent-fleet').closest('.panel').querySelector('.btn');
  btn.disabled = true;
  btn.textContent = '↻ Loading...';
  try {
    const data = await fetchData('/agents');
    if (data && data.agents) {
      data.agents.forEach(a => { agentStatuses[a.agent_id] = a.status || 'active'; });
      renderAgentFleet();
    }
  } catch (err) {
    // Show inline error instead of silent failure
    console.error('Failed to refresh agents:', err);
  } finally {
    btn.disabled = false;
    btn.textContent = '↻ Refresh';
  }
}

[MODERADO] Inconsistência entre index.html e tipagem do Next.js
Onde: index.html vs src/lib/api.ts
O Problema: O index.html trata status de agentes como strings livres ('active', 'idle', 'offline'), enquanto o backend e o api.ts usam 'ready', 'running', 'error', 'stopped', 'paused', 'degraded', 'initializing'. As classes CSS no HTML (status-active, status-idle, status-offline) não correspondem aos status reais do backend, fazendo com que agentes em estado 'running' ou 'ready' não recebam o estilo verde correto.
A Solução: Alinhar os nomes de status no HTML com os do backend:
javascriptDownloadCopy codefunction getStatusClass(status) {
  switch (status) {
    case 'running': case 'ready': return 'status-active';
    case 'error': case 'degraded': return 'status-offline';
    case 'paused': case 'initializing': return 'status-idle';
    case 'stopped': return 'status-offline';
    default: return 'status-idle';
  }
}

[SUGESTÃO] Tema escuro está hardcoded — sem opção light
Onde: layout.tsx, globals.css
O Problema: O <html> tem className="dark" hardcoded e o next-themes está nas dependências mas nunca é configurado. Embora um dashboard de operações seja tipicamente dark, a ausência de opção pode causar problemas de acessibilidade para operadores com sensibilidade visual.
A Solução: Integrar next-themes no providers.tsx:
typescriptDownloadCopy codeimport { ThemeProvider } from "next-themes";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
      {children}
    </ThemeProvider>
  );
}

[SUGESTÃO] globals.css — classes utilitárias customizadas sem documentação
Onde: src/globals.css
O Problema: Classes como .glass, .glass-heavy, .neon-border, .status-ping são utilitários custom que não seguem nenhuma convenção documentada. Um novo desenvolvedor não sabe quais classes estão disponíveis nem como combiná-las. A animação status-ping usa ::before que só funciona se o elemento tiver position: relative definido inline ou herdado, o que não é óbvio.
A Solução: Documentar em um comentário de cabeçalho ou criar um arquivo DESIGN_SYSTEM.md. Alternativamente, converter para Tailwind plugins para que apareçam no autocomplete do IDE:
typescriptDownloadCopy code// tailwind.config.ts
plugins: [
  require("tailwindcss-animate"),
  function ({ addUtilities }) {
    addUtilities({
      ".glass": {
        background: "rgba(12, 12, 18, 0.7)",
        backdropFilter: "blur(20px)",
        border: "1px solid rgba(124, 58, 237, 0.08)",
      },
    });
  },
],

Resumo por Severidade
SeveridadeQuantidadeÁreasCRÍTICO5Arquitetura dual frontend, WebSocket sem backoff, dados simulados, XSS, a11yMODERADO8Cleanup de efeitos, acúmulo de estado, dependências, responsividade, loading statesSUGESTÃO4Dados estáticos duplicados, error boundaries, tema, design system
A prioridade imediata deve ser: (1) decidir entre index.html e Next.js e eliminar o outro, (2) criar src/app/page.tsx se a escolha for Next.js, (3) corrigir o XSS no HTML, e (4) implementar backoff exponencial no WebSocket.