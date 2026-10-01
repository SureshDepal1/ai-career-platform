const API_ROOT = "/api";

const tokenStore = {
  get access() { return localStorage.getItem("career_access"); },
  get refresh() { return localStorage.getItem("career_refresh"); },
  set(tokens) {
    localStorage.setItem("career_access", tokens.access);
    localStorage.setItem("career_refresh", tokens.refresh);
  },
  clear() {
    localStorage.removeItem("career_access");
    localStorage.removeItem("career_refresh");
  },
};

async function refreshAccessToken() {
  if (!tokenStore.refresh) return false;
  const response = await fetch(`${API_ROOT}/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: tokenStore.refresh }),
  });
  if (!response.ok) {
    tokenStore.clear();
    return false;
  }
  const data = await response.json();
  localStorage.setItem("career_access", data.access);
  return true;
}

export async function apiFetch(path, options = {}, retry = true) {
  const headers = new Headers(options.headers || {});
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (tokenStore.access) headers.set("Authorization", `Bearer ${tokenStore.access}`);
  const response = await fetch(`${API_ROOT}${path}`, { ...options, headers });
  if (response.status === 401 && retry && await refreshAccessToken()) {
    return apiFetch(path, options, false);
  }
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = payload.detail || Object.values(payload).flat().join(" ") || "Something went wrong.";
    throw new Error(message);
  }
  return payload;
}

export { tokenStore };
