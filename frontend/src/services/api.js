const BASE_URL = import.meta.env.VITE_API_URL || (
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://localhost:8000"
    : window.location.origin
);

/**
 * Upload a batch of answer sheet images along with document metadata.
 * @param {FormData} formData  – must include files[], course, batch, date, exam
 * @returns {Promise<object>}
 */
export async function uploadBatch(formData) {
  const token = localStorage.getItem("access_token");
  const res = await fetch(`${BASE_URL}/extract/batch`, {
    method: "POST",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: formData, // multipart/form-data set automatically by browser
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(err.detail || `Server error ${res.status}`);
  }

  return res.json();
}

/**
 * Download the result Excel file for a batch and trigger a browser save.
 * @param {string} batchId  – the batch_id returned by uploadBatch
 * @param {string} filename – suggested filename for the save dialog
 */
export async function downloadResult(batchId, filename) {
  const token = localStorage.getItem("access_token");
  const res = await fetch(`${BASE_URL}/extract/download/${batchId}`, {
    method: "GET",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });

  if (!res.ok) {
    throw new Error(`Download failed: ${res.status}`);
  }

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename || `${batchId}.xlsx`;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

/**
 * Save a batch record to localStorage.
 * @param {object} batch
 */
export function saveBatchLocally(batch) {
  const existing = getLocalBatches();
  // Replace if same batch_id exists, otherwise prepend
  const filtered = existing.filter((b) => b.batch_id !== batch.batch_id);
  localStorage.setItem("markupBatches", JSON.stringify([batch, ...filtered]));
}

/**
 * Read all saved batch records from localStorage.
 * @returns {object[]}
 */
export function getLocalBatches() {
  try {
    return JSON.parse(localStorage.getItem("markupBatches") || "[]");
  } catch {
    return [];
  }
}
