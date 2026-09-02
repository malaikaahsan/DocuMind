import api from "./api";

export const uploadDocument = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/api/documents/upload",
    formData
  );

  return response.data;
};


export const getDocuments = async () => {
  const response = await api.get(
    "/api/documents"
  );

  return response.data;
};


export const getDocument = async (documentId) => {
  const response = await api.get(
    `/api/documents/${documentId}`
  );

  return response.data;
};


export const deleteDocument = async (documentId) => {
  const response = await api.delete(
    `/api/documents/${documentId}`
  );

  return response.data;
};