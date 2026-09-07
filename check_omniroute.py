"""
OmniRoute Connectivity Test & Vault Setup

Tests that OmniRoute is running and accessible, and initializes the Obsidian vault.
Run this before starting the main agent.
"""

import os
import sys
import logging
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
import requests
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


def test_omniroute_connection():
    """Test connectivity to OmniRoute proxy."""
    
    omniroute_endpoint = os.getenv("ANTHROPIC_ENDPOINT", "http://localhost:20128")
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    
    logger.info("=" * 60)
    logger.info("🔍 OmniRoute Connectivity Test")
    logger.info("=" * 60)
    
    # Check configuration
    if not omniroute_endpoint:
        logger.error("❌ ANTHROPIC_ENDPOINT not configured in .env")
        return False
    
    if not api_key or api_key.startswith("sk-") == False:
        logger.error("❌ ANTHROPIC_API_KEY not configured correctly in .env")
        return False
    
    logger.info(f"✅ Endpoint configured: {omniroute_endpoint}")
    logger.info(f"✅ API Key present: {api_key[:20]}...")
    logger.info(f"✅ Model: {os.getenv('ANTHROPIC_MODEL', 'auto/best-free')}")
    
    # Test connectivity
    try:
        logger.info("\n🔗 Testing connection...")
        response = requests.get(
            f"{omniroute_endpoint}/health" if omniroute_endpoint.endswith("/health") == False 
            else omniroute_endpoint,
            timeout=5
        )
        
        if response.status_code in [200, 404]:  # 404 is ok if endpoint doesn't have /health
            logger.info(f"✅ OmniRoute is reachable (Status: {response.status_code})")
            return True
        else:
            logger.error(f"❌ OmniRoute returned unexpected status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        logger.error(f"❌ Cannot connect to OmniRoute at {omniroute_endpoint}")
        logger.error("   Make sure OmniRoute is running: ollama serve (or similar)")
        return False
    except requests.exceptions.Timeout:
        logger.error(f"❌ OmniRoute connection timed out")
        return False
    except Exception as e:
        logger.error(f"❌ Connection error: {e}")
        return False


async def setup_obsidian_vault():
    """Set up Obsidian vault directory structure."""
    
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "")
    
    logger.info("\n" + "=" * 60)
    logger.info("🧠 Obsidian Vault Setup")
    logger.info("=" * 60)
    
    if not vault_path:
        logger.warning("⚠️  OBSIDIAN_VAULT_PATH not configured in .env")
        logger.info("   To enable Obsidian integration, set OBSIDIAN_VAULT_PATH in .env")
        return False
    
    vault_path = Path(vault_path)
    
    # Create vault structure
    try:
        logger.info(f"📁 Creating vault at: {vault_path}")
        
        # Main folders
        folders = [
            "Research",
            "Findings", 
            "Task Logs",
            "Concepts",
            "Tools & Integrations",
            "Errors & Debugging",
            "_metadata"
        ]
        
        for folder in folders:
            folder_path = vault_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"   ✅ {folder}/")
        
        # Create main index
        index_path = vault_path / "INDEX.md"
        if not index_path.exists():
            index_content = """# Update-Web-Agent Vault 🧠

> Real-time agent brain and knowledge base. Auto-updated as the agent discovers insights.

## 📚 Sections


## 🔗 Configuration

**OmniRoute:** http://localhost:20128
**Model:** Anthropic Claude (auto/best-free)
**Updated:** {datetime.now().isoformat()}

_This vault is managed by Update-Web-Agent and syncs in real-time_
"""
            index_path.write_text(index_content, encoding='utf-8')
            logger.info(f"   ✅ Created INDEX.md")
        
        # Create .obsidian config if it doesn't exist
        obsidian_config = vault_path / ".obsidian"
        obsidian_config.mkdir(exist_ok=True)
        
        settings_path = obsidian_config / "app.json"
        if not settings_path.exists():
            settings = {
                "baseFontSize": 16,
                "useTab": True,
                "lineLength": 0,
                "ribbonMinWidth": 50,
                "maxSidebarWidth": 50,
                "showRibbon": True,
                "showFileTree": True,
                "showProperties": True,
                "strictLineBreaks": False,
                "showInlineTitle": True,
                "showLineNumber": False,
                "showFrontmatter": False,
                "showSearchDetails": False,
                "alwaysUpdateLinks": True,
                "newLinkFormat": "relative",
                "newFileLocation": "root"
            }
            settings_path.write_text(__import__('json').dumps(settings, indent=2))
            logger.info(f"   ✅ Created .obsidian/app.json")
        
        logger.info(f"\n✅ Obsidian vault ready!")
        logger.info(f"   Open in Obsidian: Vault selector → Open folder → {vault_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to set up vault: {e}")
        return False


async def test_vault_manager():
    """Test the vault manager by importing it."""
    
    logger.info("\n" + "=" * 60)
    logger.info("🧪 Vault Manager Test")
    logger.info("=" * 60)
    
    try:
        from src.utils.obsidian_vault import get_vault_manager
        
        vault = get_vault_manager()
        
        if vault.is_enabled():
            logger.info(f"✅ Vault manager initialized")
            logger.info(f"   Path: {vault.get_vault_path()}")
            
            # Test writing a simple note
            test_path = await vault.write_research(
                topic="Setup Test",
                content="Test note created during initialization.\n\nIf you see this, the vault integration is working!",
                tags=["setup", "test"]
            )
            
            if test_path:
                logger.info(f"✅ Test write successful: {test_path.name}")
                return True
        else:
            logger.warning("⚠️  Vault manager not enabled (vault path not configured)")
            return False
            
    except Exception as e:
        logger.error(f"❌ Vault manager test failed: {e}", exc_info=True)
        return False


async def main():
    """Run all tests and setup."""
    
    logger.info("\n🚀 Update-Web-Agent: Startup Checks\n")
    
    # Test OmniRoute
    omniroute_ok = test_omniroute_connection()
    
    # Setup vault
    vault_ok = await setup_obsidian_vault()
    
    # Test vault manager
    vault_manager_ok = await test_vault_manager()
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📋 Summary")
    logger.info("=" * 60)
    
    results = {
        "OmniRoute": "✅ Ready" if omniroute_ok else "❌ Not connected",
        "Obsidian Vault": "✅ Ready" if vault_ok else "⚠️  Not configured",
        "Vault Manager": "✅ Ready" if vault_manager_ok else "⚠️  Not available"
    }
    
    for component, status in results.items():
        logger.info(f"{status.split()[0]} {component}: {status}")
    
    logger.info("\n" + "=" * 60)
    
    if omniroute_ok:
        logger.info("✅ All systems ready! You can now start the agent.")
        return 0
    else:
        logger.error("❌ OmniRoute not available. Please ensure it's running.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
