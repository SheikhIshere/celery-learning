/// <reference types="vite/client" />

// Access environment variable safely
export const API_HOST = import.meta.env.VITE_API_HOST || 'http://localhost:8001';

export const API_BASE = `${API_HOST}/v1/api/chat`;

export const POLLING_INTERVAL_MS = 1000;
export const POLLING_TIMEOUT_MS = 60000;