export const API = "/api/tasks";

export async function api(path, options = {}) {
  const response = await fetch(path, options);

  if (!response.ok) {
    const payload = await response
      .json()
      .catch(() => ({ detail: response.statusText }));

    const error = payload.error || payload.detail;

    if (error && typeof error === "object") {
      const message = error.message || response.statusText;
      const apiError = new Error(message);
      apiError.code = error.code;
      throw apiError;
    }

    throw new Error(
      typeof payload.detail === "string"
        ? payload.detail
        : response.statusText,
    );
  }

  if (response.status === 204) return null;

  return response.json();
}
