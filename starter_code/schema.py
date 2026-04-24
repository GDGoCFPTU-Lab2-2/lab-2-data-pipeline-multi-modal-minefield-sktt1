from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================

class SourceType(str, Enum):
    PDF = "PDF"
    VIDEO = "Video"
    HTML = "HTML"
    CSV = "CSV"
    CODE = "Code"

class UnifiedDocument(BaseModel):
    # model_config provides flexibility for the T+60m schema migration
    # populate_by_name=True: Allows populating fields using either the original name or an alias.
    # extra='allow': Retains any unexpected or newly introduced fields without throwing validation errors.
    model_config = ConfigDict(populate_by_name=True, extra='allow')

    # Required fields checked by the Forensic Agent
    document_id: str = Field(
        ..., 
        description="Unique identifier (e.g., 'csv-001'). Mandatory for duplicate tracking."
    )
    content: str = Field(
        ..., 
        description="Extracted text or data. Checked by semantic gates for corrupt values."
    )
    source_type: SourceType = Field(
        ..., 
        description="Origin format constrained to the SourceType Enum."
    )
    
    # Optional fields equipped with validation aliases to anticipate field renames in v2
    author: Optional[str] = Field(
        default="Unknown", 
        validation_alias="creator_name",
        description="Author of the document."
    )
    timestamp: Optional[datetime] = Field(
        default=None, 
        validation_alias="created_at",
        description="Time of creation or processing."
    )
    
    # Flexible dictionary for source-specific extracted info (e.g., 'detected_price_vnd' for transcripts)
    source_metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Key-value pairs for unstructured or source-specific attributes."
    )
