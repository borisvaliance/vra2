#!/usr/bin/env python
"""
Simple test script for the Disaster Plan Analyzer
Tests core functionality without requiring a test framework
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import extract_best_practices, extract_text_from_txt


def test_text_extraction():
    """Test text extraction from sample file"""
    print("Testing text extraction...")
    sample_file = "sample_plans/springfield_disaster_plan.txt"
    
    if not os.path.exists(sample_file):
        print(f"❌ Sample file not found: {sample_file}")
        return False
    
    text = extract_text_from_txt(sample_file)
    
    if len(text) > 0:
        print(f"✓ Successfully extracted {len(text)} characters from sample file")
        return True
    else:
        print("❌ Failed to extract text from sample file")
        return False


def test_best_practices_extraction():
    """Test best practices extraction"""
    print("\nTesting best practices extraction...")
    
    # Sample text for testing
    sample_text = """
    Fire Safety Procedures
    
    All buildings must ensure fire extinguishers are inspected annually.
    Staff should evacuate the building immediately when the fire alarm sounds.
    Buildings must implement a fire alarm system that is tested monthly.
    
    Flood Response Plan
    
    The city should maintain a comprehensive drainage system.
    Residents must be notified 48 hours in advance when flood warnings are issued.
    Evacuation routes from flood-prone areas should be clearly marked.
    """
    
    # Test fire-related practices
    fire_practices = extract_best_practices(sample_text, "fire")
    if len(fire_practices) > 0:
        print(f"✓ Found {len(fire_practices)} fire-related practices")
        for i, practice in enumerate(fire_practices[:3], 1):
            print(f"  {i}. {practice[:80]}...")
    else:
        print("❌ No fire-related practices found")
        return False
    
    # Test flood-related practices
    flood_practices = extract_best_practices(sample_text, "flood")
    if len(flood_practices) > 0:
        print(f"✓ Found {len(flood_practices)} flood-related practices")
        for i, practice in enumerate(flood_practices[:3], 1):
            print(f"  {i}. {practice[:80]}...")
    else:
        print("❌ No flood-related practices found")
        return False
    
    return True


def test_disaster_types():
    """Test that all disaster types can extract practices"""
    print("\nTesting all disaster types...")
    
    sample_text = """
    Emergency Preparedness Guidelines
    
    For fire emergencies, evacuate the building immediately.
    During floods, move to higher ground and avoid walking through water.
    Hurricane preparation should include securing outdoor items.
    Earthquake safety requires drop, cover, and hold on procedures.
    Tornado warnings require immediate shelter in interior rooms.
    """
    
    disaster_types = ["fire", "flood", "hurricane", "earthquake", "tornado"]
    results = {}
    
    for disaster_type in disaster_types:
        practices = extract_best_practices(sample_text, disaster_type)
        results[disaster_type] = len(practices)
        status = "✓" if len(practices) > 0 else "❌"
        print(f"  {status} {disaster_type.capitalize()}: {len(practices)} practices found")
    
    # At least 4 out of 5 should find something
    success_count = sum(1 for count in results.values() if count > 0)
    if success_count >= 4:
        print(f"✓ {success_count}/5 disaster types successfully extracted practices")
        return True
    else:
        print(f"❌ Only {success_count}/5 disaster types found practices")
        return False


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Disaster Plan Analyzer - Test Suite")
    print("=" * 60)
    
    tests = [
        test_text_extraction,
        test_best_practices_extraction,
        test_disaster_types,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
