import json
import urllib.request

# FIX: Changed endpoint to /api/chat which natively handles strict structural loops
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2"  # Ollama maps llama3.2 automatically

def ask_ollama_json(prompt_str):
    """Queries the local Meta engine using the structured Chat API layout."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt_str
            }
        ],
        "stream": False,
        "format": "json"  # Enforces pure JSON output schema
    }
    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=90) as response:
            raw_res = json.loads(response.read())
        
        # Extract response from structural chat messages block
        message_content = raw_res["message"]["content"]
        return json.loads(message_content)
    except Exception as e:
        print(f"❌ Planner Error: Communication break to Ollama -> {str(e)}")
        return None

def create_plan(user_task, directory_context):
    """Builds a multi-step structured plan using the local model endpoints."""
    prompt = f"""You are the core logic planning loop for an automated system engineering agent.
    Convert the USER TASK into a sequential array of executable steps matching allowed tools.

    ALLOWED TOOL CONFIGURATIONS:
    1. 'find_latest_csv' -> args: {{}}
    2. 'extract_matching_rows' -> args: {{"keyword": "text_to_scan"}}
    3. 'save_result' -> args: {{"filename": "target_name.txt"}}

    USER TASK: {user_task}
    WORKSPACE CONTEXT DATA: {json.dumps(directory_context)}

    Return ONLY a raw valid JSON object matching this exact schema block without conversational text:
    {{
       "goal": "Clear operational goal description",
       "steps": [
          {{ "id": 1, "tool": "tool_name", "args": {{}} }}
       ]
    }}"""
    return ask_ollama_json(prompt)
