import { useAuth } from "../context/AuthContext";
import { useEffect, useState } from "react";

import {
  getDocuments,
  uploadDocument,
  deleteDocument,
} from "../services/documentService";

import DocumentCard from "../components/DocumentCard";

function Dashboard() {
  const { logout } = useAuth();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const loadDocuments = async () => {
    try {
      setError("");

      const data = await getDocuments();

      setDocuments(data.documents);
    } catch (error) {
      setError(error.response?.data?.detail || "Failed to load documents");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  useEffect(() => {
  const hasProcessingDocument = documents.some(
    (document) => document.status === "processing"
  );

  if (!hasProcessingDocument) {
    return;
  }

  const interval = setInterval(() => {
    loadDocuments();
  }, 3000);

  return () => {
    clearInterval(interval);
  };
}, [documents]);

  const handleUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    try {
      setUploading(true);
      setError("");

      await uploadDocument(file);

      await loadDocuments();
    } catch (error) {
      setError(error.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);

      event.target.value = "";
    }
  };

  const handleDelete = async (documentId) => {
    try {
      await deleteDocument(documentId);

      setDocuments((current) =>
        current.filter((document) => document.id !== documentId),
      );
    } catch (error) {
      setError(error.response?.data?.detail || "Failed to delete document");
    }
  };

  return (
    <div>
      <h1>DocuMind Dashboard</h1>

      <p>You are authenticated.</p>

      <button onClick={logout}>Logout</button>
      {error && <p>{error}</p>}
      <div>
        <label>
          {uploading ? "Uploading..." : "Upload PDF"}

          <input
            type="file"
            accept="application/pdf"
            onChange={handleUpload}
            disabled={uploading}
          />
        </label>
      </div>

      {loading ? (
        <p>Loading documents...</p>
      ) : documents.length === 0 ? (
        <p>You haven't uploaded any documents yet.</p>
      ) : (
        <div>
          {documents.map((document) => (
            <DocumentCard
              key={document.id}
              document={document}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default Dashboard;
