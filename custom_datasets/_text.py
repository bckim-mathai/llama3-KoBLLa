# https://github.com/RdoubleA/torchtune/blob/custom_dataset/torchtune/datasets/_text_completion.py

# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from typing import Any, Dict, List, Mapping, Optional, Tuple

from datasets import load_dataset
from torch.utils.data import Dataset
from torchtune.data import truncate
from torchtune.modules.tokenizers import Tokenizer


class TextCompletionDataset(Dataset):
    """
    Freeform dataset for any unstructured text corpus. Quickly load any dataset
    from Hugging Face or local disk and tokenize it correctly for your model.

    Args:
        tokenizer (Tokenizer): Tokenizer used to encode data. Tokenize must implement an `encode` and `decode` method.
        source (str): path string of dataset, anything supported by Hugging Face's `load_dataset`
            (https://huggingface.co/docs/datasets/en/package_reference/loading_methods#datasets.load_dataset.path)
        column (str): name of column in the sample that contains the text data
        max_seq_len (Optional[int]): Maximum number of tokens in the returned input and label token id lists.
            Default is None, disabling truncation. We recommend setting this to the highest you can fit in memory
            and is supported by the model. For example, llama2-7B supports up to 4096 for sequence length.
        **load_dataset_kwargs (Dict[str, Any]): additional keyword arguments to pass to `load_dataset`.
    """

    def __init__(
        self,
        tokenizer: Tokenizer,
        source: str,
        column: str,
        max_seq_len: Optional[int] = None,
        **load_dataset_kwargs: Dict[str, Any],
    ) -> None:
        self._tokenizer = tokenizer
        self._data = load_dataset(source, **load_dataset_kwargs)
        self.max_seq_len = max_seq_len
        self._column = column

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index: int) -> Tuple[List[int], List[int]]:
        sample = self._data[index]
        return self._prepare_sample(sample)

    def _prepare_sample(self, sample: Mapping[str, Any]) -> Tuple[List[int], List[int]]:
        prompt = sample[self._column]
        if prompt is None:
            prompt=''
        tokens = self._tokenizer.encode(text=prompt, add_bos=True, add_eos=True)

        # Truncate if needed, but don't coerce EOS id
        if self.max_seq_len is not None:
            tokens = truncate(tokens, self.max_seq_len - 1, self._tokenizer.eos_id)

        # No need to offset labels by 1 - happens in the recipe
        labels = tokens.copy()

        assert len(tokens) == len(labels)

        return tokens, labels


def custom_text_dataset(
    tokenizer: Tokenizer,
    source: str,
    column: str,
    max_seq_len: Optional[int] = None,
    **load_dataset_kwargs: Dict[str, Any],
) -> TextCompletionDataset:
    """
    Build a configurable freeform text dataset with instruction prompts. This method should be
    used to configure a custom text dataset from the yaml config instead of
    using `TextDataset` directly, as it is made to be config friendly.

    Args:
        tokenizer (Tokenizer): Tokenizer used to encode data. Tokenize must implement an `encode` and `decode` method.
        source (str): path string of dataset, anything supported by Hugging Face's `load_dataset`
            (https://huggingface.co/docs/datasets/en/package_reference/loading_methods#datasets.load_dataset.path)
        column (str): name of column in the sample that contains the text data
        max_seq_len (Optional[int]): Maximum number of tokens in the returned input and label token id lists.
            Default is None, disabling truncation. We recommend setting this to the highest you can fit in memory
            and is supported by the model. For example, llama2-7B supports up to 4096 for sequence length.
        **load_dataset_kwargs (Dict[str, Any]): additional keyword arguments to pass to `load_dataset`.

    Returns:
        TextCompletionDataset: the configured TextCompletionDataset
    """
    return TextCompletionDataset(
        tokenizer=tokenizer,
        source=source,
        column=column,
        max_seq_len=max_seq_len,
        **load_dataset_kwargs,
    )