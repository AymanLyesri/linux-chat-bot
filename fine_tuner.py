from transformers import pipeline, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# Load pre-trained Llama model and tokenizer
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForConditionalGeneration.from_pretrained(model_name)

# Prepare your dataset
train_dataset = TextDataset(
    tokenizer=tokenizer, file_path="train.txt", block_size=128)
eval_dataset = TextDataset(
    tokenizer=tokenizer, file_path="eval.txt", block_size=128)

# Define training arguments and trainer
training_args = TrainingArguments(
    output_dir="./output",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=8,
    save_steps=10_000,
    save_total_limit=2,
)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
trainer.save_model("./fine-tuned-llama")
