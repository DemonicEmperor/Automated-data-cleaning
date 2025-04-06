from flask import Flask, render_template, request, send_file
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        missing_option = request.form.get("missing")
        remove_duplicates = request.form.get("duplicates")
        scale_option = request.form.get("scaling")
        encode_option = request.form.get("encoding")

        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Read dataset
            df = pd.read_csv(file_path) if file.filename.endswith(".csv") else pd.read_excel(file_path)

            # Handle Missing Values
            if missing_option == "drop":
                df = df.dropna()
            elif missing_option == "mean":
                df = df.fillna(df.mean(numeric_only=True))
            elif missing_option == "median":
                df = df.fillna(df.median(numeric_only=True))
            elif missing_option == "mode":
                df = df.fillna(df.mode().iloc[0])

            # Remove Duplicates
            if remove_duplicates == "yes":
                df = df.drop_duplicates()

            # Feature Scaling
            if scale_option != "none":
                scaler = MinMaxScaler() if scale_option == "minmax" else StandardScaler()
                numerical_cols = df.select_dtypes(include=['number']).columns
                df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

            # Encode Categorical Data
            if encode_option != "none":
                categorical_cols = df.select_dtypes(include=['object']).columns
                if encode_option == "onehot":
                    df = pd.get_dummies(df, columns=categorical_cols)
                else:
                    encoder = LabelEncoder()
                    for col in categorical_cols:
                        df[col] = encoder.fit_transform(df[col])

            # Save cleaned file
            cleaned_file_path = os.path.join(UPLOAD_FOLDER, "cleaned_" + file.filename)
            df.to_csv(cleaned_file_path, index=False)
            return send_file(cleaned_file_path, as_attachment=True, download_name="cleaned_data.csv")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,port=3001)

