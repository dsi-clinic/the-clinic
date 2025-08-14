"""Data models for clinic project information using Pydantic.

This module defines Pydantic models that represent the structure of clinic project data,
providing automatic type validation, conversion, and serialization.
"""

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


class Quarter(str, Enum):
    """Valid quarter names."""
    
    SPRING = "Spring"
    WINTER = "Winter"
    AUTUMN = "Autumn"


class MentorTA(BaseModel):
    """Represents a mentor or TA with their information."""
    
    key: str = Field(..., min_length=1, description="The key used to reference them")
    display_name: str = Field(..., min_length=1, description="The name displayed on the website")
    url: Optional[str] = Field(None, description="Their personal/professional URL")
    
    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        """Validate URL format."""
        if v is not None and v.strip():
            v = v.strip()
            if not v.startswith(('http://', 'https://')):
                raise ValueError('URL must start with http:// or https://')
            return v
        return None
    
    @property
    def has_url(self) -> bool:
        """Check if this mentor/TA has a valid URL."""
        return bool(self.url)


class Project(BaseModel):
    """Represents a clinic project with all associated metadata."""

    org_name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    project_url: Union[str, None] = Field(default="")
    mentor: str = Field(..., min_length=1, description="Could be multiple separated by &")
    ta: Union[str, None] = Field(default="")
    github_link: Union[str, None] = Field(default="")
    is_private_repo: bool = Field(default=False)
    has_one_pager: Optional[bool] = Field(
        default=None, 
        description="True=has one-pager, False=explicitly no, None=missing/unknown"
    )
    external_mentor_info: Union[str, None] = Field(default="")
    project_url_valid: bool = Field(default=False)
    is_11th_hour: bool = Field(default=False)

    @field_validator('github_link')
    @classmethod
    def validate_github_link(cls, v):
        """Validate GitHub link format, handle None values."""
        if v is None:
            return ""
        if v and v.strip():
            v = v.strip()
            if not v.startswith(('http://', 'https://')):
                raise ValueError('GitHub link must start with http:// or https://')
            return v
        return ""

    @field_validator('project_url')
    @classmethod
    def clean_project_url(cls, v):
        """Clean project URL, handle None values."""
        if v is None:
            return ""
        return v.strip() if v else ""

    @field_validator('external_mentor_info')
    @classmethod
    def clean_external_mentor_info(cls, v):
        """Clean external mentor info, handle None values."""
        if v is None:
            return ""
        return v.strip() if v else ""

    @field_validator('ta')
    @classmethod
    def clean_ta(cls, v):
        """Clean TA field, handle None values."""
        if v is None:
            return ""
        return v.strip() if v else ""

    @model_validator(mode='after')
    def validate_project_url_consistency(self):
        """Validate project URL if marked as valid."""
        if self.project_url_valid and self.project_url:
            if not self.project_url.startswith(('http://', 'https://')):
                raise ValueError(f'Invalid project URL format: {self.project_url}')
        return self

    @property
    def mentor_list(self) -> List[str]:
        """Return list of mentors split by '&' character."""
        return [mentor.strip() for mentor in self.mentor.split("&") if mentor.strip()]

    @property
    def external_mentor_list(self) -> List[str]:
        """Return list of external mentors split by '&' character."""
        if not self.external_mentor_info:
            return []
        return [mentor.strip() for mentor in self.external_mentor_info.split("&") if mentor.strip()]

    @property
    def has_valid_one_pager(self) -> bool:
        """Check if this project has a confirmed one-pager."""
        return self.has_one_pager is True

    @property
    def one_pager_status(self) -> str:
        """Get human-readable one-pager status."""
        if self.has_one_pager is True:
            return "Available"
        elif self.has_one_pager is False:
            return "Not Available"
        else:  # None
            return "Unknown"


class Student(BaseModel):
    """Represents a student with their project and GitHub info."""
    
    project_name: str = Field(..., min_length=1)
    student_name: str = Field(..., min_length=1)
    github_info: Optional[str] = Field(default=None)

    @field_validator('github_info')
    @classmethod
    def validate_github_info(cls, v):
        """Clean up GitHub info."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None


class QuarterData(BaseModel):
    """Represents all data for a specific quarter."""
    
    quarter: Quarter
    year: int = Field(..., ge=2020, le=2030)
    projects: List[Project]
    students: List[Student]
    name_map: Dict[str, str] = Field(default_factory=dict)

    @model_validator(mode='after')
    def validate_student_project_mapping(self):
        """Ensure students and projects are properly linked."""
        project_names = {p.org_name for p in self.projects}
        student_projects = {s.project_name for s in self.students}
        
        # Check for students referencing non-existent projects
        missing_projects = student_projects - project_names
        if missing_projects:
            raise ValueError(f"Students reference non-existent projects: {missing_projects}")
        
        return self

    def validate_mentor_references(self, all_people: Dict[str, Union[MentorTA, List[str]]]):
        """Validate that mentors and TAs exist in ALL_PEOPLE dictionary.
        
        Args:
            all_people: Dictionary mapping mentor names to either MentorTA objects or [name, url] lists
        """
        warnings = []
        
        for project in self.projects:
            # Check mentors
            for mentor in project.mentor_list:
                if mentor and mentor not in all_people:
                    warnings.append(
                        f"Mentor '{mentor}' not found in ALL_PEOPLE for project {project.org_name}"
                    )
            
            # Check TA
            if project.ta and project.ta not in all_people:
                warnings.append(
                    f"TA '{project.ta}' not found in ALL_PEOPLE for project {project.org_name}"
                )
        
        return warnings

    @property
    def project_count(self) -> int:
        """Return number of projects in this quarter."""
        return len(self.projects)

    @property  
    def student_count(self) -> int:
        """Return number of students in this quarter."""
        return len(self.students)


# ALL_PEOPLE dictionary has been moved to data/mentors_tas.yaml
# Use yaml_utils.load_mentors_tas() to load the data