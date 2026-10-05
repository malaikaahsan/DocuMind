import api from "./api";

export const searchDocuments = async ({
  query,
  top_k = 5,
  document_id = null,
}) => {
  const response = await api.post("/api/search", {
    query,
    top_k,
    document_id,
  });

  return response.data;
};