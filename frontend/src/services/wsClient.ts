type WsHandler = (payload: Record<string, unknown>) => void;

class WsClient {
  private socket: WebSocket | null = null;
  private handlers: Map<string, Set<WsHandler>> = new Map();
  private reconnectTimer: number | null = null;
  private currentToken: string | null = null;

  connect(token: string): void {
    this.currentToken = token;
    if (this.socket && this.socket.readyState <= WebSocket.OPEN) return;

    const httpBase = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";
    const wsBase = httpBase.replace(/^http/, "ws");
    this.socket = new WebSocket(`${wsBase}/ws?token=${encodeURIComponent(token)}`);

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const eventName = data.event as string;
        this.handlers.get(eventName)?.forEach((handler) => handler(data));
      } catch {
        // ignore malformed payloads
      }
    };

    this.socket.onclose = () => {
      this.socket = null;
      if (this.currentToken) {
        this.reconnectTimer = window.setTimeout(() => {
          if (this.currentToken) this.connect(this.currentToken);
        }, 3000);
      }
    };
  }

  disconnect(): void {
    this.currentToken = null;
    if (this.reconnectTimer) {
      window.clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    this.socket?.close();
    this.socket = null;
  }

  on(eventName: string, handler: WsHandler): () => void {
    if (!this.handlers.has(eventName)) this.handlers.set(eventName, new Set());
    this.handlers.get(eventName)!.add(handler);
    return () => this.handlers.get(eventName)?.delete(handler);
  }
}

export const wsClient = new WsClient();
