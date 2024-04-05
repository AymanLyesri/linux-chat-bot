import json
import random
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the data
with open('your_data.json') as file:
    data = json.load(file)

# Preprocess the data
X = []
y = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        X.append(pattern)
        y.append(intent['tag'])

# Load pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased', num_labels=len(set(y)))

# Tokenize input data
X_encoded = tokenizer(X, padding=True, truncation=True, return_tensors='pt')

# Encode labels
label_map = {label: i for i, label in enumerate(set(y))}
y_encoded = torch.tensor([label_map[label] for label in y])

# Fine-tune BERT model
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
epochs = 3
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(**X_encoded, labels=y_encoded)
    loss = outputs.loss
    loss.backward()
    optimizer.step()

# Example usage


def predict_intent(user_input):
    inputs = tokenizer(user_input, padding=True,
                       truncation=True, return_tensors="pt")
    outputs = model(**inputs)
    predicted_label_idx = torch.argmax(outputs.logits[0]).item()
    predicted_label = list(label_map.keys())[list(
        label_map.values()).index(predicted_label_idx)]
    return predicted_label

# Get response based on predicted intent


def get_response(intent):
    for item in data['intents']:
        if item['tag'] == intent:
            return random.choice(item['responses']), item.get('command')


# Example usage
user_input = input("You: ")
intent = predict_intent(user_input)
response, command = get_response(intent)
print("Bot:", response)
if command:
    print("Command:", command)
