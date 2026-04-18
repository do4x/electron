"""
solve.py — traces of motion
Run from the task folder:  python solve.py
Requires: numpy, tensorflow (or tflite_runtime), requests
"""
import sys
import json
import numpy as np

SERVER = "http://34.185.197.228:32061"

# ── Phase 2: Inventory ─────────────────────────────────────────────────────

ARTIFACT_X = "data/hidden_sequence/X_sequence.npy"
ARTIFACT_Y = "data/hidden_sequence/y_sequence.npy"
MODEL_PATH  = "model/gesture_model.tflite"

# Gesture class map (from predictor.py / labels.json)
CLASSES = {0: "SHAKE", 1: "ROTATE", 2: "LEFT", 3: "RIGHT", 4: "TAP"}

# ── Phase 4: Load & predict ───────────────────────────────────────────────

def normalize(X: np.ndarray) -> np.ndarray:
    mean = X.mean(axis=1, keepdims=True)
    std  = X.std(axis=1,  keepdims=True) + 1e-8
    return ((X - mean) / std).astype(np.float32)


def load_and_predict():
    X = np.load(ARTIFACT_X)  # (7, 50, 3)

    try:
        import tflite_runtime.interpreter as tflite
        interp = tflite.Interpreter(model_path=MODEL_PATH)
    except ImportError:
        import tensorflow as tf
        interp = tf.lite.Interpreter(model_path=MODEL_PATH)

    interp.allocate_tensors()
    inp  = interp.get_input_details()
    out  = interp.get_output_details()

    X_n = normalize(X)
    preds = []
    for i in range(len(X_n)):
        interp.set_tensor(inp[0]["index"], X_n[i:i+1])
        interp.invoke()
        logits = interp.get_tensor(out[0]["index"])
        preds.append(int(np.argmax(logits, axis=1)[0]))

    return preds


# ── Phase 5: Submit to server ─────────────────────────────────────────────

def submit(preds: list):
    try:
        import requests
    except ImportError:
        print("[!] 'requests' not installed — run:  pip install requests")
        sys.exit(1)

    class_names = [CLASSES[p] for p in preds]
    print(f"[*] Predictions : {preds}")
    print(f"[*] Class names : {class_names}")

    # Try several likely API formats
    attempts = [
        ("POST", f"{SERVER}/predict",
         {"X": np.load(ARTIFACT_X).tolist()},
         "sending raw X to /predict"),

        ("POST", f"{SERVER}/submit",
         {"predictions": preds},
         "sending int list to /submit"),

        ("POST", f"{SERVER}/predict",
         {"predictions": preds},
         "sending int list to /predict"),

        ("POST", f"{SERVER}/flag",
         {"predictions": preds},
         "sending int list to /flag"),

        ("POST", f"{SERVER}/",
         {"predictions": preds},
         "sending int list to /"),

        ("POST", f"{SERVER}/predict",
         {"labels": preds},
         "sending labels to /predict"),

        ("POST", f"{SERVER}/submit",
         {"labels": class_names},
         "sending class names to /submit"),

        ("GET",  f"{SERVER}/flag",
         None,
         "GET /flag"),
    ]

    for method, url, payload, desc in attempts:
        try:
            print(f"\n[>] Trying: {desc} → {url}")
            if method == "POST":
                r = requests.post(url, json=payload, timeout=10)
            else:
                r = requests.get(url, timeout=10)
            print(f"    Status: {r.status_code}")
            print(f"    Body  : {r.text[:300]}")
            if "CTF{" in r.text or "flag" in r.text.lower():
                print(f"\n[+] FLAG FOUND: {r.text.strip()}")
                return r.text.strip()
        except requests.exceptions.ConnectionError as e:
            print(f"    Connection error: {e}")
        except requests.exceptions.Timeout:
            print(f"    Timed out")
        except Exception as e:
            print(f"    Error: {e}")

    print("\n[-] No flag found in any response. Check server manually.")
    return None


# ── Phase 5: Verify ───────────────────────────────────────────────────────

def verify(flag: str) -> bool:
    return (
        isinstance(flag, str)
        and flag.startswith("CTF{")
        and flag.endswith("}")
        and flag.isascii()
    )


def main():
    print("[*] Loading model and classifying hidden sequence...")
    preds = load_and_predict()

    print("[*] Submitting to server...")
    flag = submit(preds)

    if flag and verify(flag):
        print(f"\n{'='*50}")
        print(f"FLAG: {flag}")
        print(f"{'='*50}")
        with open("flag.txt", "w") as f:
            f.write(flag)
        print("[+] Saved to flag.txt")
    else:
        print("\n[?] Could not automatically extract flag.")
        print("    Try the PowerShell commands below manually:\n")
        print(f'    Invoke-RestMethod -Uri "{SERVER}/predict" -Method Post \\')
        print(f'      -ContentType "application/json" \\')
        print(f'      -Body (\'{{\"predictions\": {preds}}}\' | ConvertTo-Json -Compress)')
        print(f'\n    # or plain curl.exe:')
        print(f'    curl.exe -s -X POST {SERVER}/predict \\')
        print(f'      -H "Content-Type: application/json" \\')
        print(f'      -d \'{{"predictions": {preds}}}\'')


if __name__ == "__main__":
    main()
