# Llama-3-KoBLLa

A Korean Bilingual Large Language model built with Meta Llama 3.

This project is supported and maintained by [(주)매쓰에이아이](https://maiclass.com) (MathAI).

<img src="assets/logo.png" alt="Llama-3-KoBLLa" style="width:50%;" />

## Why Another Korean Language Model?

KoBLLa models are built with a different approach compared to other Korean language models.
We believe that a good Korean language model should have these qualities:

* **Understanding of Korean Language and Culture:** The model should deeply understand the Korean language and its cultural context.
* **Skill in Following Korean Instructions:** It should accurately understand and follow instructions given in Korean. 

To be truly useful, a Korean language model should also have:

* **Specific Knowledge for Different Fields:** The model should have the necessary background knowledge for the specific area it's being used in.

Many existing Korean language models focus on learning Korean text to understand the language.
But, this can make them less capable of following instructions well.
Later training is done to improve their instruction-following abilities, but this often leads to models that are not great at either Korean or English instructions.
Additionally, good quality Korean instruction data can be hard to find, and even when available, licensing restrictions might prevent its use in commercial settings.

Therefore, our goal is to create a model that **excels in understanding Korean as a foreign language without losing its ability to follow English instructions well.**

## Base Models

### Llama 3 8B

Meta's Llama 3 is a large language model that is freely available for use by small businesses (less than 700 million monthly active users). 

While primarily an English-based model, Llama 3 has been trained on a diverse set of foreign languages, including Korean.
It also has a large enough vocabulary to handle non-alphabetic languages, like Korean.

KoBLLa uses `Meta-Llama 3 7B` as a base and trains it further to improve its understanding of the Korean language, culture, and specific knowledge related to its intended use.

### Llama 3 8B-Instruct

This model has been fine-tuned to excel in following instructions (especially in English).

Recent research suggests that a language model's ability to follow instructions well doesn't just depend on its knowledge.
It also relies on its ability to change its communication style, much like style transfer in vision models.

Therefore, we've used a method where language, culture, and knowledge are learned as text data in the base model.
The instruct model (or chat model) is trained with a smaller set of instructions.
This approach is inspired by the ideas from [LIMA](https://arxiv.org/abs/2305.11206).

To avoid big changes in the model's overall parameters during the instruction fine-tuning process, we use the concepts of [LoRA](https://arxiv.org/abs/2106.09685) and [Chat Vector](https://arxiv.org/abs/2310.04799).
This means we focus on changing smaller, specific parts of the model.

We calculate the difference between the instruct model's weights and the base model's weights.
This difference is called the chat vector.
This chat vector is then added to the Korean-trained base model and serves as the starting point for the instruct model.

## Dataset

### Ko-wikitext (20240501)

We modified the scripts in the [lovit/kowikitext](https://github.com/lovit/kowikitext/) repository to obtain a recent dump of Korean Wikipedia and save it in `.csv` format.

This corpus is licensed under CC-BY-SA 3.0, the same license as Korean Wikipedia.
For details, visit https://www.creativecommons.org/licenses/by-sa/3.0/.

### KoLIMA(MathAI) and BiLIMA

KoLIMA(MathAI) is a Korean translation of the [LIMA: Less Is More for Alignment](https://arxiv.org/pdf/2305.11206.pdf), created using Google's Gemini Pro 1.5.

While the [taeshahn/ko-lima](https://huggingface.co/datasets/taeshahn/ko-lima) dataset already exists, our KoLIMA(MathAI) dataset differs significantly in its use of Gemini Pro 1.5 for translation instead of the [DeepL API](https://developers.deepl.com/docs).
Furthermore, our dataset features user queries written in informal Korean (banmal, 반말) and assistant responses in formal Korean (jondaetmal, 존댓말).

BiLIMA is a bilingual LIMA dataset with two modes: `en_ko` and `ko_en`.
- `en_ko`: the user's query is given in English and the assistant's answer is given in Korean.
- `ko_en`: the user's query is given in Korean and the assistant's answer is given in English.

## Fine-tuning Llama 3 for English and Korean

We believe sharing our training methods and configurations is crucial.
We are convinced that this openness will foster greater collaboration and ultimately contribute to the development of even more advanced Korean language models.

This project uses [TorchTune](https://pytorch.org/torchtune/main/) to fine-tune Llama 3, enabling it to understand both English and Korean.
We teach the model to recognize similar embedding structures in both languages.
We used 4 $\times$ NVIDIA RTX A6000 GPUs.

### Getting Started

1. Download the Repository:
```bash
git clone https://github.com/bckim-mathai/llama3-KoBLLa.git
cd llama3-KoBLLa
```

2. Download Llama 3 Weights:
You'll need a Hugging Face access token to download these files.
```bash
tune download meta-llama/Meta-Llama-3-8B \
    --output-dir ./checkpoints/ \
    --hf-token <ACCESS TOKEN>

tune download meta-llama/Meta-Llama-3-8B-Instruct \
    --output-dir ./checkpoints/ \
    --hf-token <ACCESS TOKEN>
```

### Training the Model

We fine-tune Llama 3 in three stages:

1. Fine-tune the Base Model:
```bash
export PYTHONPATH=$(pwd)
tune run --nproc_per_node 4 lora_finetune_distributed \
    --config ./configs/finetune_base.yaml
```
This command adds the project's root directory to your `PYTHONPATH`, allowing the script to find the custom datasets used for training.

2. Apply Chat Vectors
```bash
python create_inst_init.py
```
This script prepares the model for instruction following.

3. Fine-tune the Instruct Model:
```bash
export PYTHONPATH=$(pwd)
tune run --nproc_per_node 4 lora_finetune_distributed \
    --config ./configs/finetune_base.yaml
```
This command fine-tunes the model to follow instructions effectively.

### Evaluation

One of our goals is to ensure that the model retains its ability to understand English instructions.
We are closely monitoring the performance metrics for both English and Korean.
Here's a preliminary comparison of the model's performance:

| Model | TruthfulQA MC2 | TBA |
|:---|:---:|:---:|
| Llama-3 | 0.4396 | |
| KoBLLa | 0.4304 | |
||||
| Llama-3-Inst. | 0.5170 | |
| KoBLLa + ChatVec. | 0.5144 | |
| KoBLLa-Inst. | TBA | |

As you can see, there's a slight decrease in performance on the TruthfulQA MC2 benchmark.
We're continuing to improve the model and will update these results as we make progress.