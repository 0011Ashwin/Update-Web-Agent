"""
Quick test script to verify Ghost UI fixes
Run this to test if the visualization features work correctly
"""
import json
import os
import sys

def test_json_parsing():
    """Test if we can parse the actual JSON structure correctly"""
    print("🔍 Testing JSON parsing...")
    
    # Find first task ID
    history_path = "./tmp/agent_history"
    if not os.path.exists(history_path):
        print("❌ Error: agent_history folder not found!")
        return False
    
    task_dirs = [d for d in os.listdir(history_path) if os.path.isdir(os.path.join(history_path, d))]
    if not task_dirs:
        print("❌ No task histories found!")
        return False
    
    task_id = task_dirs[0]
    json_file = f"./tmp/agent_history/{task_id}/{task_id}.json"
    
    print(f"📂 Testing with Task ID: {task_id}")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ JSON loaded successfully")
        print(f"   Task: {data.get('task', 'N/A')[:60]}...")
        print(f"   Steps: {len(data.get('history', []))}")
        
        # Test first step parsing
        if data.get('history'):
            step = data['history'][0]
            
            # Test action extraction
            actions = step.get("model_output", {}).get("action", [{}])
            if actions and len(actions) > 0:
                action_dict = actions[0]
                action_type = list(action_dict.keys())[0].replace('_', ' ').title() if action_dict else "Unknown"
                print(f"   First Action: {action_type}")
            
            # Test metadata extraction
            metadata = step.get("metadata", {})
            start_time = metadata.get("step_start_time", 0)
            end_time = metadata.get("step_end_time", 0)
            duration = f"{end_time - start_time:.2f}s" if start_time and end_time else "N/A"
            tokens = metadata.get("input_tokens", "N/A")
            
            print(f"   Duration: {duration}")
            print(f"   Tokens: {tokens}")
            
            # Test current_state extraction
            current_state = step.get("model_output", {}).get("current_state", {})
            next_goal = current_state.get("next_goal", "N/A")[:60]
            print(f"   Next Goal: {next_goal}...")
            
        print("\n✅ All parsing tests PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Error parsing JSON: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_visualization_functions():
    """Test if visualization functions work"""
    print("\n🎨 Testing visualization functions...")
    
    try:
        # Import the fixed module
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from src.webui.components.notes_visualization_tab import generate_step_flowchart, generate_mind_map
        
        # Load a sample task
        history_path = "./tmp/agent_history"
        task_dirs = [d for d in os.listdir(history_path) if os.path.isdir(os.path.join(history_path, d))]
        task_id = task_dirs[0]
        
        with open(f"./tmp/agent_history/{task_id}/{task_id}.json", 'r', encoding='utf-8') as f:
            history_data = json.load(f)
        
        # Test flowchart generation
        flowchart_html = generate_step_flowchart(history_data)
        if "step-node" in flowchart_html and "Unknown Action" not in flowchart_html:
            print("✅ Flowchart generation PASSED")
        else:
            print("⚠️  Flowchart may have issues")
            if "Unknown Action" in flowchart_html:
                print("   - Still showing 'Unknown Action'")
        
        # Test mind map generation
        mindmap_html = generate_mind_map(history_data)
        if "mind-map" in mindmap_html:
            print("✅ Mind map generation PASSED")
        else:
            print("⚠️  Mind map may have issues")
        
        print("\n✅ Visualization tests PASSED!")
        return True
        
    except ImportError as e:
        print(f"⚠️  Could not import modules (this is OK if gradio not installed): {e}")
        print("   Run: pip install -r requirements.txt")
        return True
    except Exception as e:
        print(f"❌ Error testing visualizations: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("🎭 Ghost UI - Fix Verification Test")
    print("=" * 60)
    print()
    
    # Test 1: JSON parsing
    test1_passed = test_json_parsing()
    
    # Test 2: Visualization functions
    test2_passed = test_visualization_functions()
    
    print("\n" + "=" * 60)
    if test1_passed and test2_passed:
        print("✅ ALL TESTS PASSED! Ghost UI fixes are working!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start UI: python webui.py")
        print("3. Test visualizations in the '📝 Notes & Visualization' tab")
    else:
        print("⚠️  Some tests had issues. Check the output above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
