#!/usr/bin/env python3
import os
import sys
import pathlib
import google.generativeai as genai

# === Cloud Build Guardian Script ===

# Step 1. Setup API Client and Project Root
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    # In Cloud Build, this should be set as a secret.
    print("❌ GEMINI_API_KEY not found.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()

# Step 2. Aggregate Configuration Files
def get_config_context():
    """Finds and reads the key infrastructure files."""
    files_to_read = ["cloudbuild.yaml", "Dockerfile", ".gcloudignore"]
    context = []
    print("🔍 Reading configuration files...")

    for filename in files_to_read:
        file_path = PROJECT_ROOT / filename
        if file_path.exists():
            try:
                content = file_path.read_text(encoding="utf-8")
                context.append(f"--- FILE: {filename} ---\n{content}")
                print(f"  ✅ Read {filename}")
            except Exception as e:
                context.append(f"--- FILE: {filename} ---\n[Could not read file: {e}]")
                print(f"  ⚠️ Could not read {filename}")
        else:
            print(f"  ℹ️  Skipping non-existent file: {filename}")


    if not context:
        print("❌ No configuration files found. Exiting.")
        sys.exit(1)

    return "\n\n".join(context)

# Step 3. Send to Gemini for Analysis
def analyze_configuration(config_bundle):
    """Submits the configuration bundle to the Gemini model for validation."""
    model = genai.GenerativeModel("gemini-2.5-pro")
    
    prompt = f"""
    You are a GCP Certified Cloud Architect specializing in CI/CD security and optimization.
    Your task is to analyze the following set of configuration files for a new deployment.
    
    Analyze the files for CRITICAL, BUILD-BREAKING issues. Focus on:
    1.  **Syntax Errors:** Invalid YAML in `cloudbuild.yaml` or commands in `Dockerfile`.
    2.  **Logical Flaws:** Steps in `cloudbuild.yaml` that are out of order or reference non-existent files.
    3.  **Security Vulnerabilities:** Leaking secrets, using public base images with known vulnerabilities, running as root user unnecessarily.
    4.  **Performance Inefficiencies:** Inefficient Docker layer caching, unnecessarily large build contexts due to a poor `.gcloudignore`.
    
    If you detect a critical, build-breaking issue, respond with ONLY the word "BLOCK:" followed by a concise, one-sentence explanation of the primary issue.
    
    If the configuration is valid and follows best practices, respond with ONLY the word "PASS".
    
    --- CONFIGURATION FILES ---
    {config_bundle}
    """
    
    print("🤖 Submitting configuration to Gemini for analysis...")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"BLOCK: Gemini API call failed: {e}"

# Step 4. Main Execution
def main():
    print("--- 🛡️ Cloud Build Guardian Initializing 🛡️ ---")
    config_bundle = get_config_context()
    result = analyze_configuration(config_bundle)
    
    print("\n--- Gemini Analysis Result ---")
    print(result)
    print("----------------------------")
    
    if result.startswith("BLOCK"):
        print("\n🚫 Build HALTED by Cloud Build Guardian.")
        sys.exit(1)
    elif result == "PASS":
        print("\n✅ Configuration approved. Proceeding with build.")
        sys.exit(0)
    else:
        print("\n⚠️ Guardian returned an indeterminate response. Halting build for safety.")
        sys.exit(1)

if __name__ == "__main__":
    main()
