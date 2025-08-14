"""Load and validate clinic data using Pydantic models.

This module provides functions to load YAML data and validate it using Pydantic models,
ensuring data integrity and type safety with automatic validation.
"""

from typing import Dict, List, Tuple
from pydantic import ValidationError

from data_models import QuarterData
from yaml_utils import load_students_for_quarter, load_projects_for_quarter, load_mentors_tas, YAMLLoadError


class DataValidationError(Exception):
    """Custom exception for data validation errors."""

    pass


def validate_quarter_data(quarter: str, year: int) -> QuarterData:
    """Load and validate a complete quarter's data using Pydantic.
    
    Args:
        quarter: Quarter name (Spring, Winter, Autumn)
        year: Year as integer
        
    Returns:
        Validated QuarterData instance with automatic Pydantic validation
        
    Raises:
        DataValidationError: If loading or validation fails
    """
    try:
        # Load projects and students from YAML files
        # Pydantic validation happens automatically in the loaders
        projects, name_map = load_projects_for_quarter(quarter, year)
        students = load_students_for_quarter(quarter, year)

        # Create QuarterData with automatic Pydantic validation
        quarter_data = QuarterData(
            quarter=quarter,
            year=year,
            projects=projects,
            students=students,
            name_map=name_map,
        )

        return quarter_data
        
    except YAMLLoadError as e:
        raise DataValidationError(f"Failed to load YAML data for {quarter} {year}: {e}") from e
    except ValidationError as e:
        raise DataValidationError(f"Failed to validate {quarter} {year} data: {e}") from e
    except Exception as e:
        raise DataValidationError(f"Unexpected error validating {quarter} {year}: {e}") from e


def validate_all_quarters(print_warnings: bool = True) -> Dict[str, QuarterData]:
    """Validate all quarters and return structured data.
    
    Args:
        print_warnings: If True, print validation warnings to stdout
    
    Returns:
        Dictionary mapping quarter keys to validated QuarterData instances
        
    Raises:
        DataValidationError: If any quarter fails validation
    """
    # Define all quarters (both projects and students now come from YAML)
    quarters_data = [
        ("Spring", 2025),
        ("Winter", 2025),
        ("Autumn", 2024),
        ("Spring", 2024),
        ("Winter", 2024),
        ("Autumn", 2023),
        ("Spring", 2023),
        ("Winter", 2023),
        ("Autumn", 2022),
    ]

    validated_quarters = {}
    validation_errors = []
    all_warnings = []
    
    # Load mentors/TAs data once for all validations
    try:
        all_people = load_mentors_tas()
    except YAMLLoadError as e:
        raise DataValidationError(f"Failed to load mentors/TAs data: {e}") from e

    for quarter, year in quarters_data:
        quarter_key = f"{quarter}_{year}"
        try:
            validated_data = validate_quarter_data(quarter, year)
            validated_quarters[quarter_key] = validated_data
            
            # Collect warnings for this quarter
            mentor_warnings = validated_data.validate_mentor_references(all_people)
            if mentor_warnings:
                all_warnings.extend([f"{quarter} {year}: {warning}" for warning in mentor_warnings])
                
        except DataValidationError as e:
            validation_errors.append(f"{quarter_key}: {e}")

    if validation_errors:
        error_msg = "Validation failed for quarters:\n" + "\n".join(validation_errors)
        raise DataValidationError(error_msg)

    # Print warnings and data quality issues
    if print_warnings:
        _print_validation_warnings(validated_quarters, all_warnings)

    return validated_quarters


def _format_quarter_project_info(quarter_data: QuarterData, project_name: str) -> str:
    """Format quarter and project info for warnings.
    
    Args:
        quarter_data: QuarterData instance
        project_name: Name of the project
        
    Returns:
        Formatted string like "Spring 2025: ProjectName"
    """
    return f"{quarter_data.quarter.value} {quarter_data.year}: {project_name}"


