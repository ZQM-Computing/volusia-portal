#!/usr/bin/env python3
"""Generate comprehensive employer reports from the SQLite database."""

import sqlite3
import os
from datetime import datetime

DB_PATH = r'C:\Users\zqmco\14_Projects\Active\Project-Volusia\Data\volusia_employers.db'
OUTPUT_DIR = r'C:\Users\zqmco\14_Projects\Active\Project-Volusia\Report\EMPLOYERS'

def get_sector_type(sector_name):
    if not sector_name:
        return "Various"
    mapping = {
        "Healthcare & Life Sciences": "Healthcare",
        "Education": "Education",
        "Government & Public Safety": "Government",
        "Aviation / Aerospace": "Aerospace",
        "Insurance & Financial Services": "Financial",
        "Manufacturing": "Manufacturing",
        "Logistics & Distribution": "Logistics",
        "Retail": "Retail",
        "Hospitality & Entertainment": "Hospitality",
        "Utilities & Infrastructure": "Utilities",
        "Construction": "Construction",
        "Professional Services": "Professional Services",
        "Technology & IT": "Technology",
        "Non-profit & Community": "Non-profit",
        "Real Estate & Development": "Real Estate",
        "Arts, Culture & Recreation": "Arts & Culture",
        "Agriculture & Food Production": "Agriculture",
    }
    return mapping.get(sector_name, sector_name)

def get_employers(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.employer_id, e.name, e.hq_in_volusia, e.is_public, e.approx_employees,
               e.avg_annual_wage_override, e.description, e.website, e.contact_email, e.contact_phone, e.contact_notes,
               s.name as sector_name,
               c.name as city_name
        FROM employers e
        JOIN sectors s ON e.sector_id = s.sector_id
        JOIN cities c ON e.city_id = c.city_id
        ORDER BY e.employer_id
    """)
    return cursor.fetchall()

def get_signals_for_employer(conn, employer_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT signal_id, signal_type, source, date_seen, date_posted,
               title, family, pay_min, pay_max, pay_unit,
               remote_eligible, entry_level, cash_priority,
               confidence, signal_tag, notes
        FROM hiring_signals
        WHERE employer_id = ?
        ORDER BY date_posted DESC
    """, (employer_id,))
    return cursor.fetchall()

