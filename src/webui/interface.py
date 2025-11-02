import gradio as gr

from src.webui.webui_manager import WebuiManager
from src.webui.components.agent_settings_tab import create_agent_settings_tab
from src.webui.components.browser_settings_tab import create_browser_settings_tab
from src.webui.components.browser_use_agent_tab import create_browser_use_agent_tab
from src.webui.components.deep_research_agent_tab import create_deep_research_agent_tab
from src.webui.components.load_save_config_tab import create_load_save_config_tab
from src.webui.components.dashboard_tab import create_dashboard_tab
from src.webui.components.notes_visualization_tab import create_notes_tab

theme_map = {
    "Default": gr.themes.Default(),
    "Soft": gr.themes.Soft(),
    "Monochrome": gr.themes.Monochrome(),
    "Glass": gr.themes.Glass(),
    "Origin": gr.themes.Origin(),
    "Citrus": gr.themes.Citrus(),
    "Ocean": gr.themes.Ocean(),
    "Base": gr.themes.Base()
}


def create_ui(theme_name="Base"):
    css = """
    :root {
        --background-fill-primary: #ffffff;
        --background-fill-secondary: #f7f8fb;
        --body-text-color: #111827;
        --color-accent: #2563eb;
        --border-color-primary: #e5e7eb;
    }

    /* layout tweaks */
    .gradio-container {
        width: 70vw !important;
        max-width: 70% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-top: 10px !important;
        background: var(--background-fill-primary) !important;
        color: var(--body-text-color) !important;
    }

    .parent-container, body {
        background: var(--background-fill-primary) !important;
        color: var(--body-text-color) !important;
    }

    /* header / tabs */
    .header-text { text-align: center; margin-bottom: 20px; color: var(--body-text-color); }
    .tab-header-text { text-align: center; color: var(--body-text-color); }

    .theme-section { margin-bottom: 10px; padding: 15px; border-radius: 10px; background: var(--background-fill-secondary); }

    /* make sure inline dark backgrounds are softened */
    [style*="rgba(34, 34, 47")], [style*="rgba(19, 19, 31")], [style*="rgba(44, 44, 57")],
    [style*="#111"], [style*="#000"] {
        background: rgba(255,255,255,0.9) !important;
        color: var(--body-text-color) !important;
        border-color: var(--border-color-primary) !important;
    }

    /* force readable text for any inline color declarations */
    .gradio-container, .gradio-container * {
        color: var(--body-text-color) !important;
    }

    /* ensure badges and status pills keep readable contrast */
    .status-pill, .badge { color: white !important; }

    /* accent color for primary buttons */
    .gr-button-primary { background: linear-gradient(90deg, var(--color-accent), #1e40af) !important; }
    """

    # prefer light theme by default
    js_func = """
    function refresh() {
        const url = new URL(window.location);

        if (url.searchParams.get('__theme') !== 'light') {
            url.searchParams.set('__theme', 'light');
            window.location.href = url.href;
        }
    }
    """

    ui_manager = WebuiManager()

    with gr.Blocks(
            title="Browser Use WebUI", theme=theme_map[theme_name], css=css, js=js_func,
    ) as demo:
        with gr.Row():
            gr.Markdown(
                """
                # 🌐 Browser Use WebUI
                ### Control your browser with AI assistance
                """,
                elem_classes=["header-text"],
            )

        with gr.Tabs() as tabs:
            with gr.TabItem("⚙️ Agent Settings"):
                create_agent_settings_tab(ui_manager)

            with gr.TabItem("🌐 Browser Settings"):
                create_browser_settings_tab(ui_manager)

            with gr.TabItem("🤖 Run Agent"):
                create_browser_use_agent_tab(ui_manager)

            with gr.TabItem("📊 Dashboard"):
                create_dashboard_tab(ui_manager)
            
            with gr.TabItem("📝 Notes & Visualization"):
                create_notes_tab(ui_manager)

            with gr.TabItem("🎁 Agent Marketplace"):
                gr.Markdown(
                    """
                    ### Agents built on Browser-Use
                    """,
                    elem_classes=["tab-header-text"],
                )
                with gr.Tabs():
                    with gr.TabItem("Deep Research"):
                        create_deep_research_agent_tab(ui_manager)

            with gr.TabItem("📁 Load & Save Config"):
                create_load_save_config_tab(ui_manager)

    return demo