def _print_validation_warnings(validated_data: Dict[str, QuarterData], mentor_warnings: List[str]) -> None:
    """Print validation warnings to stdout."""
    print()  # Empty line for spacing
    
    # Print mentor/TA warnings
    if mentor_warnings:
        print("⚠️  MENTOR/TA WARNINGS:")
        for warning in mentor_warnings:
            print(f"   {warning}")
        print()
    
    # Calculate statistics for warnings
    all_quarters = list(validated_data.values())
    
    # Projects without external mentors
    projects_without_external = []
    for quarter_data in all_quarters:
        for project in quarter_data.projects:
            if not project.external_mentor_info or not project.external_mentor_info.strip():
                projects_without_external.append(_format_quarter_project_info(quarter_data, project.org_name))
    
    if projects_without_external:
        print("⚠️  MISSING EXTERNAL MENTORS:")
        for project_info in projects_without_external:
            print(f"   {project_info}")
        print()
    
    # Projects with explicitly no one-pagers (None is acceptable, don't warn about it)
    projects_no_onepager = []
    for quarter_data in all_quarters:
        for project in quarter_data.projects:
            if project.has_one_pager is False:
                projects_no_onepager.append(_format_quarter_project_info(quarter_data, project.org_name))
    
    if projects_no_onepager:
        print("⚠️  EXPLICITLY NO ONE-PAGERS:")
        for project_info in projects_no_onepager:
            print(f"   {project_info}")
        print()
    
    # Summary statistics
    no_external_mentor_count = len(projects_without_external)
    no_one_pager_count = len(projects_no_onepager)
    total_projects = sum(q.project_count for q in all_quarters)
    
    print(f"📊 DATA QUALITY SUMMARY:")
    print(f"   Projects without external mentors: {no_external_mentor_count}/{total_projects} ({no_external_mentor_count/total_projects*100:.1f}%)")
    print(f"   Projects with explicitly no one-pagers: {no_one_pager_count}/{total_projects} ({no_one_pager_count/total_projects*100:.1f}%)")
    
    private_repo_count = sum(1 for q in all_quarters for p in q.projects if p.is_private_repo)
    eleventh_hour_count = sum(1 for q in all_quarters for p in q.projects if p.is_11th_hour)
    confirmed_onepager_count = sum(1 for q in all_quarters for p in q.projects if p.has_one_pager is True)
    unknown_onepager_count = sum(1 for q in all_quarters for p in q.projects if p.has_one_pager is None)
    
    print(f"   Private repositories: {private_repo_count}/{total_projects} ({private_repo_count/total_projects*100:.1f}%)")
    print(f"   11th Hour sponsored projects: {eleventh_hour_count}/{total_projects} ({eleventh_hour_count/total_projects*100:.1f}%)")
    print(f"   Confirmed one-pagers: {confirmed_onepager_count}/{total_projects} ({confirmed_onepager_count/total_projects*100:.1f}%)")
    print(f"   One-pager status unknown: {unknown_onepager_count}/{total_projects} ({unknown_onepager_count/total_projects*100:.1f}%)")


