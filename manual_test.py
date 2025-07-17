#!/usr/bin/env python3
"""Manual test of link resolution using actual links from the Jekyll site"""

import sys
from pathlib import Path

sys.path.insert(0, "/Users/nickross/git/the-clinic")
from generate_sitemap import JekyllSiteMapper


def manual_test():
    """Test with actual links from the Jekyll site"""
    root_path = Path("/Users/nickross/git/the-clinic")
    mapper = JekyllSiteMapper(str(root_path))

    # Test cases from actual files
    test_cases = [
        # From README.md
        (
            "README.md",
            "prospective-students/",
            "Should find prospective-students directory",
        ),
        (
            "README.md",
            "students/",
            "Should find students directory",
        ),
        ("README.md", "mentor-ta/", "Should find mentor-ta directory"),
        (
            "README.md",
                "projects/index.md",
    "Should find projects/index.md",
        ),
        ("README.md", "faq/", "Should find faq directory"),
        # From students/index.md
        (
            "students/index.md",
            "../templates/",
            "Should find templates directory",
        ),
        ("students/index.md", "../rubrics/", "Should find rubrics directory"),
        (
            "students/index.md",
            "../tutorials/",
            "Should find tutorials directory",
        ),
        (
            "students/index.md",
            "../syllabus/",
            "Should find syllabus directory",
        ),
    ]

    print("Manual Test of Link Resolution:")
    print("=" * 50)

    for current_file, link_url, description in test_cases:
        current_path = root_path / current_file
        print(f"\nTest: {description}")
        print(f"  Current file: {current_file}")
        print(f"  Link URL: {link_url}")

        # Check if current file exists
        if not current_path.exists():
            print(f"  ❌ Current file doesn't exist: {current_path}")
            continue

        # Test the resolution
        result = mapper.resolve_link_path(current_path, link_url)
        print(f"  Resolved to: {result}")

        if result:
            resolved_path = root_path / result
            if resolved_path.exists():
                print("  Status: ✅ FOUND - File exists")
            else:
                print(
                    f"  Status: ❌ RESOLVED BUT FILE MISSING - {resolved_path}"
                )
        else:
            print("  Status: ❌ NOT RESOLVED")

            # Let's debug what files are actually there
            if link_url.startswith("./"):
                search_dir = current_path.parent / link_url[2:]
                print(f"  Debug: Looking for {search_dir}")
                if search_dir.exists():
                    print(
                        "  Debug: Found it! Path exists but resolution failed"
                    )
                else:
                    print("  Debug: Path doesn't exist")
                    parent = search_dir.parent
                    if parent.exists():
                        print("  Debug: Parent dir exists, contents:")
                        for item in parent.iterdir():
                            print(f"    - {item.name}")
                    else:
                        print("  Debug: Parent dir doesn't exist either")


if __name__ == "__main__":
    manual_test()
