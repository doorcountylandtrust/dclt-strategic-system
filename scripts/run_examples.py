#!/usr/bin/env python3
"""
Example Usage Script for DCLT Strategic System Query Tools

This script demonstrates how to use the various query and analysis tools
with practical examples of strategic planning questions.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent))

from frontmatter_parser import FrontmatterParser
from resource_conflict_analyzer import ResourceConflictAnalyzer
from dependency_analyzer import DependencyAnalyzer
from strategic_query import StrategicQueryEngine
from dashboard_generator import DashboardGenerator

def run_example_queries():
    """Run example queries to demonstrate system capabilities."""
    
    print("="*60)
    print("DCLT Strategic System - Example Queries")
    print("="*60)
    print()
    
    # Initialize the system
    print("📊 Initializing Strategic Planning System...")
    parser = FrontmatterParser()
    query_engine = StrategicQueryEngine(parser)
    conflict_analyzer = ResourceConflictAnalyzer(parser)
    dependency_analyzer = DependencyAnalyzer(parser)
    dashboard_gen = DashboardGenerator(parser)
    
    print(f"✅ Loaded {len(parser.projects)} projects with frontmatter")
    print()
    
    # Example queries from the user's request
    example_queries = [
        "What work requires communications team in Q4 2025?",
        "Show dependencies between brand and website projects",
        "Identify resource conflicts in upcoming quarters"
    ]
    
    print("🔍 Running Example Queries:")
    print()
    
    for i, question in enumerate(example_queries, 1):
        print(f"{i}. {question}")
        print("-" * len(f"{i}. {question}"))
        
        # Execute query
        results = query_engine.query(question)
        
        print(f"Query Type: {results['query_type']}")
        print(f"Summary: {results['summary']}")
        
        if results['recommendations']:
            print("Recommendations:")
            for rec in results['recommendations'][:2]:  # Top 2
                print(f"  • {rec}")
        
        print()
    
    # Additional example queries
    additional_queries = [
        "High priority projects",
        "Rebrand initiative projects",
        "Projects starting in July 2025",
        "Brand strategy work",
        "External vendor projects"
    ]
    
    print("🎯 Additional Strategic Queries:")
    print()
    
    for question in additional_queries[:3]:  # Top 3
        results = query_engine.query(question)
        print(f"📋 {question}: {results['summary']}")
    
    print()
    
    # Resource conflict analysis
    print("⚠️  Resource Conflict Analysis:")
    print("-" * 35)
    
    resource_analysis = conflict_analyzer.analyze_resource_conflicts()
    workload = resource_analysis.get('resource_workload', {})
    
    for resource, data in list(workload.items())[:3]:  # Top 3 resources
        print(f"{resource.replace('-', ' ').title()}: {data['total_projects']} projects")
        if data['high_priority'] > 0:
            print(f"  └─ {data['high_priority']} high priority")
    
    print()
    
    # Dependency analysis
    print("🔗 Dependency Analysis:")
    print("-" * 25)
    
    critical_path = dependency_analyzer.find_critical_path()
    if critical_path:
        total_duration = sum(duration for _, duration in critical_path)
        print(f"Critical Path: {len(critical_path)} projects, {total_duration} days")
        print("Key projects:")
        for project, duration in critical_path[:3]:  # First 3
            print(f"  • {project} ({duration} days)")
    
    bottlenecks = dependency_analyzer.identify_bottlenecks()
    if bottlenecks:
        print(f"\nBottlenecks: {len(bottlenecks)} identified")
        for bottleneck in bottlenecks[:2]:  # Top 2
            print(f"  • {bottleneck['project']} (blocks {bottleneck['dependents_count']} projects)")
    
    print()
    
    # Brand-Website specific analysis
    brand_website = dependency_analyzer.analyze_brand_website_dependencies()
    print("🎨 Brand-Website Dependencies:")
    print("-" * 35)
    print(f"Brand Projects: {brand_website['brand_projects']}")
    print(f"Website Projects: {brand_website['website_projects']}")
    print(f"Cross-Dependencies: {len(brand_website['cross_dependencies'])}")
    
    if brand_website['parallel_opportunities']:
        print(f"Parallel Opportunities: {len(brand_website['parallel_opportunities'])}")
    
    print()
    
    # Generate sample reports
    print("📊 Generating Sample Reports...")
    print("-" * 35)
    
    # Resource conflict report
    conflict_analyzer.generate_report(output_file="sample_resource_analysis.md")
    print("✅ Resource conflict analysis: output/reports/sample_resource_analysis.md")
    
    # Dependency report
    dependency_analyzer.generate_dependency_report(output_file="sample_dependency_analysis.md")
    print("✅ Dependency analysis: output/reports/sample_dependency_analysis.md")
    
    # Strategic query results
    sample_query = query_engine.query("communications team work in Q3 2025", output_file="sample_query_results.md")
    print("✅ Strategic query results: output/reports/sample_query_results.md")
    
    print()
    
    # Dashboard generation
    print("📈 Generating Executive Dashboard...")
    print("-" * 40)
    
    dashboard_gen.generate_executive_dashboard("sample_executive_dashboard.md")
    print("✅ Executive dashboard: output/reports/sample_executive_dashboard.md")
    
    print()
    print("="*60)
    print("🎉 Example queries completed successfully!")
    print("="*60)
    print()
    print("📋 Generated Reports:")
    print("  • Resource conflict analysis")
    print("  • Project dependency analysis") 
    print("  • Strategic query results")
    print("  • Executive dashboard")
    print()
    print("💡 Usage Tips:")
    print("  • Use natural language queries with strategic_query.py")
    print("  • Run resource analysis before major project phases")
    print("  • Check dependencies before timeline changes")
    print("  • Generate dashboards weekly for leadership")
    print()

def demonstrate_cli_usage():
    """Demonstrate command line usage of the tools."""
    
    print("💻 Command Line Usage Examples:")
    print("-" * 40)
    print()
    
    examples = [
        {
            'description': 'Ask natural language questions',
            'command': 'python scripts/strategic_query.py "What work requires communications team in Q3 2025?"'
        },
        {
            'description': 'Analyze resource conflicts for specific quarter',
            'command': 'python scripts/resource_conflict_analyzer.py --quarter Q3-2025'
        },
        {
            'description': 'Focus on brand-website dependencies',
            'command': 'python scripts/dependency_analyzer.py --focus brand-website'
        },
        {
            'description': 'Generate all strategic dashboards',
            'command': 'python scripts/dashboard_generator.py --type all'
        },
        {
            'description': 'Generate executive dashboard only',
            'command': 'python scripts/dashboard_generator.py --type executive'
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['description']}:")
        print(f"   {example['command']}")
        print()
    
    print("📁 All reports saved to: output/reports/")
    print()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run examples for DCLT Strategic System")
    parser.add_argument("--demo", choices=['queries', 'cli', 'all'], default='all',
                       help="Type of demo to run")
    
    args = parser.parse_args()
    
    if args.demo in ['queries', 'all']:
        run_example_queries()
    
    if args.demo in ['cli', 'all']:
        demonstrate_cli_usage()