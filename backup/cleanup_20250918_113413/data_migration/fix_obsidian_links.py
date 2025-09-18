#!/usr/bin/env python3
"""
Fix Obsidian Cross-Reference Links in DCLT Strategic System
Convert broken Notion-style links to proper Obsidian [[Document Name]] format
"""

import os
import re
import urllib.parse
from pathlib import Path
from datetime import datetime

class ObsidianLinkFixer:
    def __init__(self, data_dir='data/dclt'):
        self.data_dir = Path(data_dir)
        self.file_mapping = {}  # Maps clean titles to actual file paths
        self.stats = {
            'files_scanned': 0,
            'links_found': 0,
            'links_fixed': 0,
            'files_updated': 0,
            'errors': 0
        }
    
    def build_file_mapping(self):
        """Build mapping of clean document titles to actual file paths"""
        print("Building file mapping for link resolution...")
        
        for file_path in self.data_dir.rglob('*.md'):
            # Get clean filename (without extension)
            clean_name = file_path.stem
            
            # Also try to extract title from frontmatter or H1
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Try to get title from frontmatter
                title = self.extract_title_from_content(content, clean_name)
                
                # Map both the filename and extracted title
                self.file_mapping[clean_name] = file_path
                if title != clean_name:
                    self.file_mapping[title] = file_path
                
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
                self.file_mapping[clean_name] = file_path
        
        print(f"Mapped {len(self.file_mapping)} document titles to file paths")
    
    def extract_title_from_content(self, content, fallback):
        """Extract document title from frontmatter or H1"""
        # Try frontmatter first
        if content.startswith('---\n'):
            try:
                parts = content.split('---\n', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
                    if title_match:
                        return title_match.group(1).strip()
            except:
                pass
        
        # Try H1 heading
        h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        
        return fallback
    
    def clean_notion_link_target(self, link_text):
        """Clean Notion-style link target to proper document title"""
        # Remove URL encoding
        cleaned = urllib.parse.unquote(link_text)
        
        # Remove Notion hash IDs (32 character alphanumeric strings)
        cleaned = re.sub(r'\s+[a-f0-9A-F]{32}', '', cleaned)
        cleaned = re.sub(r'_[a-f0-9A-F]{32}', '', cleaned)
        cleaned = re.sub(r'-[a-f0-9A-F]{32}', '', cleaned)
        
        # Clean up file extensions and paths
        cleaned = re.sub(r'\.md$', '', cleaned)
        
        # Clean up path separators and get just the filename
        if '/' in cleaned:
            cleaned = cleaned.split('/')[-1]
        
        # Clean up special prefixes
        cleaned = re.sub(r'^——+\s*', '', cleaned)  # Remove em-dashes
        cleaned = re.sub(r'^—+\s*', '', cleaned)   # Remove en-dashes
        cleaned = re.sub(r'^::\s*', '', cleaned)   # Remove :: prefixes
        cleaned = re.sub(r'^📁\s*', '', cleaned)   # Remove folder emojis
        cleaned = re.sub(r'^🧾\s*', '', cleaned)   # Remove document emojis
        cleaned = re.sub(r'^📋\s*', '', cleaned)   # Remove clipboard emojis
        
        # Clean up extra spaces and formatting
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def find_matching_document(self, target_name):
        """Find the actual document that matches the target name"""
        # Try exact match first
        if target_name in self.file_mapping:
            return target_name
        
        # Try case-insensitive match
        for mapped_name in self.file_mapping.keys():
            if mapped_name.lower() == target_name.lower():
                return mapped_name
        
        # Try partial match (for truncated titles)
        target_words = set(target_name.lower().split())
        best_match = None
        best_score = 0
        
        for mapped_name in self.file_mapping.keys():
            mapped_words = set(mapped_name.lower().split())
            if mapped_words and target_words:
                intersection = len(target_words.intersection(mapped_words))
                union = len(target_words.union(mapped_words))
                score = intersection / union if union > 0 else 0
                
                if score > best_score and score > 0.6:  # 60% similarity threshold
                    best_score = score
                    best_match = mapped_name
        
        return best_match
    
    def fix_links_in_content(self, content):
        """Fix all link formats in document content"""
        fixed_content = content
        links_fixed = 0
        
        # Pattern 1: [[old-style-link]] - already in Obsidian format but may have bad targets
        def fix_obsidian_link(match):
            nonlocal links_fixed
            link_target = match.group(1)
            cleaned_target = self.clean_notion_link_target(link_target)
            matching_doc = self.find_matching_document(cleaned_target)
            
            if matching_doc and matching_doc != link_target:
                links_fixed += 1
                return f'[[{matching_doc}]]'
            return match.group(0)
        
        fixed_content = re.sub(r'\[\[([^\]]+)\]\]', fix_obsidian_link, fixed_content)
        
        # Pattern 2: [Link Text](path/to/file.md) - Markdown links to fix
        def fix_markdown_link(match):
            nonlocal links_fixed
            link_text = match.group(1)
            link_path = match.group(2)
            
            # Skip external links
            if link_path.startswith('http') or link_path.startswith('mailto'):
                return match.group(0)
            
            # Clean the path to get document name
            cleaned_target = self.clean_notion_link_target(link_path)
            matching_doc = self.find_matching_document(cleaned_target)
            
            if matching_doc:
                links_fixed += 1
                return f'[[{matching_doc}|{link_text}]]'
            return match.group(0)
        
        fixed_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', fix_markdown_link, fixed_content)
        
        # Pattern 3: Standalone URLs in content that look like file references
        # Skip this for now to avoid breaking valid URLs
        
        return fixed_content, links_fixed
    
    def fix_document_links(self, file_path):
        """Fix all links in a single document"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_links = len(re.findall(r'\[\[([^\]]+)\]\]', content))
            
            fixed_content, links_fixed = self.fix_links_in_content(content)
            
            if links_fixed > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                self.stats['files_updated'] += 1
                self.stats['links_fixed'] += links_fixed
                print(f"Fixed {links_fixed} links in: {file_path.relative_to(self.data_dir)}")
            
            self.stats['links_found'] += original_links
            
        except Exception as e:
            print(f"Error fixing links in {file_path}: {e}")
            self.stats['errors'] += 1
    
    def validate_sample_links(self):
        """Validate that some links actually resolve to existing files"""
        print("\nValidating link resolution...")
        
        sample_count = 0
        valid_count = 0
        
        for file_path in list(self.data_dir.rglob('*.md'))[:10]:  # Sample first 10 files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all Obsidian links
                links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
                
                for link in links[:3]:  # Check first 3 links per file
                    sample_count += 1
                    if link in self.file_mapping:
                        target_file = self.file_mapping[link]
                        if target_file.exists():
                            valid_count += 1
                        else:
                            print(f"Warning: Link target not found: {link}")
                    else:
                        print(f"Warning: No mapping for: {link}")
                
                if sample_count >= 20:  # Limit validation sample
                    break
                    
            except Exception as e:
                continue
        
        if sample_count > 0:
            success_rate = (valid_count / sample_count) * 100
            print(f"Link validation: {valid_count}/{sample_count} links valid ({success_rate:.1f}%)")
        else:
            print("No links found to validate")
    
    def fix_all_links(self):
        """Fix links in all documents"""
        print("=== Obsidian Link Fixer ===")
        
        # Step 1: Build file mapping
        self.build_file_mapping()
        
        # Step 2: Fix links in all files
        print("\nFixing links in all documents...")
        for file_path in self.data_dir.rglob('*.md'):
            self.fix_document_links(file_path)
            self.stats['files_scanned'] += 1
        
        # Step 3: Validate sample links
        self.validate_sample_links()
        
        # Step 4: Generate summary
        print(f"\n=== Link Fixing Complete ===")
        print(f"Files scanned: {self.stats['files_scanned']}")
        print(f"Links found: {self.stats['links_found']}")
        print(f"Links fixed: {self.stats['links_fixed']}")
        print(f"Files updated: {self.stats['files_updated']}")
        print(f"Errors: {self.stats['errors']}")
        
        return self.stats

def main():
    """Main link fixing function"""
    fixer = ObsidianLinkFixer()
    stats = fixer.fix_all_links()
    
    print(f"\n✅ Obsidian link fixing complete!")
    print(f"🔗 {stats['links_fixed']} links converted to proper [[Document Name]] format")
    print(f"📝 {stats['files_updated']} files updated with working links")

if __name__ == '__main__':
    main()