"""Load and validate YAML data files for clinic project data using Pydantic."""

import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Union
from pydantic import ValidationError

from data_models import Student, Project, MentorTA


class YAMLLoadError(Exception):
    """Exception raised when YAML loading fails."""
    pass


def _get_quarter_filename(quarter: str, year: int) -> str:
    """Get standardized filename for a quarter's YAML data.
    
    Args:
        quarter: Quarter name (Spring, Winter, Autumn)
        year: Year as integer
        
    Returns:
        Filename in format "{quarter_lower}_{year}.yaml"
    """
    quarter_lower = quarter.lower()
    return f"{quarter_lower}_{year}.yaml"


def load_students_for_quarter(quarter: str, year: int) -> List[Student]:
    """Load student data for a specific quarter from YAML file.
    
    Args:
        quarter: Quarter name (Spring, Winter, Autumn)
        year: Year as integer
        
    Returns:
        List of Student dataclass instances
        
    Raises:
        YAMLLoadError: If YAML file cannot be loaded or is invalid
    """
    # Get standardized filename
    filename = _get_quarter_filename(quarter, year)
    yaml_file = Path(__file__).parent / "data" / "students" / filename
    
    if not yaml_file.exists():
        raise YAMLLoadError(f"Student YAML file not found: {yaml_file}")
    
    try:
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise YAMLLoadError(f"Failed to parse YAML file {yaml_file}: {e}") from e
    except Exception as e:
        raise YAMLLoadError(f"Failed to read YAML file {yaml_file}: {e}") from e
    
    # Validate YAML structure
    if not isinstance(data, dict):
        raise YAMLLoadError(f"YAML file {yaml_file} must contain a dictionary at root level")
    
    required_fields = ["quarter", "year", "students"]
    for field in required_fields:
        if field not in data:
            raise YAMLLoadError(f"YAML file {yaml_file} missing required field: {field}")
    
    # Validate quarter and year match using DRY utility
    validate_quarter_year_match(data, quarter, year, str(yaml_file))
    
    # Convert students to Pydantic instances with automatic validation
    students = []
    student_data_list = data["students"]
    
    if not isinstance(student_data_list, list):
        raise YAMLLoadError(f"YAML file {yaml_file} 'students' field must be a list")
    
    for i, student_data in enumerate(student_data_list):
        if not isinstance(student_data, dict):
            raise YAMLLoadError(
                f"YAML file {yaml_file} student {i} must be a dictionary"
            )
        
        try:
            # Pydantic automatically validates all fields and types
            student = Student(**student_data)
            students.append(student)
        except ValidationError as e:
            raise YAMLLoadError(
                f"YAML file {yaml_file} student {i} validation failed: {e}"
            ) from e
    
    return students




def load_projects_for_quarter(quarter: str, year: int) -> Tuple[List[Project], Dict[str, str]]:
    """Load project data for a specific quarter from YAML file.
    
    Args:
        quarter: Quarter name (Spring, Winter, Autumn)
        year: Year as integer
        
    Returns:
        Tuple of (List of Project dataclass instances, name_map dictionary)
        
    Raises:
        YAMLLoadError: If YAML file cannot be loaded or is invalid
    """
    # Get standardized filename
    filename = _get_quarter_filename(quarter, year)
    yaml_file = Path(__file__).parent / "data" / "projects" / filename
    
    if not yaml_file.exists():
        raise YAMLLoadError(f"Project YAML file not found: {yaml_file}")
    
    try:
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise YAMLLoadError(f"Failed to parse YAML file {yaml_file}: {e}") from e
    except Exception as e:
        raise YAMLLoadError(f"Failed to read YAML file {yaml_file}: {e}") from e
    
    # Validate YAML structure
    if not isinstance(data, dict):
        raise YAMLLoadError(f"YAML file {yaml_file} must contain a dictionary at root level")
    
    required_fields = ["quarter", "year", "projects", "name_map"]
    for field in required_fields:
        if field not in data:
            raise YAMLLoadError(f"YAML file {yaml_file} missing required field: {field}")
    
    # Validate quarter and year match using DRY utility
    validate_quarter_year_match(data, quarter, year, str(yaml_file))
    
    # Convert projects to Pydantic instances with automatic validation
    projects = []
    project_data_list = data["projects"]
    
    if not isinstance(project_data_list, list):
        raise YAMLLoadError(f"YAML file {yaml_file} 'projects' field must be a list")
    
    for i, project_data in enumerate(project_data_list):
        if not isinstance(project_data, dict):
            raise YAMLLoadError(
                f"YAML file {yaml_file} project {i} must be a dictionary"
            )
        
        try:
            # Pydantic automatically validates all fields, types, and applies field validators
            project = Project(**project_data)
            projects.append(project)
        except ValidationError as e:
            raise YAMLLoadError(
                f"YAML file {yaml_file} project {i} ({project_data.get('org_name', 'unknown')}) validation failed: {e}"
            ) from e
    
    # Get name_map
    name_map = data.get("name_map", {})
    if not isinstance(name_map, dict):
        raise YAMLLoadError(f"YAML file {yaml_file} 'name_map' field must be a dictionary")
    
    return projects, name_map


