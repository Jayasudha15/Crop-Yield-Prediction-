import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Import models to compare
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR

# Import metrics
from sklearn.metrics import r2_score, mean_squared_error

# 1. Load and Prepare Data
df = pd.read_csv("train.csv")
df.drop(columns=['Crop_Year', 'Production'], inplace=True)

# Handle missing values (a robust way)
for col in df.columns:
    if df[col].dtype == 'object':
        df[col].fillna(df[col].mode()[0], inplace=True)
    else:
        df[col].fillna(df[col].mean(), inplace=True)

# Encode categorical features
label_encoders = {}
for col in ['Crop', 'Season', 'State']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Save the label encoders
joblib.dump(label_encoders, 'label_encoders.joblib')

# 2. Split Data into Training and Testing Sets
X = df.drop(columns=['Yield'])
y = df['Yield']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Data splitting complete.")

# 3. Define Models to Train
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
    "Support Vector Regressor (SVR)": SVR()
}

# 4. Train Models and Evaluate Performance
performance_results = {}
best_model = None
best_r2_score = -np.inf

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    performance_results[name] = {"R-squared": r2, "RMSE": rmse}
    print(f"{name} - R-squared: {r2:.4f}, RMSE: {rmse:.4f}")

    # Check if this is the best model so far
    if r2 > best_r2_score:
        best_r2_score = r2
        best_model = model

# 5. Save the Performance Results and the Best Model
print(f"\nBest performing model is {type(best_model).__name__} with an R-squared of {best_r2_score:.4f}")

# Save the performance dictionary
joblib.dump(performance_results, 'model_performance.joblib')
print("Model performance results saved to 'model_performance.joblib'")

# Save the best model
joblib.dump(best_model, 'best_model.joblib')
print(f"Best model saved to 'best_model.joblib'")