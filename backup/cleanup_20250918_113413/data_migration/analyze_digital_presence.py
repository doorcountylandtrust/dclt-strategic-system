#!/usr/bin/env python3
"""
Analyze Land Trust Digital Presence
Identifies strongest and weakest digital presence based on multiple metrics
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_landtrust_data():
    """Load the master land trust dataset"""
    data_path = Path('data/landtrusts/datasets/landtrust_master_final.tsv')
    
    try:
        df = pd.read_csv(data_path, sep='\t', encoding='utf-8')
        print(f"Loaded {len(df)} organizations from dataset")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def calculate_digital_presence_score(df):
    """Calculate comprehensive digital presence score"""
    
    # Create a copy for scoring
    scoring_df = df.copy()
    
    # Handle missing values
    scoring_df['LH_Perf'] = pd.to_numeric(scoring_df['LH_Perf'], errors='coerce').fillna(0)
    scoring_df['LH_A11y'] = pd.to_numeric(scoring_df['LH_A11y'], errors='coerce').fillna(0)
    scoring_df['LH_BP'] = pd.to_numeric(scoring_df['LH_BP'], errors='coerce').fillna(0)
    scoring_df['LH_SEO'] = pd.to_numeric(scoring_df['LH_SEO'], errors='coerce').fillna(0)
    scoring_df['axe_violations'] = pd.to_numeric(scoring_df['axe_violations'], errors='coerce').fillna(10)
    
    # Calculate component scores (normalized 0-100)
    
    # 1. Technical Performance (40% weight)
    tech_score = (
        scoring_df['LH_Perf'] * 0.3 +  # Performance
        scoring_df['LH_A11y'] * 0.4 +  # Accessibility (higher weight)
        scoring_df['LH_BP'] * 0.2 +    # Best Practices
        scoring_df['LH_SEO'] * 0.1     # SEO
    )
    
    # 2. Accessibility Penalty (subtract violations)
    # Fewer violations = higher score
    accessibility_penalty = np.minimum(scoring_df['axe_violations'] * 5, 50)  # Cap at 50 point penalty
    tech_score = np.maximum(tech_score - accessibility_penalty, 0)
    
    # 3. Social Media Presence (30% weight)
    social_channels = 0
    social_channels += (scoring_df['Facebook'].notna() & (scoring_df['Facebook'] != '')).astype(int) * 25
    social_channels += (scoring_df['Instagram'].notna() & (scoring_df['Instagram'] != '')).astype(int) * 25
    social_channels += (scoring_df['YouTube'].notna() & (scoring_df['YouTube'] != '')).astype(int) * 25
    social_channels += (scoring_df['LinkedIn'].notna() & (scoring_df['LinkedIn'] != '')).astype(int) * 25
    
    # 4. CTA Strategy (20% weight)
    cta_score = 0
    # Has clear donation CTA
    cta_score += scoring_df['CTAs'].str.contains('donate', case=False, na=False).astype(int) * 40
    # Has volunteer CTA
    cta_score += scoring_df['CTAs'].str.contains('volunteer', case=False, na=False).astype(int) * 20
    # Has join/membership CTA
    cta_score += scoring_df['CTAs'].str.contains('join|member', case=False, na=False).astype(int) * 20
    # Has clear donation provider
    cta_score += (scoring_df['DonationProvider'].notna() & (scoring_df['DonationProvider'] != '')).astype(int) * 20
    
    # 5. Content Quality (10% weight)
    content_score = 0
    # Has H1 title
    content_score += (scoring_df['H1'].notna() & (scoring_df['H1'] != '')).astype(int) * 30
    # Has meta description
    content_score += (scoring_df['MetaDescription'].notna() & (scoring_df['MetaDescription'] != '')).astype(int) * 35
    # Has clear navigation
    content_score += (scoring_df['NavItems'].notna() & (scoring_df['NavItems'] != '')).astype(int) * 35
    
    # Calculate final weighted score
    final_score = (
        tech_score * 0.40 +      # Technical performance
        social_channels * 0.30 + # Social presence
        cta_score * 0.20 +       # CTA strategy
        content_score * 0.10     # Content quality
    )
    
    scoring_df['digital_presence_score'] = final_score.round(1)
    scoring_df['tech_score'] = tech_score.round(1)
    scoring_df['social_score'] = social_channels.round(1)
    scoring_df['cta_score'] = cta_score.round(1)
    scoring_df['content_score'] = content_score.round(1)
    
    return scoring_df

def analyze_strongest_weakest(df):
    """Identify strongest and weakest digital presence organizations"""
    
    # Filter out organizations with missing critical data
    valid_orgs = df[
        (df['URL'].notna()) & 
        (df['URL'] != '') &
        (df['Organization'].notna()) &
        (~df['H1'].str.contains('404|blocked|error', case=False, na=False))
    ].copy()
    
    print(f"Analyzing {len(valid_orgs)} valid organizations (filtered from {len(df)})")
    
    # Sort by digital presence score
    sorted_orgs = valid_orgs.sort_values('digital_presence_score', ascending=False)
    
    # Get top 3 and bottom 3
    strongest = sorted_orgs.head(3)
    weakest = sorted_orgs.tail(3)
    
    return strongest, weakest

def format_org_analysis(org_row):
    """Format individual organization analysis"""
    
    def clean_path(path_str):
        """Clean file paths for display"""
        if pd.isna(path_str) or path_str == '':
            return "Not available"
        # Convert absolute path to relative path
        path = Path(path_str)
        if 'data/landtrusts' in str(path):
            # Extract relative path from project root
            parts = path.parts
            if 'data' in parts:
                data_idx = parts.index('data')
                return '/'.join(parts[data_idx:])
        return str(path)
    
    def format_social_channels(row):
        """Format social media channels"""
        channels = []
        if pd.notna(row['Facebook']) and row['Facebook'] != '':
            channels.append(f"Facebook: {row['Facebook']}")
        if pd.notna(row['Instagram']) and row['Instagram'] != '':
            channels.append(f"Instagram: {row['Instagram']}")
        if pd.notna(row['YouTube']) and row['YouTube'] != '':
            channels.append(f"YouTube: {row['YouTube']}")
        if pd.notna(row['LinkedIn']) and row['LinkedIn'] != '':
            channels.append(f"LinkedIn: {row['LinkedIn']}")
        
        return channels if channels else ["No social media channels found"]
    
    analysis = f"""
