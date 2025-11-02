"""
Enhanced Data Capture System for Ghost Agent
Automatically saves detailed step-by-step data, graphs, and notes
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class GhostDataCapture:
    """Enhanced data capture system for comprehensive task tracking"""
    
    def __init__(self, base_dir: str = "./tmp/ghost_data"):
        self.base_dir = base_dir
        self.sessions_dir = os.path.join(base_dir, "sessions")
        self.graphs_dir = os.path.join(base_dir, "graphs")
        self.notes_dir = os.path.join(base_dir, "notes")
        
        # Create directories
        for dir_path in [self.sessions_dir, self.graphs_dir, self.notes_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        self.current_session = None
        self.session_data = {}
    
    def start_session(self, task: str, metadata: Optional[Dict] = None) -> str:
        """Start a new tracking session"""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        
        self.current_session = session_id
        self.session_data = {
            "session_id": session_id,
            "task": task,
            "start_time": datetime.now().isoformat(),
            "metadata": metadata or {},
            "steps": [],
            "notes": [],
            "stats": {
                "total_steps": 0,
                "successful_actions": 0,
                "failed_actions": 0,
                "total_tokens": 0,
                "total_duration": 0
            }
        }
        
        return session_id
    
    def capture_step(self, step_num: int, step_data: Dict) -> None:
        """Capture detailed step information"""
        if not self.current_session:
            return
        
        step_record = {
            "step_number": step_num,
            "timestamp": datetime.now().isoformat(),
            "action": step_data.get("action", "Unknown"),
            "reasoning": step_data.get("reasoning", ""),
            "state": step_data.get("state", {}),
            "screenshot": step_data.get("screenshot", None),
            "success": step_data.get("success", True),
            "duration": step_data.get("duration", 0),
            "tokens": step_data.get("tokens", 0),
            "errors": step_data.get("errors", [])
        }
        
        self.session_data["steps"].append(step_record)
        self.session_data["stats"]["total_steps"] += 1
        
        if step_record["success"]:
            self.session_data["stats"]["successful_actions"] += 1
        else:
            self.session_data["stats"]["failed_actions"] += 1
        
        self.session_data["stats"]["total_tokens"] += step_record["tokens"]
        self.session_data["stats"]["total_duration"] += step_record["duration"]
        
        # Auto-save after each step
        self._save_session()
    
    def add_note(self, note: str, note_type: str = "user", metadata: Optional[Dict] = None) -> None:
        """Add a note to the current session"""
        if not self.current_session:
            return
        
        note_record = {
            "timestamp": datetime.now().isoformat(),
            "type": note_type,
            "content": note,
            "metadata": metadata or {}
        }
        
        self.session_data["notes"].append(note_record)
        self._save_session()
    
    def end_session(self, final_result: Optional[str] = None, status: str = "completed") -> str:
        """End the current session and finalize data"""
        if not self.current_session:
            return ""
        
        self.session_data["end_time"] = datetime.now().isoformat()
        self.session_data["final_result"] = final_result
        self.session_data["status"] = status
        
        # Calculate final stats
        if self.session_data["steps"]:
            start_time = datetime.fromisoformat(self.session_data["start_time"])
            end_time = datetime.fromisoformat(self.session_data["end_time"])
            self.session_data["stats"]["total_duration"] = (end_time - start_time).total_seconds()
        
        # Save final session data
        session_file = self._save_session()
        
        # Generate summary report
        self._generate_summary_report()
        
        # Generate graph data
        self._generate_graph_data()
        
        session_id = self.current_session
        self.current_session = None
        
        return session_file
    
    def _save_session(self) -> str:
        """Save current session data to file"""
        if not self.current_session:
            return ""
        
        session_file = os.path.join(
            self.sessions_dir,
            f"{self.current_session}.json"
        )
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)
        
        return session_file
    
    def _generate_summary_report(self) -> str:
        """Generate a human-readable summary report"""
        if not self.current_session:
            return ""
        
        report_file = os.path.join(
            self.sessions_dir,
            f"{self.current_session}_summary.md"
        )
        
        stats = self.session_data["stats"]
        success_rate = (stats["successful_actions"] / max(stats["total_steps"], 1)) * 100
        
        report = f"""# 👻 Ghost Agent Session Report

