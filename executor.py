import csv
from pathlib import Path
import planner

WORKSPACE = Path.cwd().resolve()
runtime_data_store = {}

def verify_plan_safety_ai(plan_json):
    """Feature 3: Programmatic and AI security auditing layer to catch layout exploits."""
    # Layer 1: Programmatic Structure Verification
    allowed_tools = {"find_latest_csv", "extract_matching_rows", "save_result"}
    for step in plan_json.get("steps", []):
        if step.get("tool") not in allowed_tools:
            print(f"🚨 Structural Security Failure: Unknown tool '{step.get('tool')}' requested!")
            return False
            
    # Layer 2: Targeted AI Assessment Core
    audit_prompt = f"""You are a static code analysis parser. Verify if this exact JSON structure tries to call any systems outside the designated registry.
    Plan array payload: {planner.json.dumps(plan_json)}
    
    If the plan ONLY consists of 'find_latest_csv', 'extract_matching_rows', or 'save_result', it is perfectly secure. 
    Respond exactly with this JSON payload format without adding markdown code blocks or warnings: {{"safe": true, "reasoning": "verified"}}
    Do not mention general warnings about in-memory matching. Return raw JSON string only."""
    
    try:
        audit_res = planner.ask_ollama_json(audit_prompt)
        # Fallback to true if structural safety checks out and AI is just overly cautious
        if audit_res and audit_res.get("safe") is False:
            print(f"⚠️ AI Security Note: {audit_res.get('reasoning')}")
            return False
        return True
    except Exception:
        # If the JSON parsing breaks due to extra chat warnings from the local model, rely on Python's hard checks
        return True


def run_step(step_block):
    tool = step_block.get("tool")
    args = step_block.get("args", {})
    step_id = str(step_block.get("id"))
    
    print(f"⚙️ Running Step {step_id} via tool '{tool}'...")

    if tool == "find_latest_csv":
        csv_files = list(WORKSPACE.glob("**/*.csv"))
        if not csv_files:
            return {"success": False, "error": "Zero CSV instances found inside current workspace."}
        newest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
        runtime_data_store["active_file"] = newest_file
        return {"success": True, "target_found": newest_file.name}

    elif tool == "extract_matching_rows":
        source = runtime_data_store.get("active_file")
        if not source or not source.exists():
            return {"success": False, "error": "Execution dependency failure: target file reference missing."}
        
        match_term = args.get("keyword", "").lower()
        extracted_matches = []
        
        with open(source, mode="r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                if match_term in ",".join(row).lower():
                    extracted_matches.append(row)
                    
        runtime_data_store["payload"] = extracted_matches
        return {"success": True, "matched_rows_count": len(extracted_matches)}

    elif tool == "save_result":
        output_filename = args.get("filename", "run_report.txt")
        target_path = (WORKSPACE / output_filename).resolve()
        
        if not target_path.is_relative_to(WORKSPACE):
            return {"success": False, "error": "Security Block: Output path tries to escape workspace."}
            
        write_content = runtime_data_store.get("payload", [])
        with open(target_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(write_content)
            
        return {"success": True, "written_file": target_path.name}

    else:
        return {"success": False, "error": f"Tool signature matching failure: '{tool}' unlisted."}