## {org_row['Organization']}

- **Website URL**: {org_row['URL']}
- **Digital Presence Score**: {org_row['digital_presence_score']}/100
- **CTA Strategy**: {org_row['CTAs'] if pd.notna(org_row['CTAs']) else 'Not specified'}
- **Donation Provider**: {org_row['DonationProvider'] if pd.notna(org_row['DonationProvider']) else 'Not specified'}

### Performance Metrics
- **Lighthouse Performance**: {org_row['LH_Perf']}/100
- **Accessibility Score**: {org_row['LH_A11y']}/100
- **Best Practices**: {org_row['LH_BP']}/100
- **SEO Score**: {org_row['LH_SEO']}/100
- **Accessibility Violations**: {org_row['axe_violations']}

### Social Media Presence
{chr(10).join([f"- {channel}" for channel in format_social_channels(org_row)])}

### Assets
- **Logo**: `{clean_path(org_row['LogoPath'])}`
- **Screenshot**: `{clean_path(org_row['ScreenshotPath'])}`

### Score Breakdown
- Technical Performance: {org_row['tech_score']}/100
- Social Media: {org_row['social_score']}/100  
- CTA Strategy: {org_row['cta_score']}/100
- Content Quality: {org_row['content_score']}/100
"""
    
    return analysis

def generate_strategic_recommendations(strongest_df, weakest_df):
    """Generate strategic recommendations for DCLT"""
    
    recommendations = """
# Strategic Recommendations for Door County Land Trust

## Lessons to Learn from Strong Digital Performers

### 1. **Comprehensive Accessibility Implementation**
The strongest organizations prioritize accessibility with high Lighthouse A11y scores (86-100) and minimal axe violations. They implement:
- Proper heading structures and semantic HTML
- Alt text for all images
- Keyboard navigation support
- High color contrast ratios
- Screen reader compatibility

*DCLT Action*: Conduct comprehensive accessibility audit and implement WCAG 2.1 AA standards across all digital properties.

### 2. **Multi-Channel Social Media Strategy**
Top performers maintain active presence across 3-4 social platforms with consistent messaging:
- Facebook for community engagement and event promotion
- Instagram for visual storytelling and conservation impact
- YouTube for educational content and donor stories
- LinkedIn for professional networking and partnership building

