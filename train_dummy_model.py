# train_dummy_model.py
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Example dataset: 5 skills, 3 course labels
X = np.array([
    [50, 60, 55, 70, 65],
    [70, 80, 75, 60, 80],
    [30, 40, 35, 50, 45],
    [85, 90, 80, 95, 90],
    [60, 55, 65, 50, 60]
])
y = np.array(['Python', 'ML', 'DataViz', 'SQL', 'Statistics'])

# Encode target labels
le = LabelEncoder()
y_enc = le.fit_transform(y)

# Train model
model = RandomForestClassifier()
model.fit(X, y_enc)

# Save model and encoder
with open('rf_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('le_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

print("rf_model.pkl and le_encoder.pkl created successfully!")
