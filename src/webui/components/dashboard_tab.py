"""
Dashboard Tab - Provides visualization and analytics for agent tasks
"""
import gradio as gr
import json
import os
from datetime import datetime
from typing import Dict, List
from src.webui.webui_manager import WebuiManager


def load_task_analytics(history_path: str = "./tmp/agent_history") -> Dict:
    """Load analytics data from agent history files"""
    analytics = {
        "total_tasks": 0,
        "successful_tasks": 0,
        "failed_tasks": 0,
        "total_steps": 0,
        "total_duration": 0,
        "total_tokens": 0,
        "tasks_by_date": {},
        "recent_tasks": []
    }
    
    if not os.path.exists(history_path):
        return analytics
    
    for task_dir in os.listdir(history_path):
        task_path = os.path.join(history_path, task_dir)
        if os.path.isdir(task_path):
            history_file = os.path.join(task_path, f"{task_dir}.json")
            if os.path.exists(history_file):
                try:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        analytics["total_tasks"] += 1
                        
                        # Count steps
                        if "history" in data:
                            analytics["total_steps"] += len(data["history"])
                        
                        # Get task info
                        if "final_result" in data:
                            if data["final_result"]:
                                analytics["successful_tasks"] += 1
                            else:
                                analytics["failed_tasks"] += 1
                        
                        # Add to recent tasks
                        task_info = {
                            "id": task_dir,
                            "task": data.get("task", "Unknown"),
                            "status": "Success" if data.get("final_result") else "Failed",
                            "steps": len(data.get("history", [])),
                            "timestamp": os.path.getctime(history_file)
                        }
                        analytics["recent_tasks"].append(task_info)
                        
                except Exception as e:
                    print(f"Error loading task history {history_file}: {e}")
    
    # Sort recent tasks by timestamp
    analytics["recent_tasks"] = sorted(
        analytics["recent_tasks"], 
        key=lambda x: x["timestamp"], 
        reverse=True
    )[:10]
    
    return analytics


def generate_dashboard_html(analytics: Dict) -> str:
    """Generate HTML for dashboard visualization"""
    html = f"""
    <div style="font-family: 'Exo 2', sans-serif; color: #e0e0ff;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
            
            <!-- Total Tasks Card -->
            <div style="background: linear-gradient(135deg, rgba(117, 70, 242, 0.2), rgba(70, 117, 242, 0.1)); 
                        padding: 25px; border-radius: 16px; border: 1px solid #4c3ba1; 
                        box-shadow: 0 5px 15px rgba(117, 70, 242, 0.2);">
                <div style="font-size: 14px; opacity: 0.8; margin-bottom: 10px;">Total Tasks</div>
                <div style="font-size: 36px; font-weight: 700; color: #7546f2;">{analytics['total_tasks']}</div>
            </div>
            
            <!-- Successful Tasks Card -->
            <div style="background: linear-gradient(135deg, rgba(40, 200, 120, 0.2), rgba(30, 150, 90, 0.1)); 
                        padding: 25px; border-radius: 16px; border: 1px solid #28c878; 
                        box-shadow: 0 5px 15px rgba(40, 200, 120, 0.2);">
                <div style="font-size: 14px; opacity: 0.8; margin-bottom: 10px;">Successful</div>
                <div style="font-size: 36px; font-weight: 700; color: #28c878;">{analytics['successful_tasks']}</div>
            </div>
            
            <!-- Failed Tasks Card -->
            <div style="background: linear-gradient(135deg, rgba(242, 70, 70, 0.2), rgba(200, 50, 50, 0.1)); 
                        padding: 25px; border-radius: 16px; border: 1px solid #f24646; 
                        box-shadow: 0 5px 15px rgba(242, 70, 70, 0.2);">
                <div style="font-size: 14px; opacity: 0.8; margin-bottom: 10px;">Failed</div>
                <div style="font-size: 36px; font-weight: 700; color: #f24646;">{analytics['failed_tasks']}</div>
            </div>
            
            <!-- Total Steps Card -->
            <div style="background: linear-gradient(135deg, rgba(242, 186, 70, 0.2), rgba(200, 150, 50, 0.1)); 
                        padding: 25px; border-radius: 16px; border: 1px solid #f2ba46; 
                        box-shadow: 0 5px 15px rgba(242, 186, 70, 0.2);">
                <div style="font-size: 14px; opacity: 0.8; margin-bottom: 10px;">Total Steps</div>
                <div style="font-size: 36px; font-weight: 700; color: #f2ba46;">{analytics['total_steps']}</div>
            </div>
        </div>
        
        <!-- Success Rate Progress Bar -->
        <div style="background: rgba(34, 34, 47, 0.8); padding: 20px; border-radius: 16px; 
                    border: 1px solid #4c3ba1; margin-bottom: 20px;">
            <div style="font-size: 16px; margin-bottom: 10px; font-weight: 500;">Success Rate</div>
            <div style="background: rgba(76, 59, 161, 0.3); height: 30px; border-radius: 15px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #7546f2, #28c878); 
                            height: 100%; width: {(analytics['successful_tasks'] / max(analytics['total_tasks'], 1)) * 100}%; 
                            transition: width 0.5s ease; display: flex; align-items: center; justify-content: center; 
                            color: white; font-weight: 600; font-size: 14px;">
                    {int((analytics['successful_tasks'] / max(analytics['total_tasks'], 1)) * 100)}%
                </div>
            </div>
        </div>
    </div>
    """
    return html


