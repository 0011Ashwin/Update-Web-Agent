"""
Visualization Tab - Advanced step-by-step visualization with dynamic flowcharts and AI-powered mind maps
"""
import gradio as gr
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from src.webui.webui_manager import WebuiManager


def generate_step_flowchart(history_data: Dict) -> str:
    """Generate an enhanced dynamic visual flowchart of agent steps with animations"""
    if not history_data or "history" not in history_data:
        return "<div style='text-align: center; padding: 40px; color: #888;'>No step data available</div>"
    
    steps = history_data["history"]
    task_name = history_data.get("task", "Task Execution")
    
    html = f"""
    <div style="font-family: 'Exo 2', sans-serif; padding: 20px; max-width: 1400px; margin: 0 auto;">
        <style>
            .flowchart-container {{
                position: relative;
                padding: 30px 0;
            }}
            
            .task-header {{
                background: linear-gradient(135deg, #7546f2, #9046f2);
                color: white;
                padding: 25px 35px;
                border-radius: 20px;
                font-size: 24px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 50px;
                box-shadow: 0 10px 40px rgba(117, 70, 242, 0.5);
                animation: slideDown 0.6s ease-out;
                position: relative;
                overflow: hidden;
            }}
            
            .task-header::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
                transform: rotate(45deg);
                animation: shimmer 3s infinite;
            }}
            
            .step-timeline {{
                position: relative;
                margin-left: 80px;
            }}
            
            .step-node {{
                background: linear-gradient(135deg, rgba(117, 70, 242, 0.15), rgba(70, 117, 242, 0.08));
                border: 3px solid #7546f2;
                border-radius: 20px;
                padding: 30px;
                margin: 30px 0;
                position: relative;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                animation: fadeInRight 0.6s ease-out;
                cursor: pointer;
            }}
            
            .step-node:hover {{
                transform: translateX(15px) scale(1.02);
                box-shadow: 0 15px 40px rgba(117, 70, 242, 0.5);
                border-color: #9046f2;
                background: linear-gradient(135deg, rgba(117, 70, 242, 0.25), rgba(70, 117, 242, 0.15));
            }}
            
            .step-connector {{
                position: absolute;
                left: 50px;
                top: 100%;
                width: 4px;
                height: 60px;
                background: linear-gradient(180deg, #7546f2 0%, #9046f2 50%, #7546f2 100%);
                animation: growDown 0.5s ease-out;
                box-shadow: 0 0 10px rgba(117, 70, 242, 0.5);
            }}
            
            .step-connector::before {{
                content: '';
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                width: 0;
                height: 0;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 12px solid #9046f2;
                filter: drop-shadow(0 2px 4px rgba(117, 70, 242, 0.5));
            }}
            
            .step-number {{
                position: absolute;
                left: -80px;
                top: 50%;
                transform: translateY(-50%);
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #7546f2, #9046f2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                font-size: 24px;
                color: white;
                box-shadow: 0 5px 20px rgba(117, 70, 242, 0.6);
                border: 4px solid rgba(19, 19, 31, 0.9);
                animation: pulse 2s ease-in-out infinite;
            }}
            
            .step-header {{
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 15px;
            }}
            
            .step-icon {{
                font-size: 32px;
                filter: drop-shadow(0 2px 4px rgba(117, 70, 242, 0.5));
            }}
            
            .step-title {{
                font-size: 22px;
                font-weight: 700;
                color: #e0e0ff;
                flex: 1;
            }}
            
            .step-status {{
                padding: 6px 16px;
                background: linear-gradient(135deg, #28c878, #20a860);
                color: white;
                border-radius: 20px;
                font-size: 13px;
                font-weight: 600;
                box-shadow: 0 2px 8px rgba(40, 200, 120, 0.4);
            }}
            
            .step-content {{
                color: #c0c0dd;
                font-size: 16px;
                line-height: 1.8;
                margin: 15px 0;
                padding: 20px;
                background: rgba(34, 34, 47, 0.5);
                border-radius: 12px;
                border-left: 4px solid #7546f2;
            }}
            
            .step-details {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }}
            
            .detail-card {{
                background: rgba(76, 59, 161, 0.15);
                padding: 15px 20px;
                border-radius: 12px;
                border: 1px solid rgba(117, 70, 242, 0.3);
                transition: all 0.3s ease;
            }}
            
            .detail-card:hover {{
                background: rgba(76, 59, 161, 0.25);
                border-color: #7546f2;
                transform: translateY(-2px);
            }}
            
            .detail-label {{
                font-size: 12px;
                color: #888;
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .detail-value {{
                font-size: 18px;
                font-weight: 600;
                color: #7546f2;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .action-badge {{
                display: inline-block;
                padding: 4px 12px;
                background: rgba(117, 70, 242, 0.2);
                border: 1px solid #7546f2;
                border-radius: 8px;
                font-size: 13px;
                color: #b0b0ff;
                margin-top: 10px;
            }}
            
            @keyframes fadeInRight {{
                from {{
                    opacity: 0;
                    transform: translateX(-30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateX(0);
                }}
            }}
            
            @keyframes slideDown {{
                from {{
                    opacity: 0;
                    transform: translateY(-30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            @keyframes growDown {{
                from {{
                    height: 0;
                    opacity: 0;
                }}
                to {{
                    height: 60px;
                    opacity: 1;
                }}
            }}
            
            @keyframes pulse {{
                0%, 100% {{
                    box-shadow: 0 5px 20px rgba(117, 70, 242, 0.6);
                }}
                50% {{
                    box-shadow: 0 5px 30px rgba(117, 70, 242, 0.9);
                }}
            }}
            
            @keyframes shimmer {{
                0% {{
                    transform: translateX(-100%) translateY(-100%) rotate(45deg);
                }}
                100% {{
                    transform: translateX(100%) translateY(100%) rotate(45deg);
                }}
            }}
        </style>
        
        <div class="flowchart-container">
            <div class="task-header">
                👻 {task_name}
            </div>
            
            <div class="step-timeline">
    """
    
    # Icon mapping for different action types
    icon_map = {
        'search': '🔍',
        'click': '👆',
        'open': '🌐',
        'go': '🚀',
        'extract': '📝',
        'input': '⌨️',
        'scroll': '📜',
        'wait': '⏳',
        'navigate': '🧭',
        'type': '✍️',
        'select': '☑️',
        'default': '⚡'
    }
    
    for idx, step in enumerate(steps, 1):
        # Extract action - handle different action types
        actions = step.get("model_output", {}).get("action", [{}])
        if actions and len(actions) > 0:
            action_dict = actions[0]
            action_key = list(action_dict.keys())[0] if action_dict else "unknown"
            action_type = action_key.replace('_', ' ').title()
        else:
            action_type = "Unknown Action"
            action_key = "default"
        
        # Get icon for action
        icon = icon_map.get(action_key.split('_')[0].lower(), icon_map['default'])
        
        # Get reasoning from current_state
        current_state = step.get("model_output", {}).get("current_state", {})
        evaluation = current_state.get("evaluation_previous_goal", "")
        memory = current_state.get("memory", "")
        next_goal = current_state.get("next_goal", "")
        
        # Get result content for display
        result = step.get("result", [{}])
        result_content = ""
        if result and len(result) > 0:
            result_content = result[0].get("extracted_content", "")
        
        # Choose best description
        description = result_content or next_goal or memory or "Processing step..."
        
        # Extract metadata
        metadata = step.get("metadata", {})
        start_time = metadata.get("step_start_time", 0)
        end_time = metadata.get("step_end_time", 0)
        duration = f"{end_time - start_time:.2f}s" if start_time and end_time else "N/A"
        tokens = metadata.get("input_tokens", "N/A")
        step_number = metadata.get("step_number", idx)
        
        html += f"""
        <div class="step-node" style="animation-delay: {idx * 0.1}s;">
            <div class="step-number">{idx}</div>
            
            <div class="step-header">
                <div class="step-icon">{icon}</div>
                <div class="step-title">{action_type}</div>
                <div class="step-status">✓ Complete</div>
            </div>
            
            <div class="step-content">
                {description[:300]}{'...' if len(description) > 300 else ''}
            </div>
            
            <div class="step-details">
                <div class="detail-card">
                    <div class="detail-label">Duration</div>
                    <div class="detail-value">⏱️ {duration}</div>
                </div>
                <div class="detail-card">
                    <div class="detail-label">Tokens Used</div>
                    <div class="detail-value">🎫 {tokens}</div>
                </div>
                <div class="detail-card">
                    <div class="detail-label">Step Number</div>
                    <div class="detail-value">📍 {step_number}</div>
                </div>
            </div>
            
            <div class="action-badge">Action: {action_key}</div>
        </div>
        """
        
        if idx < len(steps):
            html += f'<div class="step-connector" style="animation-delay: {idx * 0.1 + 0.05}s;"></div>'
    
    html += """
            </div>
        </div>
    </div>
    """
    
    return html


