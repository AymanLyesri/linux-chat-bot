import pandas as pd

# Data
data = {
    'INPUT': ['workspace 1', 'workspace 2', 'workspace 3', 'workspace 4', 'workspace 5',
              'workspace 6', 'workspace 7', 'workspace 8', 'workspace 9', 'workspace 10'],
    'OUTPUT': ['going to workspace one | hyprctl dispatch 1',
               'going to workspace two | hyprctl dispatch 2',
               'going to workspace three | hyprctl dispatch 3',
               'going to workspace four | hyprctl dispatch 4',
               'going to workspace five | hyprctl dispatch 5',
               'going to workspace six | hyprctl dispatch 6',
               'going to workspace seven | hyprctl dispatch 7',
               'going to workspace eight | hyprctl dispatch 8',
               'going to workspace nine | hyprctl dispatch 9',
               'going to workspace ten | hyprctl dispatch 10'],
}

# Create DataFrame
df = pd.DataFrame(data)

# Change the format of the 'text' column
df['text'] = df.apply(
    lambda row: f"user\n{row['INPUT']}\nassistant\n{row['OUTPUT']}\n", axis=1)

# Display DataFrame
print(df)

df.to_csv("train.csv", index=True)

print("CSV file 'train.csv' has been created.")