def generate_recent_tasks_table(analytics: Dict) -> str:
    """Generate HTML table for recent tasks"""
    if not analytics["recent_tasks"]:
        return "<div style='text-align: center; padding: 40px; color: #888;'>No recent tasks found</div>"
    
    rows = ""
    for task in analytics["recent_tasks"]:
        status_color = "#28c878" if task["status"] == "Success" else "#f24646"
        timestamp = datetime.fromtimestamp(task["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        
        rows += f"""
        <tr style="border-bottom: 1px solid rgba(76, 59, 161, 0.3);">
            <td style="padding: 15px; color: #e0e0ff;">{task['task'][:50]}...</td>
            <td style="padding: 15px; text-align: center;">
                <span style="background: {status_color}; color: white; padding: 4px 12px; 
                             border-radius: 12px; font-size: 12px; font-weight: 600;">
                    {task['status']}
                </span>
            </td>
            <td style="padding: 15px; text-align: center; color: #7546f2; font-weight: 600;">{task['steps']}</td>
            <td style="padding: 15px; color: #888; font-size: 12px;">{timestamp}</td>
        </tr>
        """
    
    html = f"""
    <div style="font-family: 'Exo 2', sans-serif; overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; 
                      background: rgba(34, 34, 47, 0.6); border-radius: 16px;">
            <thead>
                <tr style="background: rgba(117, 70, 242, 0.2); border-bottom: 2px solid #7546f2;">
                    <th style="padding: 15px; text-align: left; color: #e0e0ff; font-weight: 600;">Task</th>
                    <th style="padding: 15px; text-align: center; color: #e0e0ff; font-weight: 600;">Status</th>
                    <th style="padding: 15px; text-align: center; color: #e0e0ff; font-weight: 600;">Steps</th>
                    <th style="padding: 15px; text-align: left; color: #e0e0ff; font-weight: 600;">Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
    """
    return html


def refresh_dashboard() -> tuple:
    """Refresh dashboard data"""
    analytics = load_task_analytics()
    dashboard_html = generate_dashboard_html(analytics)
    recent_tasks_html = generate_recent_tasks_table(analytics)
    return dashboard_html, recent_tasks_html


def create_dashboard_tab(webui_manager: WebuiManager):
    """Create the dashboard tab with analytics and visualization"""
    
    tab_components = {}
    
    with gr.Column():
        gr.Markdown(
            """
            ### 📊 Ghost Dashboard
            #### Real-time analytics and task visualization
            """,
            elem_classes=["tab-header-text"]
        )
        
        refresh_btn = gr.Button("🔄 Refresh Dashboard", variant="primary", size="sm")
        
        with gr.Row():
            dashboard_display = gr.HTML(
                value=generate_dashboard_html(load_task_analytics()),
                label="Analytics Overview"
            )
        
        gr.Markdown("### 📋 Recent Tasks")
        recent_tasks_display = gr.HTML(
            value=generate_recent_tasks_table(load_task_analytics()),
            label="Recent Tasks"
        )
        
        # Add visualization placeholder for future graphs
        with gr.Accordion("📈 Advanced Analytics (Coming Soon)", open=False):
            gr.Markdown("""
            Future features:
            - Task success rate over time (line chart)
            - Steps per task distribution (bar chart)
            - Token usage analytics
            - Performance metrics
            """)
    
    tab_components.update(
        dict(
            refresh_btn=refresh_btn,
            dashboard_display=dashboard_display,
            recent_tasks_display=recent_tasks_display
        )
    )
    
    webui_manager.add_components("dashboard", tab_components)
    
    # Event handlers
    refresh_btn.click(
        fn=refresh_dashboard,
        inputs=None,
        outputs=[dashboard_display, recent_tasks_display]
    )
    
    return tab_components
