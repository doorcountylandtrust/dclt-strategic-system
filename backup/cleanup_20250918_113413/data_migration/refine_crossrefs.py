#!/usr/bin/env python3
"""
Refine Cross-References for DCLT Strategic System
Clean up over-aggressive cross-references and focus on high-quality strategic connections
"""

import os
import re
from pathlib import Path
from datetime import datetime

class DCLTCrossReferenceRefiner:
    def __init__(self, data_dir='data/dclt'):
        self.data_dir = Path(data_dir)
        self.stats = {
            'files_processed': 0,
            'links_removed': 0,
            'sections_cleaned': 0,
            'errors': 0
        }
    
    def clean_frontmatter_links(self, content):
        """Remove excessive links from frontmatter"""
        # Split frontmatter and content
        if content.startswith('---\n'):
            parts = content.split('---\n', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                main_content = parts[2]
                
                # Clean excessive links from frontmatter
                # Remove all [[link]] patterns from frontmatter values
                cleaned_frontmatter = re.sub(r'\[\[([^\]]+)\]\]', '', frontmatter)
                # Clean up extra parentheses and formatting
                cleaned_frontmatter = re.sub(r'\(\)\s*\(\)', '', cleaned_frontmatter)
                cleaned_frontmatter = re.sub(r'\s+', ' ', cleaned_frontmatter)
                
                return f"---\n{cleaned_frontmatter}---\n{main_content}"
        
        return content
    
    def clean_related_documents_section(self, content):
        """Clean and refine the Related Documents section"""
        # Find Related Documents section
        related_pattern = r'## Related Documents\s*\n(.*?)(?=\n##|\n---|\Z)'
        
        match = re.search(related_pattern, content, re.DOTALL)
        if not match:
            return content
        
        related_section = match.group(1)
        
        # Extract only high-quality links (limit to 3-5 per category)
        refined_section = "## Related Documents\n\n"
        
        # Find cross-referenced documents (highest priority)
        cross_ref_matches = re.findall(r'\[\[([^\]]+)\]\] - Documents reference each other', related_section)
        if cross_ref_matches:
            refined_section += "**Cross-Referenced Documents**\n"
            for link in cross_ref_matches[:3]:  # Limit to 3
                refined_section += f"- [[{link}]]\n"
            refined_section += "\n"
        
        # Find strategy implementation links
        strategy_matches = re.findall(r'\[\[([^\]]+)\]\] - Implementation of strategic themes', related_section)
        if strategy_matches:
            refined_section += "**Strategic Implementation**\n"
            for link in strategy_matches[:3]:  # Limit to 3
                refined_section += f"- [[{link}]]\n"
            refined_section += "\n"
        
        # Find thematic alignment links
        thematic_matches = re.findall(r'\[\[([^\]]+)\]\] - Aligned on: ([^\\n]+)', related_section)
        if thematic_matches:
            refined_section += "**Thematic Alignment**\n"
            for link, themes in thematic_matches[:3]:  # Limit to 3
                refined_section += f"- [[{link}]] - {themes}\n"
            refined_section += "\n"
        
        # Replace the old section with refined version
        new_content = re.sub(related_pattern, refined_section.rstrip(), content, flags=re.DOTALL)
        
        return new_content
    
    def remove_excessive_inline_links(self, content):
        """Remove excessive inline links while keeping strategic ones"""
        # Remove patterns like "Strategic Implementation ([[link1]]) ([[link2]]) ..."
        content = re.sub(r'\*\*Strategic Implementation[^*]*?\*\*', '', content)
        
        # Clean up multiple consecutive links in parentheses
        content = re.sub(r'\(\[\[[^\]]+\]\]\)\s*\(\[\[[^\]]+\]\]\)', '', content)
        
        # Remove excessive link chains
        content = re.sub(r'(\[\[[^\]]+\]\]\s*){5,}', '', content)
        
        return content
    
    def refine_document(self, file_path):
        """Refine cross-references in a single document"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Clean frontmatter
            content = self.clean_frontmatter_links(content)
            
            # Clean Related Documents section
            content = self.clean_related_documents_section(content)
            
            # Remove excessive inline links
            content = self.remove_excessive_inline_links(content)
            
            # Count changes
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Count links removed
                original_links = len(re.findall(r'\[\[[^\]]+\]\]', original_content))
                new_links = len(re.findall(r'\[\[[^\]]+\]\]', content))
                links_removed = original_links - new_links
                
                self.stats['links_removed'] += links_removed
                if links_removed > 0:
                    self.stats['files_processed'] += 1
                    print(f"Refined: {file_path.relative_to(self.data_dir)} (removed {links_removed} excessive links)")
            
        except Exception as e:
            print(f"Error refining {file_path}: {e}")
            self.stats['errors'] += 1
    
    def refine_all_documents(self):
        """Refine cross-references in all documents"""
        print("=== DCLT Cross-Reference Refinement ===")
        print("Cleaning excessive links while preserving strategic connections...")
        
        for file_path in self.data_dir.rglob('*.md'):
            self.refine_document(file_path)
        
        print(f"\n=== Refinement Complete ===")
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Excessive links removed: {self.stats['links_removed']}")
        print(f"Errors: {self.stats['errors']}")
        
        return self.stats

def main():
    """Main refinement function"""
    refiner = DCLTCrossReferenceRefiner()
    stats = refiner.refine_all_documents()
    
    print(f"\n✅ Cross-reference refinement complete!")
    print(f"📈 Your Obsidian graph now shows focused strategic relationships")
    print(f"🔗 Quality over quantity - strategic connections preserved")

if __name__ == '__main__':
    main()