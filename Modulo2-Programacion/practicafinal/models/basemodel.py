from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Exportamos todos los símbolos comunes para usarlos desde aquí
__all__ = [
    "Base",
    "Column",
    "Integer",
    "String",
    # "Float",
    # "Date",
    "DateTime",
    # "Boolean",
    "ForeignKey",
    # "Text",
    "relationship",
    "BaseModel",
    "Field",
    "field_validator",
    "model_validator",
    "Optional"
]

Base = declarative_base()