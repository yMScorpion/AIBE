export interface WsClientConfig<TMessage> {
  createUrl: () => string;
  onMessage: (message: TMessage) => void;
  onConnectionChange?: (connected: boolean) => void;
  maxDelayMs?: number;
}

export class TypedWsClient<TMessage> {
  private ws: WebSocket | null = null;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private reconnectAttempt = 0;
  private manuallyDisconnected = false;
  private readonly maxDelayMs: number;

  constructor(private readonly config: WsClientConfig<TMessage>) {
    this.maxDelayMs = config.maxDelayMs ?? 30_000;
  }

  connect() {
    this.manuallyDisconnected = false;
    this.clearReconnect();
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    try {
      this.ws = new WebSocket(this.config.createUrl());
      this.ws.onopen = () => {
        this.reconnectAttempt = 0;
        this.config.onConnectionChange?.(true);
      };
      this.ws.onclose = () => {
        this.config.onConnectionChange?.(false);
        this.ws = null;
        this.scheduleReconnect();
      };
      this.ws.onerror = () => {
        this.config.onConnectionChange?.(false);
        this.ws?.close();
      };
      this.ws.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data) as TMessage;
          this.config.onMessage(parsed);
        } catch {}
      };
    } catch {
      this.config.onConnectionChange?.(false);
      this.scheduleReconnect();
    }
  }

  send(payload: unknown) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      return;
    }
    this.ws.send(JSON.stringify(payload));
  }

  disconnect() {
    this.manuallyDisconnected = true;
    this.clearReconnect();
    this.ws?.close();
    this.ws = null;
    this.reconnectAttempt = 0;
    this.config.onConnectionChange?.(false);
  }

  private scheduleReconnect() {
    if (this.manuallyDisconnected) return;
    this.clearReconnect();
    const delay = Math.min(1_000 * 2 ** this.reconnectAttempt, this.maxDelayMs);
    this.reconnectAttempt += 1;
    this.reconnectTimer = setTimeout(() => this.connect(), delay);
  }

  private clearReconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }
}
