export interface Session {
  id: number;
  title: string;
  messages: Message[] | string; // API might return stringified JSON
  created_at: string;
  updated_at: string;
}

export interface Message {
  count?: number;
  message: string; // User input
  response: string; // AI output
  created_at?: string;
}

export interface AiRequest {
  id: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  response?: string;
  message?: string;
}

export interface CreateSessionPayload {
  title?: string;
}

export interface SendMessagePayload {
  message: string;
}