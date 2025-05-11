# Feature Relationship Anomaly Detection 🔍

Detect weird combinations of features that shouldn't exist together, even if individual values look normal!

## 🧩 How It Works

### 1. Learn Normal Patterns
For each category (e.g., Dogs vs Werewolves):

```plaintext
          | Avg Size | Avg Legs | Common Color
----------|----------|----------|-------------
🐶 Dogs    | 10cm     | 4        | Brown       
🐺 Werewolves | 100cm   | 2        | Gray