def get_jobs_for_employer(conn, employer_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_id, title, family, remote_eligible, entry_level, 
               pay_type, pay_min, pay_max, pay_unit, url, apply_url,
               apply_email, apply_phone, cash_priority, notes, posted_date, source
        FROM jobs 
        WHERE employer_id = ?
        ORDER BY title
    """, (employer_id,))
    return cursor.fetchall()

def format_pay(pay_min, pay_max, pay_type, pay_unit):
    if pay_min and pay_max:
        unit = pay_unit if pay_unit else 'hr'
        return f"${pay_min}-{pay_max}/{unit}"
    elif pay_min:
        unit = pay_unit if pay_unit else 'hr'
        return f"${pay_min}+/{unit}"
    elif pay_max:
        unit = pay_unit if pay_unit else 'hr'
        return f"Up to ${pay_max}/{unit}"
    else:
        return "Not specified"

def format_apply(apply_url, apply_email, apply_phone):
    parts = []
    if apply_url:
        parts.append(f"[Apply]({apply_url})")
    if apply_email:
        parts.append(f"email {apply_email}")
    if apply_phone:
        parts.append(f"phone {apply_phone}")
    return " | ".join(parts) if parts else "Contact via website"

def format_employer_report(employer, jobs, signals):
    (employer_id, name, hq_in_volusia, is_public, approx_employees,
     wage_override, description, website, contact_email, contact_phone, contact_notes,
     sector_name, city_name) = employer
    
    name = name or "Unknown Employer"
    hq_status = "Yes" if hq_in_volusia else "No"
    public_status = "Yes" if is_public else "No"
    state = "FL"
    sector_type = get_sector_type(sector_name)
    city_name = city_name or "Unknown City"
    approx_employees_str = f"{approx_employees:,}" if approx_employees else "Unknown"
    
    lines = [f"# Employer Profile: {name}"]
    lines.append("")
    lines.append("## Basic Information")
    lines.append(f"- **Name**: {name}")
    lines.append(f"- **Sector**: {sector_name or 'Unknown'}")
    lines.append(f"- **Sector Type**: {sector_type}")
    lines.append(f"- **City**: {city_name}, {state}")
    lines.append(f"- **Headquarters in Volusia**: {hq_status}")
    lines.append(f"- **Public/Government/Education**: {public_status}")
    lines.append(f"- **Employer ID**: {employer_id}")
    lines.append(f"- **Approximate Employees**: {approx_employees_str}")
    if wage_override:
        lines.append(f"- **Avg Annual Wage Override**: ${wage_override:,}")
    if description:
        lines.append(f"- **Description**: {description}")
    lines.append("")
    lines.append("## Contact Information")
    if website:
        lines.append(f"- **Website**: [{website}]({website})")
    if contact_email:
        lines.append(f"- **Email**: {contact_email}")
    if contact_phone:
        lines.append(f"- **Phone**: {contact_phone}")
    if contact_notes:
        lines.append(f"- **Notes**: {contact_notes}")
    lines.append("")
    lines.append("## Job Openings")
    lines.append("")
    
    if not jobs:
        lines.append("*No current job postings in database*\n")
    else:
        for job in jobs:
            job_id, title, family, remote_eligible, entry_level, \
                pay_type, pay_min, pay_max, pay_unit, url, apply_url, \
                apply_email, apply_phone, cash_priority, notes, posted_date, source = job
            
            remote = "Yes" if remote_eligible else "No"
            entry = "Yes" if entry_level else "No"
            pay_str = format_pay(pay_min, pay_max, pay_type, pay_unit)
            apply_str = format_apply(apply_url, apply_email, apply_phone)
            
            lines.append(f"### {title or 'Untitled'}")
            lines.append(f"- **Family**: {family or 'General'}")
            lines.append(f"- **Pay**: {pay_str}")
            lines.append(f"- **Remote**: {remote} | **Entry**: {entry}")
            lines.append(f"- **Apply**: {apply_str}")
            if notes:
                lines.append(f"- **Notes**: {notes}")
            lines.append("")
        
        lines.append(f"*Total Jobs: {len(jobs)}*\n")
    
    lines.append("## Hiring Signals")
    lines.append("")
    if not signals:
        lines.append("*No hiring signals recorded*\n")
    else:
        for sig in signals:
            signal_id, signal_type, source, date_seen, date_posted, \
                title, family, pay_min, pay_max, pay_unit, \
                remote_eligible, entry_level, cash_priority, \
                confidence, signal_tag, notes = sig
            
            pay_str = format_pay(pay_min, pay_max, pay_type=None, pay_unit=pay_unit)
            lines.append(f"- **{title or 'Unknown'}** ({signal_type}) — {pay_str} [{confidence}]")
            if notes:
                lines.append(f"  - {notes}")
        lines.append("")
        lines.append(f"*Total Signals: {len(signals)}*\n")
    
    lines.append("## Data Source")
    lines.append("- Source: Local database extraction")
    lines.append(f"- Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("- Database: volusia_employers.db")
    lines.append(f"- Records: {len(jobs) if jobs else 0} job postings")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated from Project Volusia database - verify all details at source links above*")
    
    return "\n".join(lines)

def main():
    conn = sqlite3.connect(DB_PATH)
    
    employers = get_employers(conn)
    
    print(f"Generating reports for {len(employers)} employers...")
    
    for employer in employers:
        employer_id = employer[0]
        name = employer[1]
        
        jobs = get_jobs_for_employer(conn, employer_id)
        signals = get_signals_for_employer(conn, employer_id)
        report = format_employer_report(employer, jobs, signals)
        
        filename = f"{employer_id:03d}-{name.replace('/', '_').replace(' ', '_')}.md" if name else f"{employer_id:03d}-unknown.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w') as f:
            f.write(report)
        
        print(f"  Generated: {filename} ({len(jobs)} jobs, {len(signals)} signals)")
    
    conn.close()
    print(f"\nDone! Reports saved to {OUTPUT_DIR}")

if __name__ == '__main__':
    main()