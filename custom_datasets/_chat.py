from typing import Any, Dict, List, Mapping, Optional
from torchtune.modules.tokenizers import Tokenizer
from torchtune.data import Message
from torchtune.dataset import ChatDataset

def _converter(sample: Mapping[str, Any]) -> List[Message]:
    system_msg = sample['system']
    text_msgs = [m.strip() for m in sample['conversations'].split('[sep]')]
    
    is_user = True
    # Multi-turn dataset
    msgs = [
        Message(
            role="system",
            content=system_msg,
            masked=True, # Mask if not training on prompt
        )
    ]
    for m in text_msgs:
        msgs.append(
            Message(
                role="user" if is_user else "assistant",
                content=m,
                masked=is_user,
            )
        )
        is_user = not is_user

    return msgs

def custom_chat_dataset(
    tokenizer: Tokenizer,
    source: str,
    max_seq_len: Optional[int] = None,
    **load_dataset_kwargs: Dict[str, Any],
) -> ChatDataset:

    return ChatDataset(
        tokenizer=tokenizer,
        source=source,
        convert_to_messages=_converter,
        # Llama3 does not need a chat format
        chat_format=None,
        max_seq_len=max_seq_len,
        **load_dataset_kwargs,
    )