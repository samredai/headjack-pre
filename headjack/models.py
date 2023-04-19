"""
Models used across headjack
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Tuple
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Stringable(Protocol):
    def __str__(self) -> str:
        pass


@dataclass
class Tool:
    description: str
    ref_name: str

    def __call__(self, utterance: "Utterance") -> "Observation":
        raise NotImplementedError()

    async def __acall__(self, utterance: "Utterance") -> "Observation":
        raise NotImplementedError()


class ActionKind(str, Enum):
    use_tool = "Use a tool."
    respond = "Generate a response from the current information."


class Action(BaseModel):
    kind: ActionKind


class Observation(BaseModel):
    """
    Value produced from using a tool
    """

    tool: Tool
    args: List[Any]


class Utterance(BaseModel):
    marker: str
    utterance: str = Field(..., description="The text of the utterance")
    session_id: UUID = Field(default_factory=uuid4, description="The UUID session identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="The timestamp of the utterance")

    def __str__(self):
        return self.marker + self.utterance


@dataclass
class BaseMemory:
    history: List[Tuple[Utterance, Utterance]] = field(default_factory=list)

    def add_memory(self, human: Utterance, agent: Utterance):
        self.history.append((human, agent))

    def __str__(self):
        return "\n".join(str(human) + "\n" + str(agent) for human, agent in self.history)


@dataclass
class Agent:
    description: str
    ref_name: str
    tools: List[Tool]
    memory: BaseMemory

    def __call__(self, str) -> Stringable:
        raise NotImplementedError()

    async def __acall__(self, str) -> Stringable:
        raise NotImplementedError()


class BatchEmbeddings(BaseModel):
    ids: List[str]
    documents: List[str]
    metadatas: List[Dict[str, str]]


class Document(BaseModel):
    name: str
    description: str
    metadata: Optional[Dict[str, str]]

    def generate_embeddings(self) -> BatchEmbeddings:
        # Add logic here to chunk up the content
        embeddings = BatchEmbeddings(
            ids=["foo"],
            documents=["placeholder sentence"],
            metadatas=[{"node_document": "foo"}],
        )
        return embeddings


class KnowledgeDocument(Document):
    content: str
    url: str
