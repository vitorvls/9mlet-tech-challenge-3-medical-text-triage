import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType

def main():
    model_path = "models/baseline.joblib"
    onnx_path = "models/baseline.onnx"
    
    print(f"Loading {model_path}...")
    model = joblib.load(model_path)
    
    print("Converting to ONNX...")
    # The pipeline expects a list/array of strings
    initial_type = [('text_input', StringTensorType([None, 1]))]
    
    # We must explicitly set options for TfidfVectorizer if needed,
    # but convert_sklearn usually handles standard TfidfVectorizer well.
    onx = convert_sklearn(model, initial_types=initial_type, target_opset=12)
    
    with open(onnx_path, "wb") as f:
        f.write(onx.SerializeToString())
        
    print(f"Saved ONNX model to {onnx_path}")

if __name__ == "__main__":
    main()
