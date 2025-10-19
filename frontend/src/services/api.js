/**
 * API Service
 * Handles all API communication with backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class APIService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('auth_token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Debate endpoints
  async startDebate(topic, stance = 'supporting') {
    return this.request('/debate/start', {
      method: 'POST',
      body: JSON.stringify({ topic, initial_stance: stance }),
    });
  }

  async submitArgument(debateId, argument, roundNumber) {
    return this.request('/debate/argument', {
      method: 'POST',
      body: JSON.stringify({
        debate_id: debateId,
        argument,
        round_number: roundNumber,
      }),
    });
  }

  async getDebateHistory(debateId) {
    return this.request(`/debate/history/${debateId}`);
  }

  async getAgentStatus() {
    return this.request('/debate/agent-status');
  }

  // Document endpoints
  async uploadDocuments(files) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    return this.request('/documents/upload', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
  }

  // Web scraping endpoints
  async scrapeTopic(topic, urls = null) {
    return this.request('/scrape/scrape', {
      method: 'POST',
      body: JSON.stringify({ topic, urls }),
    });
  }

  // WebSocket connection
  connectWebSocket(debateId, onMessage) {
    const wsURL = `ws://localhost:8000/ws/debate/${debateId}`;
    const ws = new WebSocket(wsURL);

    ws.onopen = () => console.log('WebSocket connected');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };
    ws.onerror = (error) => console.error('WebSocket error:', error);
    ws.onclose = () => console.log('WebSocket disconnected');

    return ws;
  }
}

export default new APIService();