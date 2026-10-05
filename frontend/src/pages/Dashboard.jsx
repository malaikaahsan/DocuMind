import { useAuth } from "../context/AuthContext";
import { useEffect, useState } from "react";

import {
  getDocuments,
  uploadDocument,
  deleteDocument,
} from "../services/documentService";
import { searchDocuments } from "../services/searchService";

import DocumentCard from "../components/DocumentCard";

function Dashboard() {
  const { logout } = useAuth();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [selectedDocumentId, setSelectedDocumentId] = useState("");

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
      (document) => document.status === "processing",
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

  const handleSearch = async (event) => {
    event.preventDefault();

    if (!searchQuery.trim()) {
      return;
    }

    try {
      setSearching(true);
      setError("");

      const data = await searchDocuments({
        query: searchQuery,
        top_k: 5,
        document_id: selectedDocumentId || null,
      });

      setSearchResults(data.results);
    } catch (error) {
      setError(error.response?.data?.detail || "Search failed");
    } finally {
      setSearching(false);
    }
  };

  return (
    <div>
      <h1>DocuMind Dashboard</h1>

      <p>You are authenticated.</p>

      <button onClick={logout}>Logout</button>

      <div>
        <h2>Search Documents</h2>
        <select
          value={selectedDocumentId}
          onChange={(event) => setSelectedDocumentId(event.target.value)}
        >
          <option value="">All documents</option>

          {documents
            .filter((document) => document.status === "ready")
            .map((document) => (
              <option key={document.id} value={document.id}>
                {document.original_name}
              </option>
            ))}
        </select>
        <form onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Ask something about your documents..."
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
          />

          <button type="submit" disabled={searching}>
            {searching ? "Searching..." : "Search"}
          </button>
        </form>
      </div>

      {searchResults.length > 0 && (
        <div>
          <h3>Search Results</h3>

          {searchResults.map((result) => (
            <div key={`${result.document_id}-${result.chunk_index}`}>
              <p>
                <strong>Page:</strong> {result.page_number}
              </p>

              <p>
                <strong>Chunk:</strong> {result.chunk_index}
              </p>

              <p>{result.text}</p>

              <p>
                <strong>Distance:</strong> {result.distance.toFixed(4)}
              </p>
            </div>
          ))}
        </div>
      )}

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
