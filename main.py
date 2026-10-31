from context_engine import get_directory_context
from planner import create_plan
from executor import verify_plan_safety_ai, run_step
import json

def run_agent_loop():
    print("="*60)
    print("🤖 GHOSTOPERATOR AI: AGENTIC COMPUTER ASSISTANT ACTIVE")
    print("="*60)
    
    user_input = input("Enter automation objective: ").strip()
    if not user_input:
        print("❌ System Exit: Empty target instruction.")
        return

    print("\n[Step 1/4] Scanning local folder structure...")
    folder_context = get_directory_context()
    
    print("[Step 2/4] Querying local Meta Llama model for operational blueprint...")
    orchestration_plan = create_plan(user_input, folder_context)
    
    if not orchestration_plan or "steps" not in orchestration_plan:
        print("❌ Execution Failure: Model failed to establish a valid JSON schema plan.")
        return
        
    print("\n📋 PROPOSED STRUCTURED EXECUTION BLUEPRINT:")
    print(json.dumps(orchestration_plan, indent=2))

    print("\n[Step 3/4] Running security validation checks...")
    if not verify_plan_safety_ai(orchestration_plan):
        print("🛑 Critical Halt: Security parameters rejected execution plan chains.")
        return
    print("🛡️ Security Verification Passed.")

    user_confirm = input("\nApprove automated plan execution? (y/n): ").strip().lower()
    if user_confirm != 'y':
        print("⏭️ Execution dropped by user decision.")
        return

    print("\n[Step 4/4] Beginning automated tool execution sequence...")
    for step in orchestration_plan["steps"]:
        result = run_step(step)
        if not result.get("success"):
            print(f"💥 Runtime Exception at Step {step.get('id')}: {result.get('error')}")
            break
        else:
            print(f"➔ Status: Step Completed. Response details: {json.dumps(result)}\n")
            
    print("🏁 Sequence complete. GhostOperator agent returning to standby mode.")

if __name__ == "__main__":
    run_agent_loop()