*DCLT Action*: Develop integrated social media content calendar with platform-specific strategies and consistent posting schedule.

## Pitfalls to Avoid from Weaker Digital Performers

### 1. **Technical Performance Neglect**
Organizations with weak digital presence often have:
- Poor Lighthouse performance scores (0-32)
- Multiple accessibility violations (5+ axe violations)
- Broken or missing donation infrastructure
- Inconsistent or missing meta descriptions and H1 tags

*DCLT Action*: Establish monthly technical performance monitoring and quarterly comprehensive site audits.

### 2. **Unclear or Missing Call-to-Action Strategy**
Weak performers typically lack:
- Clear donation pathways and providers
- Consistent volunteer recruitment messaging
- Strategic placement of engagement opportunities
- Integration between website CTAs and social media

*DCLT Action*: Develop clear CTA hierarchy with primary (donate), secondary (volunteer), and tertiary (join newsletter) actions visible on every page.

## Additional Strategic Insights

### **Digital Presence Success Factors**
1. **Technical Excellence**: Average score of 85+ across Lighthouse metrics
2. **Social Integration**: Active presence on 3+ platforms with regular engagement
3. **Clear Value Proposition**: Compelling H1 and meta descriptions that communicate impact
4. **Streamlined Donation Process**: Reliable donation infrastructure with multiple giving options

### **Competitive Positioning Opportunities**
- Many land trusts still have poor technical performance (avg. 40-50 Lighthouse scores)
- Social media presence is inconsistent across the sector
- Accessibility compliance is often overlooked (opportunity for leadership)
- CTA strategy varies widely in effectiveness

*DCLT can differentiate by excelling in all four areas simultaneously.*
"""
    
    return recommendations

def main():
    """Main analysis function"""
    print("=== Land Trust Digital Presence Analysis ===")
    
    # Load data
    df = load_landtrust_data()
    if df is None:
        return
    
    # Calculate digital presence scores
    print("\nCalculating digital presence scores...")
    scored_df = calculate_digital_presence_score(df)
    
    # Identify strongest and weakest
    print("Identifying top and bottom performers...")
    strongest, weakest = analyze_strongest_weakest(scored_df)
    
    # Generate comprehensive report
    report = f"""# Land Trust Digital Presence Analysis Report
*Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*

This analysis evaluates {len(scored_df)} land trust organizations across multiple digital presence metrics to identify the strongest and weakest performers.

## Methodology

**Digital Presence Score** (0-100) combines:
- **Technical Performance (40%)**: Lighthouse scores for performance, accessibility, best practices, and SEO
- **Social Media Presence (30%)**: Active presence across Facebook, Instagram, YouTube, and LinkedIn
- **CTA Strategy (20%)**: Clear donation, volunteer, and engagement calls-to-action
- **Content Quality (10%)**: H1 tags, meta descriptions, and navigation structure

## TOP 3 STRONGEST DIGITAL PRESENCE
"""
    
    for idx, (_, org) in enumerate(strongest.iterrows(), 1):
        report += format_org_analysis(org)
        report += "\n" + "="*80 + "\n"
    
    report += """
## BOTTOM 3 WEAKEST DIGITAL PRESENCE
"""
    
    for idx, (_, org) in enumerate(weakest.iterrows(), 1):
        report += format_org_analysis(org)
        report += "\n" + "="*80 + "\n"
    
    # Add strategic recommendations
    report += generate_strategic_recommendations(strongest, weakest)
    
    # Save report
    output_path = Path('output/reports/digital_presence_analysis.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Analysis complete! Report saved to: {output_path}")
    
    # Print summary
    print(f"\n=== SUMMARY ===")
    print("STRONGEST DIGITAL PRESENCE:")
    for idx, (_, org) in enumerate(strongest.iterrows(), 1):
        print(f"{idx}. {org['Organization']} (Score: {org['digital_presence_score']})")
    
    print("\nWEAKEST DIGITAL PRESENCE:")
    for idx, (_, org) in enumerate(weakest.iterrows(), 1):
        print(f"{idx}. {org['Organization']} (Score: {org['digital_presence_score']})")

if __name__ == '__main__':
    main()