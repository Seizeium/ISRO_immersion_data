import pandas as pd
from transformers import BertTokenizer

# Load the scraped data
df = pd.read_csv("wikipedia_isro_data.csv")

# Initialize the tokenizer
tokenizer = BertTokenizer.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")

# Tokenize the data
df['input_ids'] = df['content'].apply(lambda x: tokenizer.encode(x, add_special_tokens=True))

# Create the dataset in the format required for training
train_data = df[['input_ids']]

# Convert to PyTorch tensors
import torch

class ISRODataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data.iloc[idx]
        return torch.tensor(item['input_ids'])

train_dataset = ISRODataset(train_data)
