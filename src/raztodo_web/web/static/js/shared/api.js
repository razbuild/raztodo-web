export const API = "/api/tasks";

export async function api(path, options = {}) {
  const response = await fetch(path, options);

  if (!response.ok) {
    const apiError = new Error(
      "Something went wrong. Please try again.",
    );

    apiError.status = response.status;

    throw apiError;
  }

  if (response.status === 204) return null;

  return response.json();
}
