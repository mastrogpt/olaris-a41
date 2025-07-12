import os, sys, glob

import torch
print("torch:", torch.__version__, torch.cuda.is_available())

from dotenv import load_dotenv
load_dotenv()
print(f"HF_TOKEN is {os.getenv('HF_TOKEN') != ''}")

from datasets import load_dataset

from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template
from unsloth.save import create_ollama_modelfile
from trl import SFTConfig, SFTTrainer

from pathlib import Path

def load(folder, tokenizer):

    dataset = load_dataset("json", data_files=f"{folder}/*", split="train")
    def to_chatml(example):
        messages = example["messages"]
        text = tokenizer.apply_chat_template(messages, tokenize=False)
        return {"text": text}

    dataset = dataset.map(to_chatml, remove_columns=["messages"])

def train(folder, model_name):

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model_name,
        max_seq_length = 2048,
        dtype = None,
        load_in_4bit = True,
        # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
    )
    #tokenizer = get_chat_template(tokenizer, chat_template)
    dataset = load(folder, tokenizer)
    #print(tokenizer.chat_template)

    model = FastLanguageModel.get_peft_model(
        model,
        r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 16,
        lora_dropout = 0, # Supports any, but = 0 is optimized
        bias = "none",    # Supports any, but = "none" is optimized
        # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
        use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
        random_state = 3407,
        use_rslora = False,  # We support rank stabilized LoRA
        loftq_config = None, # And LoftQ
    )

    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = 2048,
        packing = False, # Can make training 5x faster for short sequences.
        args = SFTConfig(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            max_steps = 60,
            # num_train_epochs = 1, # For longer training runs!
            learning_rate = 2e-4,
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = "outputs",
            report_to = "none", # Use this for WandB etc
        ),
    )
    trainer_stats = trainer.train()

    folderout = f"{folder}_out"
    os.makedirs(folderout, exist_ok=True)
    #model.save_pretrained_merged(folderout, tokenizer, save_method = "merged_16bit",)
    model.save_pretrained_gguf(folderout, tokenizer)
    os.listdir(folderout)
    gguf = glob.glob(f"{folderout}/*.gguf")[0]
    Path(f"{folderout}/Modelfile").write_text(f"FROM {gguf}\n")

def main(argv):
    model_name = "unsloth/Meta-Llama-3.1-8B-Instruct"

    args = sys.argv[1:]
    if len(argv) == 0:
        print("Usage: <folder>")
        sys.exit(1)

    folder = os.path.join(os.getenv("OPS_PWD") or ".", "data", "ftpartit")
    folder = args[0]
    if not os.path.exists(folder):
        print(f"Folder {folder} does not exist.")
        sys.exit(1)
    
    train(folder, model_name)

