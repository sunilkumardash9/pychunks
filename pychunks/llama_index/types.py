"""Text splitter implementations."""
import json
from abc import ABC, abstractmethod
from typing import List, Any, Dict
from pydantic import BaseModel, ConfigDict

class BaseComponent(BaseModel):
    """Base component object to caputure class names."""

    @classmethod
    @abstractmethod
    def class_name(cls) -> str:
        """Get class name."""

    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        data = self.dict(**kwargs)
        data["class_name"] = self.class_name()
        return data

    def to_json(self, **kwargs: Any) -> str:
        data = self.to_dict(**kwargs)
        return json.dumps(data)

    # TODO: return type here not supported by current mypy version
    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs: Any):  # type: ignore
        if isinstance(kwargs, dict):
            data.update(kwargs)

        data.pop("class_name", None)
        return cls(**data)

    @classmethod
    def from_json(cls, data_str: str, **kwargs: Any):  # type: ignore
        data = json.loads(data_str)
        return cls.from_dict(data, **kwargs)

class TextSplitter(ABC, BaseComponent):
    
    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True) 

    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        ...


class MetadataAwareTextSplitter(TextSplitter):
    @abstractmethod
    def split_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]:
        ...