import json
import os
from jinja2 import Environment, FileSystemLoader

# 1. Load the mock data
def load_cbom(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# 2. Process the data (First-Principles logic)
def process_assets(cbom_data):
    assets = []
    vulnerable_count = 0
    safe_count = 0
    
    for component in cbom_data.get("components", []):
        crypto_props = component.get("cryptoProperties", {})
        algo_props = crypto_props.get("algorithmProperties", {})
        
        algorithm = algo_props.get("algorithm", "Unknown")
        primitive = algo_props.get("primitive", "Unknown")
        
        # Simple logic: RSA is vulnerable, AES is safe (for this mock)
        is_vulnerable = "RSA" in algorithm or "SHA-1" in algorithm
        
        if is_vulnerable:
            vulnerable_count += 1
        else:
            safe_count += 1
            
        assets.append({
            "name": component.get("name", "Unknown Asset"),
            "algorithm": algorithm,
            "primitive": primitive,
            "is_vulnerable": is_vulnerable
        })
        
    return assets, vulnerable_count, safe_count

# 3. Render the HTML report
def generate_report():
    print("🚀 Generating Crypto-CI Report...")
    
    # Load data
    cbom_data = load_cbom("tests/mock-cbom.json")
    assets, vulnerable, safe = process_assets(cbom_data)
    
    # Calculate a mock score (0-100)
    total = vulnerable + safe
    score = int((safe / total) * 100) if total > 0 else 0
    
    # Setup Jinja
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")
    
    # Render
    html_output = template.render(
        target_name="Acme Corp / auth-service",
        score=score,
        vulnerable_count=vulnerable,
        safe_count=safe,
        assets=assets
    )
    
    # Write to file
    os.makedirs("dist", exist_ok=True)
    with open("dist/report.html", "w") as f:
        f.write(html_output)
        
    print("✅ Report generated at dist/report.html")

if __name__ == "__main__":
    generate_report()
