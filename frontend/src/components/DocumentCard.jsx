function DocumentCard({
  document,
  onDelete,
}) {
  return (
    <div>
      <h3>{document.original_name}</h3>

      <p>
        Status: {document.status}
      </p>

      <p>
        Pages: {document.page_count}
      </p>

      <p>
        Uploaded:{" "}
        {new Date(
          document.uploaded_at
        ).toLocaleDateString()}
      </p>

      <button
        onClick={() => onDelete(document.id)}
      >
        Delete
      </button>
    </div>
  );
}

export default DocumentCard;