import os
import subprocess
import sys

PROJECTS = [
    "01_customer_segmentation",
    "02_sales_performance_dashboard",
    "03_social_media_sentiment",
    "04_sales_demand_forecasting",
    "05_marketing_campaign_analysis",
    "06_email_fraud_detection",
    "07_house_price_prediction",
    "08_medical_diagnosis_deep_learning",
    "09_netflix_recommendation_system",
    "10_music_genre_classification",
]

def run_script(project_dir, script_name):
    script_path = os.path.join(project_dir, script_name)
    if not os.path.exists(script_path):
        print(f"[-] Script not found: {script_path}")
        return False
    
    print(f"[*] Running {script_name} in {project_dir}...")
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print(f"[+] Success: {script_name} completed in {project_dir}")
            return True
        else:
            print(f"[-] Error in {script_path}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[-] Failed to execute {script_path}: {e}")
        return False

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    success_count = 0
    total_scripts = 0
    
    for project in PROJECTS:
        project_path = os.path.join(base_dir, project)
        if not os.path.isdir(project_path):
            print(f"[-] Project directory not found: {project}")
            continue
            
        total_scripts += 2
        gen_ok = run_script(project_path, "generate_data.py")
        ana_ok = False
        if gen_ok:
            ana_ok = run_script(project_path, "analysis.py")
            
        if gen_ok and ana_ok:
            success_count += 2
        elif gen_ok:
            success_count += 1
            
    print("\n" + "="*50)
    print(f"Verification completed. Success rate: {success_count}/{total_scripts} scripts executed successfully.")
    print("="*50)

if __name__ == "__main__":
    main()
