autotrain llm --train --project-name bruh1 --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --data-path . --use-peft --batch-size 4 --epochs 10 --lr 2e-4 --trainer sft >training.log
