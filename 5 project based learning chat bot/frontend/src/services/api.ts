import { API_BASE, POLLING_INTERVAL_MS, POLLING_TIMEOUT_MS } from '../constants';
import { Session, AiRequest, CreateSessionPayload, SendMessagePayload } from '../types';

const getHeaders = () => ({
  'Content-Type': 'application/json',
});

export const api = {
  async getSessions(): Promise<Session[]> {
    const res = await fetch(`${API_BASE}/sessions/`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Failed to fetch sessions');
    return res.json();
  },

  async createSession(title?: string): Promise<Session> {
    const payload: CreateSessionPayload = title ? { title } : {};
    const res = await fetch(`${API_BASE}/sessions/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to create session');
    return res.json();
  },

  async getSession(id: number): Promise<Session> {
    const res = await fetch(`${API_BASE}/sessions/${id}/`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Failed to fetch session details');
    const data = await res.json();
    
    // Handle case where messages might be a stringified JSON
    if (typeof data.messages === 'string') {
      try {
        data.messages = JSON.parse(data.messages);
      } catch (e) {
        console.error("Failed to parse messages JSON", e);
        data.messages = [];
      }
    }
    return data;
  },

  async sendMessage(sessionId: number, message: string): Promise<AiRequest> {
    const payload: SendMessagePayload = { message };
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/send/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to send message');
    return res.json();
  },

  async getRequestStatus(requestId: number): Promise<AiRequest> {
    const res = await fetch(`${API_BASE}/requests/${requestId}/`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Failed to poll request');
    return res.json();
  },

  // Polling helper
  async pollForCompletion(requestId: number): Promise<void> {
    const startTime = Date.now();

    return new Promise((resolve, reject) => {
      const checkStatus = async () => {
        try {
          if (Date.now() - startTime > POLLING_TIMEOUT_MS) {
            reject(new Error('Request timed out'));
            return;
          }

          const data = await this.getRequestStatus(requestId);
          
          if (data.status === 'completed') {
            resolve();
          } else if (data.status === 'failed') {
            reject(new Error('AI Request failed on server'));
          } else {
            // Still pending or running
            setTimeout(checkStatus, POLLING_INTERVAL_MS);
          }
        } catch (error) {
          reject(error);
        }
      };
      
      checkStatus();
    });
  }
};