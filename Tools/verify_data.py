#!/usr/bin/env python3
"""
Data verification script for Project Volusia employer database.
Verifies data integrity and consistency across all sources.
"""

import sqlite3
import os
import sys

DB_PATH = r'C:\Users\zqmco\14_Projects\Active\Project-Volusia\Data\volusia_employers.db'
EMPLOYER_PROFILES_DIR = r'C:\Users\zqmco\14_Projects\Active\Project-Volusia\Report\EMPLOYERS'

def verify_data():
    """Verify data consistency across all sources."""
    issues = []
    warnings = []
    
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}")
        return 1
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Count employers
    cursor.execute("SELECT COUNT(*) FROM employers")
    employer_count = cursor.fetchone()[0]
    print(f"Employers in database: {employer_count}")
    
    # Count jobs
    cursor.execute("SELECT COUNT(*) FROM jobs")
    job_count = cursor.fetchone()[0]
    print(f"Jobs in database: {job_count}")
    
    # Count sectors
    cursor.execute("SELECT COUNT(*) FROM sectors")
    sector_count = cursor.fetchone()[0]
    print(f"Sectors: {sector_count}")
    
    # Count cities
    cursor.execute("SELECT COUNT(*) FROM cities")
    city_count = cursor.fetchone()[0]
    print(f"Cities: {city_count}")
    
    # Check foreign key integrity
    cursor.execute("""
        SELECT j.job_id, j.title 
        FROM jobs j 
        LEFT JOIN employers e ON j.employer_id = e.employer_id 
        WHERE e.employer_id IS NULL
    """)
    orphan_jobs = cursor.fetchall()
    if orphan_jobs:
        issues.append(f"Found {len(orphan_jobs)} jobs with invalid employer references")
    
    # Check sector references
    cursor.execute("""
        SELECT e.employer_id, e.name 
        FROM employers e 
        LEFT JOIN sectors s ON e.sector_id = s.sector_id 
        WHERE s.sector_id IS NULL
    """)
    invalid_sectors = cursor.fetchall()
    if invalid_sectors:
        issues.append(f"Found {len(invalid_sectors)} employers with invalid sector references")
    
    # Check city references
    cursor.execute("""
        SELECT e.employer_id, e.name 
        FROM employers e 
        LEFT JOIN cities c ON e.city_id = c.city_id 
        WHERE c.city_id IS NULL
    """)
    invalid_cities = cursor.fetchall()
    if invalid_cities:
        issues.append(f"Found {len(invalid_cities)} employers with invalid city references")
    
    # Check for duplicate employer names
    cursor.execute("""
        SELECT name, COUNT(*) as cnt 
        FROM employers 
        GROUP BY name 
        HAVING COUNT(*) > 1
    """)
    duplicates = cursor.fetchall()
    if duplicates:
        warnings.append(f"Found {len(duplicates)} duplicate employer names")
    
    conn.close()
    
    # Check employer profiles directory
    profile_count = 0
    if os.path.exists(EMPLOYER_PROFILES_DIR):
        profiles = [f for f in os.listdir(EMPLOYER_PROFILES_DIR) if f.endswith('.md')]
        profile_count = len(profiles)
        print(f"Employer profiles: {profile_count}")
    else:
        warnings.append(f"Employer profiles directory not found: {EMPLOYER_PROFILES_DIR}")
    
    # Summary
    print("\n=== VERIFICATION SUMMARY ===")
    print(f"Employers: {employer_count}")
    print(f"Jobs: {job_count}")
    print(f"Profiles generated: {profile_count}")
    
    if issues:
        print("\n❌ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not issues and not warnings:
        print("\n✅ All data verified successfully!")
    
    # Check profile count vs employer count
    if profile_count and employer_count:
        if profile_count != employer_count:
            warnings.append(f"Profile count ({profile_count}) differs from employer count ({employer_count})")
    
    return 0

if __name__ == "__main__":
    sys.exit(verify_data())