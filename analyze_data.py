# analyze_data.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load audio features
audio_features = pd.read_csv('audio_features.csv')

# Plot energy distribution
plt.figure(figsize=(10, 6))
sns.histplot(audio_features['energy'], bins=20, kde=True)
plt.title('Energy Distribution')
plt.xlabel('Energy')
plt.ylabel('Frequency')
plt.show()

# Plot mood (valence) distribution
plt.figure(figsize=(10, 6))
sns.histplot(audio_features['valence'], bins=20, kde=True)
plt.title('Mood (Valence) Distribution')
plt.xlabel('Valence')
plt.ylabel('Frequency')
plt.show()