## Session Information
- **Session ID**: {self.current_session}
- **Task**: {self.session_data["task"]}
- **Start Time**: {self.session_data["start_time"]}
- **End Time**: {self.session_data.get("end_time", "N/A")}
- **Status**: {self.session_data.get("status", "In Progress")}

## Statistics
- **Total Steps**: {stats["total_steps"]}
- **Successful Actions**: {stats["successful_actions"]}
- **Failed Actions**: {stats["failed_actions"]}
- **Success Rate**: {success_rate:.2f}%
- **Total Tokens Used**: {stats["total_tokens"]:,}
- **Total Duration**: {stats["total_duration"]:.2f} seconds

## Step-by-Step Breakdown

"""
        
        for step in self.session_data["steps"]:
            status_icon = "✅" if step["success"] else "❌"
            report += f"""### Step {step['step_number']} {status_icon}
- **Action**: {step['action']}
- **Reasoning**: {step['reasoning'][:200]}...
- **Duration**: {step['duration']:.2f}s
- **Tokens**: {step['tokens']}

"""
        
        if self.session_data["notes"]:
            report += "\n## Notes\n\n"
            for note in self.session_data["notes"]:
                report += f"- **[{note['type']}]** {note['content']}\n"
        
        report += f"\n## Final Result\n\n{self.session_data.get('final_result', 'No final result recorded')}\n"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report_file
    
    def _generate_graph_data(self) -> str:
        """Generate data for graph visualization"""
        if not self.current_session:
            return ""
        
        graph_file = os.path.join(
            self.graphs_dir,
            f"{self.current_session}_graph.json"
        )
        
        # Prepare graph data
        graph_data = {
            "session_id": self.current_session,
            "task": self.session_data["task"],
            "nodes": [],
            "edges": [],
            "timeline": []
        }
        
        # Create nodes for each step
        for idx, step in enumerate(self.session_data["steps"]):
            node = {
                "id": f"step_{idx}",
                "label": f"Step {step['step_number']}",
                "action": step["action"],
                "success": step["success"],
                "duration": step["duration"],
                "tokens": step["tokens"]
            }
            graph_data["nodes"].append(node)
            
            # Create edge to next step
            if idx < len(self.session_data["steps"]) - 1:
                edge = {
                    "from": f"step_{idx}",
                    "to": f"step_{idx + 1}",
                    "weight": step["duration"]
                }
                graph_data["edges"].append(edge)
            
            # Add to timeline
            timeline_entry = {
                "step": step['step_number'],
                "timestamp": step["timestamp"],
                "action": step["action"],
                "duration": step["duration"],
                "success": step["success"]
            }
            graph_data["timeline"].append(timeline_entry)
        
        # Save graph data
        with open(graph_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        return graph_file
    
    def load_session(self, session_id: str) -> Optional[Dict]:
        """Load a previous session"""
        session_file = os.path.join(self.sessions_dir, f"{session_id}.json")
        
        if not os.path.exists(session_file):
            return None
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return None
    
    def list_sessions(self, limit: int = 10) -> List[Dict]:
        """List recent sessions"""
        sessions = []
        
        for file in sorted(os.listdir(self.sessions_dir), reverse=True):
            if file.endswith('.json') and not file.endswith('_graph.json'):
                session_file = os.path.join(self.sessions_dir, file)
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        sessions.append({
                            "session_id": data.get("session_id"),
                            "task": data.get("task"),
                            "start_time": data.get("start_time"),
                            "status": data.get("status", "Unknown"),
                            "total_steps": data.get("stats", {}).get("total_steps", 0)
                        })
                except:
                    continue
                
                if len(sessions) >= limit:
                    break
        
        return sessions


# Global instance
ghost_capture = GhostDataCapture()
