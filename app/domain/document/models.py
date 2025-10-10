from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Document(SQLModel, table=True):
    """Represents a stored document within the knowledge base."""

    __tablename__ = "document"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False, description="Title of the document")
    description: Optional[str] = Field(
        default=None, description="Optional description of the document"
    )
    source: Optional[str] = Field(
        default=None, description="File path, URL, or origin reference"
    )
    owner_id: Optional[int] = Field(
        default=None, description="Identifier of the user who uploaded the document"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of when the document was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of the last document update",
    )

    # Relationship with document chunks (embeddings)
    chunks: List["DocumentChunk"] = Relationship(
        back_populates="document",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )


class DocumentChunk(SQLModel, table=True):
    """Represents a text fragment (chunk) from a document with its embedding."""

    __tablename__ = "document_chunk"

    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(
        foreign_key="document.id",
        index=True,
        nullable=False,
        description="Reference to the parent document",
    )
    content: str = Field(nullable=False, description="Text content of the chunk")
    embedding: List[float] = Field(
        sa_column_kwargs={"type_": "vector(1536)"},
        description="Embedding vector generated from the chunk",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of when the chunk was created",
    )

    # Relationship back to document
    document: Document | None = Relationship(back_populates="chunks")
