from langchain.memory import RedisChatMessageHistory
import json
import logging
from langchain.memory import ConversationBufferWindowMemory
from typing import List, Optional
from langchain.schema import (
    BaseChatMessageHistory,
)
from langchain.schema.messages import BaseMessage, _message_to_dict, messages_from_dict
from typing import Any, Dict, List, Sequence
from langchain.schema import AIMessage, HumanMessage, SystemMessage, FunctionMessage, ChatMessage


def get_buffer_string(
    messages: Sequence[BaseMessage], human_prefix: str = "<|prompter|>", 
    ai_prefix: str = "<|assistant|>", 
    postfix: str = '<|endoftext|>') -> str:

    string_messages = []
    for m in messages:
        if isinstance(m, HumanMessage):
            prefix = human_prefix
        elif isinstance(m, AIMessage):
            prefix = ai_prefix
        elif isinstance(m, SystemMessage):
            prefix = "System"
        elif isinstance(m, FunctionMessage):
            prefix = "Function"
        elif isinstance(m, ChatMessage):
            prefix = m.role
        else:
            raise ValueError(f"Got unsupported message type: {m}")
        message = f"{prefix}{m.content}{postfix}"
        if isinstance(m, AIMessage) and "function_call" in m.additional_kwargs:
            message += f"{m.additional_kwargs['function_call']}"
        string_messages.append(message)

    return "\n".join(string_messages)




class CustomConversationBufferWindowMemory(ConversationBufferWindowMemory):
    """Buffer for storing conversation memory."""

    human_prefix: str = "<|prompter|>"
    ai_prefix: str = "<|assistant|>"
    postfix: str = '<|endoftext|>'
    memory_key: str = "history"  #: :meta private:
    k: int = 5


    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Return history buffer."""

        buffer: Any = self.buffer[-self.k * 2 :] if self.k > 0 else []
        if not self.return_messages:
            buffer = get_buffer_string(
                buffer,
                human_prefix=self.human_prefix,
                ai_prefix=self.ai_prefix,
            )
        return {self.memory_key: buffer}


class CustomRedisChatMessageHistory(RedisChatMessageHistory):
    """Chat message history stored in a Redis database."""

    def __init__(
        self,
        session_id: str,
        url: str = "redis://localhost:6379/0",
        key_prefix: str = "message_store:",
        ttl: Optional[int] = None,
        max_len = 10,
    ):
        self.max_len = max_len
        RedisChatMessageHistory.__init__(self, 
                                         session_id = session_id, 
                                         url = url, 
                                         key_prefix = key_prefix, 
                                         ttl = ttl)


    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        """Retrieve the messages from Redis"""
        _items = self.redis_client.lrange(self.key, 0, -1)
        items = [json.loads(m.decode("utf-8")) for m in _items[::-1]]
        messages = messages_from_dict(items)
        
        if len(messages) > self.max_len:
            self.redis_client.lpop(self.key, 2)

        return messages