def load_mentors_tas() -> Dict[str, MentorTA]:
    """Load mentor/TA data from YAML file.
    
    Returns:
        Dictionary mapping mentor keys to MentorTA instances
        
    Raises:
        YAMLLoadError: If YAML file cannot be loaded or is invalid
    """
    yaml_file = Path(__file__).parent / "data" / "mentors_tas.yaml"
    
    if not yaml_file.exists():
        raise YAMLLoadError(f"Mentors/TAs YAML file not found: {yaml_file}")
    
    try:
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise YAMLLoadError(f"Failed to parse YAML file {yaml_file}: {e}") from e
    except Exception as e:
        raise YAMLLoadError(f"Failed to read YAML file {yaml_file}: {e}") from e
    
    # Validate YAML structure
    if not isinstance(data, dict):
        raise YAMLLoadError(f"YAML file {yaml_file} must contain a dictionary at root level")
    
    # Convert to MentorTA instances
    mentors = {}
    for key, mentor_data in data.items():
        if not isinstance(mentor_data, dict):
            raise YAMLLoadError(f"YAML file {yaml_file} mentor '{key}' must be a dictionary")
        
        required_fields = ["display_name"]
        for field in required_fields:
            if field not in mentor_data:
                raise YAMLLoadError(f"YAML file {yaml_file} mentor '{key}' missing required field: {field}")
        
        try:
            # Create MentorTA instance with validation
            mentor = MentorTA(
                key=key,
                display_name=mentor_data["display_name"],
                url=mentor_data.get("url")  # url is optional
            )
            mentors[key] = mentor
        except Exception as e:
            raise YAMLLoadError(
                f"YAML file {yaml_file} mentor '{key}' validation failed: {e}"
            ) from e
    
    return mentors


def format_quarter_year_path(year: int, quarter: str) -> str:
    """Format year-quarter for file paths (DRY utility).
    
    Args:
        year: Year as integer
        quarter: Quarter name (e.g., "Spring")
        
    Returns:
        Formatted string like "2025-spring"
    """
    return f"{year}-{quarter.lower()}"


def validate_quarter_year_match(data: Dict[str, Union[str, int]], quarter: str, year: int, file_path: str) -> None:
    """Validate that YAML data matches expected quarter and year (DRY utility).
    
    Args:
        data: YAML data dictionary
        quarter: Expected quarter name
        year: Expected year
        file_path: Path to YAML file for error reporting
        
    Raises:
        YAMLLoadError: If quarter or year don't match
    """
    if data["quarter"] != quarter:
        raise YAMLLoadError(
            f"YAML file {file_path} has quarter '{data['quarter']}' but expected '{quarter}'"
        )
    if data["year"] != year:
        raise YAMLLoadError(
            f"YAML file {file_path} has year {data['year']} but expected {year}"
        )


