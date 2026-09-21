from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts: list[str]):
    embeddings = model.encode(
        texts,
        show_progress_bar=False,
    )

    return embeddings.tolist()