def analyze_task_structure(history_data: Dict) -> Dict:
    """Analyze task structure to create intelligent groupings for mind map"""
    if not history_data or "history" not in history_data:
        return {}
    
    steps = history_data["history"]
    task = history_data.get("task", "Unknown Task")
    
    # Group steps by action type
    action_groups = {}
    for idx, step in enumerate(steps, 1):
        actions = step.get("model_output", {}).get("action", [{}])
        if actions and len(actions) > 0:
            action_dict = actions[0]
            action_key = list(action_dict.keys())[0] if action_dict else "unknown"
            action_category = action_key.split('_')[0]  # e.g., 'click', 'search', 'open'
            
            if action_category not in action_groups:
                action_groups[action_category] = []
            
            action_groups[action_category].append({
                'step_num': idx,
                'action': action_key.replace('_', ' ').title(),
                'description': step.get("model_output", {}).get("current_state", {}).get("next_goal", "")[:80]
            })
    
    return {
        'task': task,
        'total_steps': len(steps),
        'action_groups': action_groups,
        'complexity': 'High' if len(steps) > 10 else 'Medium' if len(steps) > 5 else 'Low'
    }


def generate_mind_map(history_data: Dict) -> str:
    """Generate an AI-powered mind map with SVG connections and detailed explanations"""
    if not history_data:
        return "<div style='text-align: center; padding: 40px; color: #888;'>No data available</div>"
    
    # Analyze task structure
    analysis = analyze_task_structure(history_data)
    task = analysis.get('task', 'Unknown Task')
    action_groups = analysis.get('action_groups', {})
    total_steps = analysis.get('total_steps', 0)
    complexity = analysis.get('complexity', 'Low')
    
    # Calculate dynamic height based on number of groups
    num_groups = len(action_groups)
    min_height = 900 + (num_groups * 200)  # Increase height based on groups
    
    html = f"""
    <div style="font-family: 'Exo 2', sans-serif; padding: 30px; max-width: 1800px; margin: 0 auto;">
        <style>
            .mindmap-container {{
                position: relative;
                min-height: {min_height}px;
                background: linear-gradient(135deg, rgba(19, 19, 31, 0.9), rgba(34, 34, 47, 0.8));
                border-radius: 30px;
                padding: 50px;
                overflow: visible;
            }}
            
            .central-node {{
                position: absolute;
                left: 50%;
                top: 150px;
                transform: translateX(-50%);
                background: linear-gradient(135deg, #7546f2, #9046f2);
                color: white;
                padding: 40px 50px;
                border-radius: 25px;
                font-size: 24px;
                font-weight: 800;
                box-shadow: 0 15px 50px rgba(117, 70, 242, 0.7);
                z-index: 10;
                animation: pulse-glow 3s ease-in-out infinite;
                max-width: 500px;
                text-align: center;
            }}
            
            .central-node::before {{
                content: '';
                position: absolute;
                inset: -3px;
                background: linear-gradient(45deg, #7546f2, #9046f2, #7546f2);
                border-radius: 25px;
                z-index: -1;
                animation: rotate-border 3s linear infinite;
                opacity: 0.6;
            }}
            
            .complexity-badge {{
                position: absolute;
                top: 10px;
                right: 10px;
                padding: 5px 15px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
            }}
            
            .branch-container {{
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
            }}
            
            .branch-group {{
                position: absolute;
                width: 350px;
                animation: fadeIn 0.6s ease-out;
            }}
            
            .branch-title {{
                background: linear-gradient(135deg, rgba(117, 70, 242, 0.4), rgba(70, 117, 242, 0.25));
                border: 3px solid #7546f2;
                border-radius: 20px;
                padding: 22px 28px;
                margin-bottom: 18px;
                font-size: 21px;
                font-weight: 700;
                color: #e0e0ff;
                box-shadow: 0 10px 30px rgba(117, 70, 242, 0.5);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            .branch-title::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
                transition: left 0.5s ease;
            }}
            
            .branch-title:hover {{
                transform: scale(1.08) translateY(-5px);
                box-shadow: 0 15px 40px rgba(117, 70, 242, 0.7);
                border-color: #9046f2;
            }}
            
            .branch-title:hover::before {{
                left: 100%;
            }}
            
            .branch-step {{
                background: linear-gradient(135deg, rgba(34, 34, 47, 0.95), rgba(44, 44, 57, 0.9));
                border: 2px solid rgba(117, 70, 242, 0.4);
                border-radius: 14px;
                padding: 16px 22px;
                margin-bottom: 12px;
                transition: all 0.3s ease;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }}
            
            .branch-step:hover {{
                background: linear-gradient(135deg, rgba(117, 70, 242, 0.2), rgba(70, 117, 242, 0.15));
                border-color: #7546f2;
                transform: translateX(12px) scale(1.02);
                box-shadow: 0 6px 18px rgba(117, 70, 242, 0.4);
            }}
            
            .step-num {{
                display: inline-block;
                width: 32px;
                height: 32px;
                background: linear-gradient(135deg, #7546f2, #9046f2);
                border-radius: 50%;
                text-align: center;
                line-height: 32px;
                font-weight: 800;
                font-size: 15px;
                margin-right: 12px;
                box-shadow: 0 3px 8px rgba(117, 70, 242, 0.5);
            }}
            
            .step-action {{
                color: #b0b0ff;
                font-weight: 700;
                font-size: 15px;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
            }}
            
            .step-desc {{
                color: #999;
                font-size: 13px;
                line-height: 1.5;
                padding-left: 44px;
            }}
            
            .connection-line {{
                position: absolute;
                background: linear-gradient(90deg, #7546f2, transparent);
                height: 2px;
                transform-origin: left center;
                pointer-events: none;
                opacity: 0.6;
            }}
            
            .stats-panel {{
                position: absolute;
                bottom: 30px;
                right: 30px;
                background: linear-gradient(135deg, rgba(34, 34, 47, 0.98), rgba(44, 44, 57, 0.95));
                border: 3px solid #7546f2;
                border-radius: 18px;
                padding: 25px;
                min-width: 220px;
                box-shadow: 0 10px 30px rgba(117, 70, 242, 0.4);
                animation: fadeIn 0.8s ease-out 0.5s both;
            }}
            
            .stat-item {{
                display: flex;
                justify-content: space-between;
                margin: 12px 0;
                color: #e0e0ff;
                padding: 8px 0;
                border-bottom: 1px solid rgba(117, 70, 242, 0.2);
            }}
            
            .stat-item:last-child {{
                border-bottom: none;
            }}
            
            .stat-label {{
                color: #999;
                font-size: 14px;
                font-weight: 500;
            }}
            
            .stat-value {{
                color: #7546f2;
                font-weight: 800;
                font-size: 18px;
            }}
            
            @keyframes pulse-glow {{
                0%, 100% {{
                    box-shadow: 0 15px 50px rgba(117, 70, 242, 0.7);
                }}
                50% {{
                    box-shadow: 0 20px 60px rgba(117, 70, 242, 1);
                }}
            }}
            
            @keyframes rotate-border {{
                0% {{
                    filter: hue-rotate(0deg);
                }}
                100% {{
                    filter: hue-rotate(360deg);
                }}
            }}
            
            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                    transform: scale(0.95) translateY(10px);
                }}
                to {{
                    opacity: 1;
                    transform: scale(1) translateY(0);
                }}
            }}
        </style>
        
        <div class="mindmap-container">
            <!-- Central Node -->
            <div class="central-node">
                <div class="complexity-badge">{complexity} Complexity</div>
                👻 {task[:80]}
            </div>
            
            <!-- SVG for connection lines -->
            <svg style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; z-index: 1;">
                <defs>
                    <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#7546f2;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#7546f2;stop-opacity:0.3" />
                    </linearGradient>
                    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                        <polygon points="0 0, 10 3, 0 6" fill="#7546f2" />
                    </marker>
                </defs>
    """
    
    # Calculate positions for branch groups - improved layout with better spacing
    import math
    
    num_groups = len(action_groups)
    
    # Use different layouts based on number of groups
    group_positions = []
    
    if num_groups == 1:
        # Single group - place below center
        for i, (group_name, steps) in enumerate(action_groups.items()):
            group_positions.append({
                'name': group_name,
                'steps': steps,
                'x': 50,  # Center horizontally
                'y': 450,
                'angle': math.pi / 2
            })
    
    elif num_groups == 2:
        # Two groups - place side by side
        positions = [
            {'x': 15, 'y': 450, 'angle': -math.pi/4},  # Left
            {'x': 65, 'y': 450, 'angle': math.pi/4}    # Right
        ]
        for i, (group_name, steps) in enumerate(action_groups.items()):
            group_positions.append({
                'name': group_name,
                'steps': steps,
                'x': positions[i]['x'],
                'y': positions[i]['y'],
                'angle': positions[i]['angle']
            })
    
    elif num_groups == 3:
        # Three groups - triangle layout
        positions = [
            {'x': 50, 'y': 350, 'angle': -math.pi/2},   # Top
            {'x': 15, 'y': 600, 'angle': math.pi*3/4},  # Bottom left
            {'x': 65, 'y': 600, 'angle': math.pi/4}     # Bottom right
        ]
        for i, (group_name, steps) in enumerate(action_groups.items()):
            group_positions.append({
                'name': group_name,
                'steps': steps,
                'x': positions[i]['x'],
                'y': positions[i]['y'],
                'angle': positions[i]['angle']
            })
    
    elif num_groups == 4:
        # Four groups - square layout
        positions = [
            {'x': 15, 'y': 350, 'angle': -math.pi*3/4},  # Top left
            {'x': 65, 'y': 350, 'angle': -math.pi/4},    # Top right
            {'x': 15, 'y': 600, 'angle': math.pi*3/4},   # Bottom left
            {'x': 65, 'y': 600, 'angle': math.pi/4}      # Bottom right
        ]
        for i, (group_name, steps) in enumerate(action_groups.items()):
            group_positions.append({
                'name': group_name,
                'steps': steps,
                'x': positions[i]['x'],
                'y': positions[i]['y'],
                'angle': positions[i]['angle']
            })
    
    else:
        # 5+ groups - use circular layout with larger radius
        center_x_pct = 50
        center_y_px = 150
        radius = 500  # Increased radius for more spacing
        
        for i, (group_name, steps) in enumerate(action_groups.items()):
            angle = (2 * math.pi * i / num_groups) - (math.pi / 2)
            x_offset = radius * math.cos(angle)
            y_offset = radius * math.sin(angle)
            
            # Convert to percentage for x
            x = center_x_pct + (x_offset / 18)  # Adjusted scaling
            # Keep y in pixels
            y = center_y_px + 300 + y_offset
            
            group_positions.append({
                'name': group_name,
                'steps': steps,
                'x': max(5, min(85, x)),  # Constrain to 5-85%
                'y': max(350, y),  # Minimum y position
                'angle': angle
            })
    
    # Draw connection lines
    for pos in group_positions:
        x = pos['x']
        y = pos['y']
        
        # Calculate line endpoints
        start_x = 50  # Center x
        start_y = 230  # Below central node
        end_x = x if x < 50 else x + 22  # Adjust for branch width
        end_y = y + 30  # Top of branch group
        
        html += f"""
                <line x1="{start_x}%" y1="{start_y}px" x2="{end_x}%" y2="{end_y}px" 
                      stroke="url(#lineGradient)" stroke-width="3" opacity="0.7" 
                      marker-end="url(#arrowhead)" />
        """
    
    html += """
            </svg>
            
            <!-- Branch Groups -->
            <div class="branch-container">
    """
    
    # Icon mapping for action categories
    icon_map = {
        'search': '🔍',
        'click': '👆',
        'open': '🌐',
        'go': '🚀',
        'extract': '📝',
        'input': '⌨️',
        'scroll': '📜',
        'navigate': '🧭',
        'type': '✍️'
    }
    
    for pos in group_positions:
        group_name = pos['name']
        steps = pos['steps']
        x = pos['x']
        y = pos['y']
        
        icon = icon_map.get(group_name.lower(), '⚡')
        display_name = group_name.replace('_', ' ').title()
        
        html += f"""
            <div class="branch-group" style="left: {x}%; top: {y}px;">
                <div class="branch-title">
                    {icon} {display_name} ({len(steps)})
                </div>
        """
        
        for step_info in steps[:5]:  # Limit to 5 steps per group
            html += f"""
                <div class="branch-step">
                    <div class="step-action">
                        <span class="step-num">{step_info['step_num']}</span>
                        {step_info['action']}
                    </div>
                    <div class="step-desc">{step_info['description']}</div>
                </div>
            """
        
        if len(steps) > 5:
            html += f"""
                <div class="branch-step" style="text-align: center; color: #888; font-style: italic;">
                    +{len(steps) - 5} more steps...
                </div>
            """
        
        html += """
            </div>
        """
    
    html += f"""
            </div>
            
            <!-- Stats Panel -->
            <div class="stats-panel">
                <h4 style="color: #7546f2; margin-top: 0; margin-bottom: 15px;">📊 Task Stats</h4>
                <div class="stat-item">
                    <span class="stat-label">Total Steps:</span>
                    <span class="stat-value">{total_steps}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Action Groups:</span>
                    <span class="stat-value">{num_groups}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Complexity:</span>
                    <span class="stat-value">{complexity}</span>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html


def create_notes_tab(webui_manager: WebuiManager):
    """Create the visualization tab (Notes removed, only flowchart and mind map)"""
    
    tab_components = {}
    
    with gr.Column():
        gr.Markdown(
            """
            ### 👻 Ghost Visualization
            #### Visualize and analyze your agent's journey with dynamic flowcharts and AI-powered mind maps
            """,
            elem_classes=["tab-header-text"]
        )
        
        with gr.Tabs():
            # Step-by-Step Flowchart Tab
            with gr.TabItem("🔄 Dynamic Flowchart"):
                gr.Markdown("#### Enhanced step-by-step visualization with animations and detailed metrics")
                
                with gr.Row():
                    task_id_input = gr.Textbox(
                        label="Task ID",
                        placeholder="Enter task ID to visualize...",
                        scale=3
                    )
                    load_flowchart_btn = gr.Button("📊 Load Flowchart", variant="primary", scale=1)
                
                flowchart_display = gr.HTML(
                    value="<div style='text-align: center; padding: 40px; color: #888;'>Enter a task ID and click Load Flowchart</div>",
                    label="Dynamic Flowchart"
                )
            
            # AI-Powered Mind Map Tab
            with gr.TabItem("🧠 AI Mind Map"):
                gr.Markdown("#### Intelligent task visualization with grouped actions and connections")
                
                with gr.Row():
                    mindmap_task_id_input = gr.Textbox(
                        label="Task ID",
                        placeholder="Enter task ID for AI-powered mind map...",
                        scale=3
                    )
                    load_mindmap_btn = gr.Button("🗺️ Generate AI Mind Map", variant="primary", scale=1)
                
                mindmap_display = gr.HTML(
                    value="<div style='text-align: center; padding: 40px; color: #888;'>Enter a task ID and click Generate AI Mind Map</div>",
                    label="AI Mind Map"
                )
    
    tab_components.update(
        dict(
            task_id_input=task_id_input,
            load_flowchart_btn=load_flowchart_btn,
            flowchart_display=flowchart_display,
            mindmap_task_id_input=mindmap_task_id_input,
            load_mindmap_btn=load_mindmap_btn,
            mindmap_display=mindmap_display
        )
    )
    
    webui_manager.add_components("notes", tab_components)
    
    # Event handlers
    def load_flowchart(task_id: str) -> str:
        """Load and display enhanced flowchart for a task"""
        if not task_id:
            return "<div style='text-align: center; padding: 40px; color: #f24646;'>⚠️ Please enter a task ID</div>"
        
        history_file = f"./tmp/agent_history/{task_id}/{task_id}.json"
        if not os.path.exists(history_file):
            return f"<div style='text-align: center; padding: 40px; color: #f24646;'>❌ Task ID '{task_id}' not found<br><small>Check tmp/agent_history/ for available IDs</small></div>"
        
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            return generate_step_flowchart(history_data)
        except Exception as e:
            return f"<div style='text-align: center; padding: 40px; color: #f24646;'>❌ Error loading flowchart: {str(e)}</div>"
    
    def load_mindmap(task_id: str) -> str:
        """Load and display AI-powered mind map for a task"""
        if not task_id:
            return "<div style='text-align: center; padding: 40px; color: #f24646;'>⚠️ Please enter a task ID</div>"
        
        history_file = f"./tmp/agent_history/{task_id}/{task_id}.json"
        if not os.path.exists(history_file):
            return f"<div style='text-align: center; padding: 40px; color: #f24646;'>❌ Task ID '{task_id}' not found<br><small>Check tmp/agent_history/ for available IDs</small></div>"
        
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            return generate_mind_map(history_data)
        except Exception as e:
            return f"<div style='text-align: center; padding: 40px; color: #f24646;'>❌ Error loading mind map: {str(e)}</div>"
    
    # Connect event handlers
    load_flowchart_btn.click(
        fn=load_flowchart,
        inputs=[task_id_input],
        outputs=[flowchart_display]
    )
    
    load_mindmap_btn.click(
        fn=load_mindmap,
        inputs=[mindmap_task_id_input],
        outputs=[mindmap_display]
    )
    
    return tab_components
