import os
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ChangelogManager:
    def __init__(self):
        self.changelog_path = Path(__file__).parent.parent / 'CHANGELOG.md'
        
    def add_entry(self, version: str, changes: dict):
        """Add a new changelog entry"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            new_entry = f"\n## [{version}] - {today}\n\n"
            
            for category, items in changes.items():
                if items:
                    new_entry += f"### {category}\n"
                    for item in items:
                        new_entry += f"- {item}\n"
                    new_entry += "\n"
            
            current_content = self.changelog_path.read_text()
            marker = "# Changelog\n"
            new_content = current_content.replace(
                marker,
                f"{marker}\n{new_entry}"
            )
            
            self.changelog_path.write_text(new_content)
            logger.info(f"Added changelog entry for version {version}")
            
        except Exception as e:
            logger.error(f"Failed to update changelog: {e}")
