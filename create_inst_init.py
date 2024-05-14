import torch

base = torch.load("./checkpoints/Meta-Llama-3-8B/original/consolidated.00.pth")
inst = torch.load("./checkpoints/Meta-Llama-3-8B-Instruct/original/consolidated.00.pth")

assert base.keys() == inst.keys()

chat_vec = {k: v-base[k] for k,v in inst.items()}

del base
del inst

koblla = torch.load("./checkpoints/Llama-3-KoBLLa/meta_model_6.pt")

assert koblla.keys() == chat_vec.keys()

koblla_inst_init = {k: koblla[k]+v for k,v in chat_vec.items()}
torch.save(koblla_inst_init, "./checkpoints/Llama-3-KoBLLa-Instruct/meta_model_init.pt")

print("Created instruct model's initial weights:\n\t./checkpoints/Llama-3-KoBLLa-Instruct/meta_model_init.pt")
