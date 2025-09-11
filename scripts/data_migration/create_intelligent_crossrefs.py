#!/usr/bin/env python3
"""
Create Intelligent Cross-References for DCLT Strategic System
Analyzes document relationships and adds strategic markdown links for Obsidian graph view
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json

class DCLTCrossReferenceBuilder:
    def __init__(self, data_dir='data/dclt'):
        self.data_dir = Path(data_dir)
        self.documents = {}
        self.relationships = defaultdict(list)
        self.stakeholders = set()
        self.projects = set()
        self.themes = set()
        self.stats = {
            'files_analyzed': 0,
            'relationships_found': 0,
            'links_created': 0,
            'files_updated': 0,
            'errors': 0
        }
    
    def extract_frontmatter_and_content(self, file_path):
        """Extract YAML frontmatter and content from markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter = {}
            main_content = content
            
            # Check for YAML frontmatter
            if content.startswith('---\n'):
                try:
                    # Split frontmatter and content
                    parts = content.split('---\n', 2)
                    if len(parts) >= 3:
                        frontmatter_text = parts[1]
                        main_content = parts[2]
                        frontmatter = yaml.safe_load(frontmatter_text) or {}
                except yaml.YAMLError:
                    pass  # If YAML parsing fails, treat as no frontmatter
            
            return frontmatter, main_content
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return {}, ""
    
    def analyze_document_content(self, file_path, frontmatter, content):
        """Analyze document content for strategic elements"""
        doc_info = {
            'path': file_path,
            'title': self.extract_title(file_path, frontmatter, content),
            'frontmatter': frontmatter,
            'content': content,
            'category': self.determine_category(file_path),
            'stakeholders': self.extract_stakeholders(frontmatter, content),
            'projects': self.extract_projects(frontmatter, content),
            'themes': self.extract_themes(frontmatter, content),
            'referenced_docs': self.extract_document_references(content),
            'strategic_keywords': self.extract_strategic_keywords(content)
        }
        
        return doc_info
    
    def extract_title(self, file_path, frontmatter, content):
        """Extract document title from various sources"""
        # Priority: frontmatter title > H1 heading > filename
        if 'title' in frontmatter:
            return frontmatter['title']
        
        # Look for H1 heading
        h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        
        # Fall back to filename without extension
        return file_path.stem
    
    def determine_category(self, file_path):
        """Determine document category from path"""
        path_str = str(file_path)
        if '1 STRATEGY' in path_str:
            return 'strategy'
        elif '2 EXECUTION' in path_str:
            return 'execution'
        elif '3 REFERENCE' in path_str:
            return 'reference'
        else:
            return 'other'
    
    def extract_stakeholders(self, frontmatter, content):
        """Extract stakeholder names from frontmatter and content"""
        stakeholders = set()
        
        # From frontmatter
        for key in ['stakeholders', 'people', 'contacts', 'interviewees']:
            if key in frontmatter:
                if isinstance(frontmatter[key], list):
                    stakeholders.update(frontmatter[key])
                elif isinstance(frontmatter[key], str):
                    stakeholders.add(frontmatter[key])
        
        # From content - look for name patterns
        name_patterns = [
            r'([A-Z][a-z]+ [A-Z][a-z]+)',  # First Last
            r'([A-Z][a-z]+ & [A-Z][a-z]+ [A-Z][a-z]+)',  # First & First Last
            r'([A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+)',  # First M. Last
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Filter out common false positives
                if not re.search(r'(Door County|Land Trust|Strategic|Master|Brand|Website)', match):
                    stakeholders.add(match)
        
        return list(stakeholders)
    
    def extract_projects(self, frontmatter, content):
        """Extract project names and initiatives"""
        projects = set()
        
        # From frontmatter
        for key in ['projects', 'initiatives', 'campaigns']:
            if key in frontmatter:
                if isinstance(frontmatter[key], list):
                    projects.update(frontmatter[key])
                elif isinstance(frontmatter[key], str):
                    projects.add(frontmatter[key])
        
        # From content - look for project patterns
        project_patterns = [
            r'([A-Z][a-z\s]+(?:Project|Campaign|Initiative|Strategy|Plan))',
            r'(Brand System \([0-9]+\))',
            r'(Website (?:Strategy|Overhaul|Redesign))',
            r'(Membership Strategy)',
            r'(Legacy of the Land)',
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            projects.update(matches)
        
        return list(projects)
    
    def extract_themes(self, frontmatter, content):
        """Extract strategic themes and topics"""
        themes = set()
        
        # From frontmatter
        for key in ['themes', 'topics', 'tags', 'categories']:
            if key in frontmatter:
                if isinstance(frontmatter[key], list):
                    themes.update(frontmatter[key])
                elif isinstance(frontmatter[key], str):
                    themes.add(frontmatter[key])
        
        # Strategic themes from content
        theme_keywords = [
            'land protection', 'conservation', 'stewardship', 'fundraising',
            'community engagement', 'volunteers', 'membership', 'brand strategy',
            'communications', 'website', 'marketing', 'outreach', 'education',
            'partnerships', 'accessibility', 'strategic planning'
        ]
        
        content_lower = content.lower()
        for keyword in theme_keywords:
            if keyword in content_lower:
                themes.add(keyword)
        
        return list(themes)
    
    def extract_document_references(self, content):
        """Extract references to other documents"""
        references = set()
        
        # Look for document-like references
        doc_patterns = [
            r'(?:see|refer to|outlined in|as per|according to)\s+([A-Z][^.!?]*(?:Plan|Strategy|Report|Summary|Brief|Framework))',
            r'([A-Z][^.!?]*(?:Plan|Strategy|Report|Summary|Brief|Framework))\s+(?:document|file|outlines|describes)',
        ]
        
        for pattern in doc_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            references.update(matches)
        
        return list(references)
    
    def extract_strategic_keywords(self, content):
        """Extract strategic keywords for relationship analysis"""
        keywords = set()
        
        strategic_terms = [
            'strategic initiative', 'mission', 'vision', 'goals', 'objectives',
            'stakeholder', 'audience', 'messaging', 'brand', 'identity',
            'campaign', 'outreach', 'engagement', 'member', 'donor',
            'preserve', 'easement', 'acquisition', 'stewardship'
        ]
        
        content_lower = content.lower()
        for term in strategic_terms:
            if term in content_lower:
                keywords.add(term)
        
        return list(keywords)
    
    def scan_all_documents(self):
        """Scan all markdown files and analyze content"""
        print("Scanning all documents for relationship analysis...")
        
        for file_path in self.data_dir.rglob('*.md'):
            try:
                frontmatter, content = self.extract_frontmatter_and_content(file_path)
                doc_info = self.analyze_document_content(file_path, frontmatter, content)
                
                # Store document info
                relative_path = file_path.relative_to(self.data_dir)
                self.documents[str(relative_path)] = doc_info
                
                # Update global sets
                self.stakeholders.update(doc_info['stakeholders'])
                self.projects.update(doc_info['projects'])
                self.themes.update(doc_info['themes'])
                
                self.stats['files_analyzed'] += 1
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
                self.stats['errors'] += 1
        
        print(f"Analyzed {self.stats['files_analyzed']} documents")
        print(f"Found {len(self.stakeholders)} stakeholders, {len(self.projects)} projects, {len(self.themes)} themes")
    
    def identify_relationships(self):
        """Identify relationships between documents"""
        print("Identifying strategic relationships...")
        
        doc_list = list(self.documents.items())
        
        for i, (path1, doc1) in enumerate(doc_list):
            for j, (path2, doc2) in enumerate(doc_list[i+1:], i+1):
                relationships = self.find_document_relationships(doc1, doc2)
                
                for relationship in relationships:
                    self.relationships[path1].append({
                        'target_doc': path2,
                        'target_title': doc2['title'],
                        'relationship_type': relationship['type'],
                        'strength': relationship['strength'],
                        'context': relationship['context']
                    })
                    
                    # Add reverse relationship
                    self.relationships[path2].append({
                        'target_doc': path1,
                        'target_title': doc1['title'],
                        'relationship_type': relationship['type'],
                        'strength': relationship['strength'],
                        'context': relationship['context']
                    })
        
        total_relationships = sum(len(rels) for rels in self.relationships.values())
        self.stats['relationships_found'] = total_relationships // 2  # Divide by 2 since we count each twice
        print(f"Found {self.stats['relationships_found']} strategic relationships")
    
    def find_document_relationships(self, doc1, doc2):
        """Find specific relationships between two documents"""
        relationships = []
        
        # Skip if same document
        if doc1['path'] == doc2['path']:
            return relationships
        
        # Strategy-Execution relationship
        if doc1['category'] == 'strategy' and doc2['category'] == 'execution':
            if self.has_shared_elements(doc1['themes'], doc2['themes'], min_overlap=2):
                relationships.append({
                    'type': 'strategy_implementation',
                    'strength': 'high',
                    'context': f"Implementation of strategic themes"
                })
        
        # Shared stakeholders
        shared_stakeholders = set(doc1['stakeholders']) & set(doc2['stakeholders'])
        if shared_stakeholders:
            relationships.append({
                'type': 'shared_stakeholders',
                'strength': 'medium' if len(shared_stakeholders) > 1 else 'low',
                'context': f"Shared stakeholders: {', '.join(list(shared_stakeholders)[:3])}"
            })
        
        # Shared projects
        shared_projects = set(doc1['projects']) & set(doc2['projects'])
        if shared_projects:
            relationships.append({
                'type': 'shared_projects',
                'strength': 'high',
                'context': f"Related to: {', '.join(list(shared_projects)[:2])}"
            })
        
        # Shared themes (strategic alignment)
        shared_themes = set(doc1['themes']) & set(doc2['themes'])
        if len(shared_themes) >= 3:  # Significant thematic overlap
            relationships.append({
                'type': 'thematic_alignment',
                'strength': 'medium',
                'context': f"Aligned on: {', '.join(list(shared_themes)[:3])}"
            })
        
        # Reference-based relationships
        if self.documents_reference_each_other(doc1, doc2):
            relationships.append({
                'type': 'cross_reference',
                'strength': 'high',
                'context': "Documents reference each other"
            })
        
        return relationships
    
    def has_shared_elements(self, list1, list2, min_overlap=1):
        """Check if two lists have minimum overlap"""
        return len(set(list1) & set(list2)) >= min_overlap
    
    def documents_reference_each_other(self, doc1, doc2):
        """Check if documents reference each other by title or content"""
        title1_in_2 = doc1['title'].lower() in doc2['content'].lower()
        title2_in_1 = doc2['title'].lower() in doc1['content'].lower()
        return title1_in_2 or title2_in_1
    
    def create_cross_reference_links(self):
        """Create intelligent cross-reference links in documents"""
        print("Creating intelligent cross-reference links...")
        
        for doc_path, relationships in self.relationships.items():
            if not relationships:
                continue
            
            try:
                doc_info = self.documents[doc_path]
                full_path = doc_info['path']
                
                # Read current content
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add cross-references
                updated_content = self.add_cross_references_to_content(content, relationships, doc_info)
                
                if updated_content != content:
                    # Write updated content
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    self.stats['files_updated'] += 1
                    self.stats['links_created'] += len(relationships)
                    print(f"Updated: {doc_path}")
            
            except Exception as e:
                print(f"Error updating {doc_path}: {e}")
                self.stats['errors'] += 1
        
        print(f"Updated {self.stats['files_updated']} files with {self.stats['links_created']} cross-references")
    
    def add_cross_references_to_content(self, content, relationships, doc_info):
        """Add cross-reference links to document content"""
        updated_content = content
        
        # Group relationships by type and strength
        high_priority = [r for r in relationships if r['strength'] == 'high']
        medium_priority = [r for r in relationships if r['strength'] == 'medium']
        
        # Only add cross-references if we have meaningful relationships
        significant_relationships = high_priority + medium_priority[:3]  # Limit to avoid over-linking
        
        if not significant_relationships:
            return content
        
        # Check if document already has a "Related Documents" section
        if '## Related Documents' not in content and '## Related' not in content:
            # Add Related Documents section at the end
            related_section = self.create_related_documents_section(significant_relationships)
            updated_content = content.rstrip() + '\n\n' + related_section
        
        # Add inline references where contextually appropriate
        updated_content = self.add_inline_references(updated_content, significant_relationships)
        
        return updated_content
    
    def create_related_documents_section(self, relationships):
        """Create a Related Documents section"""
        section = "## Related Documents\n\n"
        
        # Group by relationship type
        by_type = defaultdict(list)
        for rel in relationships:
            by_type[rel['relationship_type']].append(rel)
        
        type_labels = {
            'strategy_implementation': '**Strategic Implementation**',
            'shared_projects': '**Related Projects**',
            'shared_stakeholders': '**Shared Stakeholders**',
            'thematic_alignment': '**Thematic Alignment**',
            'cross_reference': '**Cross-Referenced Documents**'
        }
        
        for rel_type, rels in by_type.items():
            if rel_type in type_labels:
                section += f"{type_labels[rel_type]}\n"
                for rel in rels[:3]:  # Limit to 3 per type
                    section += f"- [[{rel['target_title']}]] - {rel['context']}\n"
                section += "\n"
        
        return section
    
    def add_inline_references(self, content, relationships):
        """Add inline references where contextually appropriate"""
        updated_content = content
        
        # Look for opportunities to add natural links
        for rel in relationships:
            if rel['relationship_type'] in ['strategy_implementation', 'cross_reference']:
                # Try to add contextual links
                target_title = rel['target_title']
                
                # Look for mentions of related concepts
                concept_phrases = [
                    'strategic plan', 'implementation', 'execution', 'strategy',
                    'outlined in', 'as described', 'following the'
                ]
                
                for phrase in concept_phrases:
                    pattern = rf'({phrase})\b'
                    if re.search(pattern, content, re.IGNORECASE):
                        replacement = f'\\1 ([[{target_title}]])'
                        # Only replace first occurrence to avoid over-linking
                        updated_content = re.sub(pattern, replacement, updated_content, count=1, flags=re.IGNORECASE)
                        break
        
        return updated_content
    
    def generate_relationship_report(self):
        """Generate comprehensive relationship analysis report"""
        report = f"""# DCLT Cross-Reference Analysis Report
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Executive Summary

Successfully analyzed {self.stats['files_analyzed']} documents in the DCLT strategic system and created {self.stats['relationships_found']} strategic relationships with {self.stats['links_created']} cross-reference links.

## Analysis Results

### Document Analysis
- **Files Analyzed**: {self.stats['files_analyzed']}
- **Strategic Relationships Found**: {self.stats['relationships_found']}
- **Cross-Reference Links Created**: {self.stats['links_created']}
- **Files Updated**: {self.stats['files_updated']}
- **Processing Errors**: {self.stats['errors']}

### Stakeholder Network
**{len(self.stakeholders)} stakeholders identified:**
{self.format_list(list(self.stakeholders)[:20])}

### Project Ecosystem
**{len(self.projects)} projects/initiatives identified:**
{self.format_list(list(self.projects)[:15])}

### Strategic Themes
**{len(self.themes)} strategic themes identified:**
{self.format_list(list(self.themes)[:15])}

## Relationship Categories Created

### 1. Strategy-Implementation Links
Documents in the Strategy section linked to their implementation in the Execution section.

### 2. Shared Stakeholder Connections
Documents involving the same people, organizations, or community members.

### 3. Project-Based Relationships
Documents related to the same projects, campaigns, or initiatives.

### 4. Thematic Alignment
Documents addressing similar strategic themes (land protection, community engagement, etc.).

### 5. Cross-Reference Networks
Documents that explicitly reference each other or related concepts.

## Top Connected Documents

"""
        
        # Find most connected documents
        connection_counts = {path: len(rels) for path, rels in self.relationships.items()}
        top_connected = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for path, count in top_connected:
            doc_title = self.documents[path]['title']
            report += f"- **{doc_title}** ({count} connections)\n"
        
        report += f"""

## Obsidian Graph Benefits

### Enhanced Navigation
- **Strategic Pathways**: Clear connections between planning and execution
- **Stakeholder Networks**: Visualize who's involved in what initiatives
- **Project Ecosystems**: See how different efforts relate and support each other

### Improved Discovery
- **Related Content**: Find relevant documents through graph connections
- **Knowledge Gaps**: Identify areas needing additional documentation
- **Workflow Optimization**: Understand document dependencies and sequences

### Strategic Insights
- **Initiative Alignment**: Visualize how projects support strategic goals
- **Stakeholder Engagement**: Track involvement across multiple initiatives
- **Thematic Clustering**: See how strategic themes connect different efforts

## Link Quality Standards

### Intelligent Linking Criteria
- ✅ **Genuine Relationships**: Only linked documents with meaningful connections
- ✅ **Strategic Relevance**: Prioritized connections that support planning and execution
- ✅ **Contextual Integration**: Added links that enhance understanding
- ✅ **Balanced Approach**: Avoided over-linking while ensuring discoverability

### Relationship Strength Levels
- **High**: Direct implementation, shared projects, explicit cross-references
- **Medium**: Shared stakeholders, strong thematic alignment
- **Low**: Basic thematic overlap, tangential connections

## Next Steps

1. **Explore the Graph**: Open data/dclt/ in Obsidian to visualize connections
2. **Refine Relationships**: Review and adjust links as strategic priorities evolve
3. **Expand Network**: Add cross-references for new documents
4. **Monitor Usage**: Track which connections are most valuable for your workflow

---
*Cross-reference system optimized for strategic planning and execution workflows*
"""
        
        # Save report
        report_path = Path('output/reports/dclt_crossreference_analysis.md')
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save detailed relationship data
        relationship_data = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'stakeholders': list(self.stakeholders),
            'projects': list(self.projects),
            'themes': list(self.themes),
            'relationships': dict(self.relationships)
        }
        
        data_path = Path('output/reports/dclt_crossreference_data.json')
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(relationship_data, f, indent=2, default=str)
        
        return report_path
    
    def format_list(self, items):
        """Format list items for report"""
        if not items:
            return "None identified"
        
        formatted = []
        for item in items:
            if len(item.strip()) > 0:
                formatted.append(f"- {item}")
        
        if len(items) > len(formatted):
            formatted.append(f"... and {len(items) - len(formatted)} more")
        
        return '\n'.join(formatted) if formatted else "None identified"
    
    def build_cross_references(self):
        """Execute complete cross-reference building process"""
        print("=== DCLT Cross-Reference Builder ===")
        
        # Step 1: Scan all documents
        self.scan_all_documents()
        
        # Step 2: Identify relationships
        self.identify_relationships()
        
        # Step 3: Create cross-reference links
        self.create_cross_reference_links()
        
        # Step 4: Generate report
        report_path = self.generate_relationship_report()
        
        print(f"\n=== Cross-Reference Building Complete ===")
        print(f"Files analyzed: {self.stats['files_analyzed']}")
        print(f"Relationships found: {self.stats['relationships_found']}")
        print(f"Links created: {self.stats['links_created']}")
        print(f"Files updated: {self.stats['files_updated']}")
        print(f"Report saved: {report_path}")
        
        return report_path

def main():
    """Main cross-reference building function"""
    builder = DCLTCrossReferenceBuilder()
    result = builder.build_cross_references()
    
    print(f"\n✅ Cross-reference system complete!")
    print(f"📈 Your Obsidian graph now shows strategic relationships")
    print(f"📋 Review the analysis report for insights")

if __name__ == '__main__':
    main()