def generate_validation_report() -> str:
    """Generate a human-readable validation report.
    
    Returns:
        String containing detailed validation report
    """
    try:
        validated_data = validate_all_quarters(print_warnings=False)
        
        # Load mentors/TAs data for report generation
        try:
            all_people = load_mentors_tas()
        except YAMLLoadError as e:
            return f"❌ Failed to load mentors/TAs data: {e}"
        
        report_lines = ["# Data Validation Report", ""]
        
        # Summary statistics
        total_projects = sum(q.project_count for q in validated_data.values())
        total_students = sum(q.student_count for q in validated_data.values())
        
        report_lines.extend([
            f"## Summary",
            f"- Total quarters: {len(validated_data)}",
            f"- Total projects: {total_projects}",
            f"- Total students: {total_students}",
            "",
        ])
        
        # Per-quarter details
        report_lines.append("## Quarter Details")
        for quarter_key, quarter_data in sorted(validated_data.items()):
            report_lines.extend([
                f"### {quarter_data.quarter.value} {quarter_data.year}",
                f"- Projects: {quarter_data.project_count}",
                f"- Students: {quarter_data.student_count}",
                "",
            ])
            
            # Check for mentor warnings
            mentor_warnings = quarter_data.validate_mentor_references(all_people)
            if mentor_warnings:
                report_lines.append("**Warnings:**")
                for warning in mentor_warnings:
                    report_lines.append(f"- {warning}")
                report_lines.append("")
        
        # Data quality checks
        report_lines.extend([
            "## Data Quality Checks",
            "",
        ])
        
        all_quarters = list(validated_data.values())
        
        # Check for projects without one-pagers
        no_one_pager_count = sum(
            1 for q in all_quarters 
            for p in q.projects 
            if not p.has_one_pager
        )
        report_lines.append(f"- Projects without one-pagers: {no_one_pager_count}")
        
        # Check for private repos
        private_repo_count = sum(
            1 for q in all_quarters 
            for p in q.projects 
            if p.is_private_repo
        )
        report_lines.append(f"- Private repositories: {private_repo_count}")
        
        # Check for 11th hour projects
        eleventh_hour_count = sum(
            1 for q in all_quarters 
            for p in q.projects 
            if p.is_11th_hour
        )
        report_lines.append(f"- 11th Hour sponsored projects: {eleventh_hour_count}")
        
        # Check for projects without external mentors
        no_external_mentor_count = sum(
            1 for q in all_quarters 
            for p in q.projects 
            if not p.external_mentor_info or not p.external_mentor_info.strip()
        )
        report_lines.append(f"- Projects without external mentors: {no_external_mentor_count}")
        
        # Check for projects with external mentors
        with_external_mentor_count = sum(
            1 for q in all_quarters 
            for p in q.projects 
            if p.external_mentor_info and p.external_mentor_info.strip()
        )
        report_lines.append(f"- Projects with external mentors: {with_external_mentor_count}")
        
        
        report_lines.extend(["", "✅ All validations passed successfully!"])
        
        return "\n".join(report_lines)
        
    except DataValidationError as e:
        return f"❌ Validation failed:\n{e}"


# CLI interface for standalone validation
def main() -> int:
    """Main validation function for CLI usage."""
    import argparse
    import sys
    from pathlib import Path
    
    parser = argparse.ArgumentParser(
        description="Validate all clinic project data"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate detailed validation report to file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true", 
        help="Show verbose output"
    )
    parser.add_argument(
        "--output", "-o",
        default="validation_report.txt",
        help="Output file for detailed report (default: validation_report.txt)"
    )
    
    args = parser.parse_args()
    
    print("🔍 Validating clinic project data...")
    
    try:
        # Run validation
        validated_data = validate_all_quarters()
        
        # Success message
        total_quarters = len(validated_data)
        total_projects = sum(q.project_count for q in validated_data.values())
        total_students = sum(q.student_count for q in validated_data.values())
        
        print("✅ All data validation passed!")
        print(f"   📊 Validated {total_quarters} quarters")
        print(f"   📋 {total_projects} projects")
        print(f"   👥 {total_students} students")
        
        if args.verbose:
            print("\n📑 Quarter breakdown:")
            for quarter_key, quarter_data in sorted(validated_data.items()):
                print(f"   {quarter_data.quarter.value} {quarter_data.year}: "
                      f"{quarter_data.project_count} projects, "
                      f"{quarter_data.student_count} students")
        
        # Generate detailed report if requested
        if args.report:
            print(f"\n📝 Generating detailed report to {args.output}...")
            report = generate_validation_report()
            
            output_path = Path(args.output)
            output_path.write_text(report, encoding="utf-8")
            print(f"   Report saved to {output_path.absolute()}")
            
            # Show warnings from report if any
            if "**Warnings:**" in report:
                print("\n⚠️  Some warnings found - check the report for details")
        
        return 0
        
    except DataValidationError as e:
        print(f"❌ Data validation failed:")
        print(f"   {e}")
        
        # Try to generate partial report for debugging
        if args.report:
            try:
                print(f"\n📝 Attempting to generate error report to {args.output}...")
                report = generate_validation_report()  # This will include error details
                
                output_path = Path(args.output)
                output_path.write_text(report, encoding="utf-8")
                print(f"   Error report saved to {output_path.absolute()}")
            except Exception as report_error:
                print(f"   Could not generate error report: {report_error}")
        
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected error during validation:")
        print(f"   {e}")
        
        if args.verbose:
            import traceback
            print("\n🔍 Full traceback:")
            traceback.print_exc()
        
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())


