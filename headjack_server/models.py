"""
Models used across headjack
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, ClassVar, Dict, Generator, List, Optional, Protocol, Tuple, Type, Optional, TypeVar, Callable, AsyncGenerator
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

T = TypeVar("T")
def required_value(message: str, return_type: Type[T])->Callable[[], T]:
    def raise_message()->T:
        raise ValueError(message)
    return raise_message
        
class Stringable(Protocol):
    def __str__(self) -> str:
        pass

async def cli_agent_input()->AsyncGenerator["Utterance", None]:
    user = " "
    while True and user:
        user = input()
        yield Utterance(user, marker="User: ")

@dataclass
class Tool:
    default_description: ClassVar[str]
    default_ref_name: ClassVar[str]
    model_identifier: str
    description_: Optional[str] = None
    ref_name_: Optional[str] = None
    
    @property
    def description(self):
        return self.description_ or self.default_description

    @property
    def ref_name(self):
        return self.ref_name_ or self.default_ref_name

    async def __call__(self, utterance: "Utterance") -> "Observation":
        raise NotImplementedError()


@dataclass
class Utterance:
    utterance: str
    session_id_: Optional[UUID] = None
    marker: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    context: str = ""
    parent: Optional["Utterance"] = None
    
    def __str__(self):
        return self.marker + self.utterance
    
    def history(self, n: Optional[int] = None) -> Generator:
        n_ = n or float('inf')
        curr = self
        while n_>0 and curr is not None:
            yield curr
            curr = self.parent  # type: ignore
            n_-=1
    
    @property
    def session_id(self):
        if self.session_id_ is not None:
            return self.session_id_
        if self.parent is not None:
            return self.parent.session_id
        return None

@dataclass
class Observation(Utterance):
    """
    Value produced from a tool
    """
    tool: Tool = field(default_factory=required_value("`tool` is required for an Observation.", Tool))

@dataclass
class BaseMemory:
    history: List[Tuple[Utterance, Utterance]] = field(default_factory=list)

    def add_memory(self, human: Utterance, agent: Utterance):
        self.history.append((human, agent))

    def __str__(self):
        return "\n".join(str(human) + "\n" + str(agent) for human, agent in self.history)


@dataclass
class Agent:
    description: ClassVar[str]
    ref_name: ClassVar[str]
    tools: List[Type[Tool]]
    model_identifier: str
    memory: "BaseMemory" = field(default_factory=BaseMemory)

    async def __call__(self, input: AsyncGenerator[Utterance, None]) -> Utterance:
        raise NotImplementedError()

@dataclass
class Thought(Utterance):
    """
    Value produced from an agent
    """
    agent: Agent = field(default_factory=required_value("`agent` is required for a Thought.", Agent))
    marker = "Thought: "

@dataclass
class Answer(Utterance):
    """
    Final answer value produced from an agent
    """
    agent: Agent = field(default_factory=required_value("`agent` is required for a Answer.", Agent))
    marker = "Answer: "

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
