/**
 * API Client for Darukaa.Earth Biodiversity Backend
 */

const API_BASE = '/api';

export async function sendChatMessage(message, structuredInput = null, sessionId = 'default_session') {
  const payload = {
    message: message || '',
    structured_input: structuredInput,
    session_id: sessionId
  };

  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail?.validation_errors?.join(', ') || 'Diagnostic pipeline error');
  }

  return await res.json();
}

export async function fetchCaseFile(sessionId = 'default_session') {
  const res = await fetch(`${API_BASE}/case-file/${sessionId}`);
  if (!res.ok) throw new Error('Failed to fetch case file');
  return await res.json();
}

export async function resetCaseFile(sessionId = 'default_session') {
  const res = await fetch(`${API_BASE}/case-file/${sessionId}/reset`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to reset case file');
  return await res.json();
}

export async function fetchDemoCase(demoKey = 'canonical_semi_arid_wheat') {
  const res = await fetch(`${API_BASE}/demo/${demoKey}`);
  if (!res.ok) throw new Error('Failed to fetch demo case');
  return await res.json();
}

export async function fetchSessions(signal = null) {
  const res = await fetch(`${API_BASE}/sessions`, { signal });
  if (!res.ok) throw new Error('Failed to fetch sessions');
  return await res.json();
}

export async function createSession(title = 'New Investigation', signal = null) {
  const res = await fetch(`${API_BASE}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
    signal
  });
  if (!res.ok) throw new Error('Failed to create session');
  return await res.json();
}

export async function fetchSessionDetails(sessionId, signal = null) {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`, { signal });
  if (!res.ok) throw new Error(`Failed to fetch session ${sessionId}`);
  return await res.json();
}

export async function fetchSessionMessages(sessionId, signal = null) {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/messages`, { signal });
  if (!res.ok) throw new Error(`Failed to fetch messages for session ${sessionId}`);
  return await res.json();
}

export async function fetchSessionAudit(sessionId, signal = null) {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/audit`, { signal });
  if (!res.ok) throw new Error(`Failed to fetch audit log for session ${sessionId}`);
  return await res.json();
}

export async function deleteSession(sessionId) {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error(`Failed to delete session ${sessionId}`);
  return await res.json();
}
