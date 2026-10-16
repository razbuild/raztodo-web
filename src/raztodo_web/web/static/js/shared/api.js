export const API = "/api/tasks";

const GENERIC_MESSAGE = "Something went wrong. Please try again.";

export async function api(path, options = {}) {
  const response = await fetch(path, options);

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    const error = payload?.error ?? payload?.detail;

    let message = "";
    let code;

    if (error && typeof error === "object" && !Array.isArray(error)) {
      message = error.message;
      code = error.code;
    } else if (typeof error === "string") {
      message = error;
    }

    if (!message) {
      message =
        response.status === 422
          ? GENERIC_MESSAGE
          : response.statusText || GENERIC_MESSAGE;
    }

    const apiError = new Error(message);
    apiError.status = response.status;
    apiError.code = code;
    throw apiError;
  }

  if (response.status === 204) return null;

  return response.json();
}
