"""Generate the projects index.md markdown file.

This module creates a comprehensive table of all clinic projects organized by quarter,
with student information, mentor details, and project metadata.
"""

from typing import List, Dict, Optional, Union, Any
from data_models import MentorTA
from yaml_utils import load_students_for_quarter, load_projects_for_quarter, format_quarter_year_path, load_mentors_tas

# Constants for better maintainability
PREAMBLE_TEXT = """<!--- This file is generated from a script DO NOT EDIT \
DIRECTLY -->
### Previous Projects

This page contains a list of projects organized by quarter with the list of \
students who worked on the project and the faculty mentor. Note that the \
dates listed below are by _calendar year_ not academic year.

A few important notes:
* Not all projects have complete information. Some of the projects are under \
NDAs or other specifications (such as UChicago not hosting the repo).
* The requirements for the project have changed year over year and are \
sometimes project specific.
* Projects designated by a "&#8224;" were funded by <!-- \
markdown-link-check-disable -->\
[The 11th hour foundation](https://11thhourproject.org/)\
<!-- markdown-link-check-enable -->.

---
"""


# Supported quarters configuration
ALL_QUARTERS = [
    {"quarter": "Autumn", "year": 2025},
    {"quarter": "Spring", "year": 2025},
    {"quarter": "Winter", "year": 2025},
    {"quarter": "Autumn", "year": 2024},
    {"quarter": "Spring", "year": 2024},
    {"quarter": "Winter", "year": 2024},
    {"quarter": "Autumn", "year": 2023},
    {"quarter": "Spring", "year": 2023},
    {"quarter": "Winter", "year": 2023},
    {"quarter": "Autumn", "year": 2022},
]


# Removed: Now using format_quarter_year_path from yaml_utils for DRY compliance


def render_one_pager_info(has_one_pager: Optional[bool], year: int, quarter: str, project_link: str) -> str:
    """Render one-pager information based on the optional boolean status.
    
    Args:
        has_one_pager: True=has one-pager, False=explicitly no, None=missing/unknown
        year: Project year
        quarter: Project quarter
        project_link: Project identifier for filename
        
    Returns:
        HTML string for one-pager cell (link or empty string)
    """
    if has_one_pager is True:
        # Has a confirmed one-pager - create link
        one_pager_location = f"./one-pagers/{format_quarter_year_path(year, quarter)}/"
        file_info = one_pager_location + project_link + ".pdf"
        return f'<a href="{file_info.replace(" ", "%20")}">One-Pager</a>'
    else:
        # Either explicitly no one-pager (False) or unknown status (None)
        # Both render as empty string
        return ""


def _create_html_link(name: str, url: Optional[str]) -> str:
    """Create HTML link or plain text if no URL (DRY utility).
    
    Args:
        name: Display name
        url: Optional URL
        
    Returns:
        HTML link string or plain text
    """
    if url and url.strip():
        return f'<a href="{url}">{name}</a>'
    return name


def create_link_for_mentor(mentor_info: Union[MentorTA, List[str]]) -> str:
    """Create HTML link for mentor (supports both MentorTA objects and legacy format).
    
    Args:
        mentor_info: Either MentorTA object or legacy [name, url] list
        
    Returns:
        HTML link string
    """
    if hasattr(mentor_info, 'display_name'):
        # New MentorTA object format
        return _create_html_link(mentor_info.display_name, mentor_info.url)
    else:
        # Legacy [name, url] format (for student info compatibility)
        return _create_html_link(mentor_info[0], mentor_info[1])


def create_link_for_student(student_info: List[Optional[str]]) -> str:
    """Create HTML link for student with GitHub username handling.
    
    Args:
        student_info: List containing [project_name, student_name, github_info]
        
    Returns:
        HTML link string
    """
    name, github_info = student_info[1], student_info[2]
    
    if github_info is None or github_info.startswith("https://"):
        # Already a full URL or None
        return _create_html_link(name, github_info)
    else:
        # Just a username, prepend GitHub URL
        github_url = f"https://www.github.com/{github_info}"
        return _create_html_link(name, github_url)


def create_single_quarter_table(
    quarter: str,
    year: int,
    all_people: Dict[str, MentorTA],
    use_yaml_data: bool = True,
) -> str:
    """This returns a single table of information.
    A Table should be considered a single quarter.
    
    Args:
        quarter: Quarter name (e.g., "Spring", "Winter", "Autumn")
        year: Year as integer
        use_yaml_data: If True, load both students and projects from YAML files
        
    Returns:
        HTML table string for the quarter
    """
    # Load both student and project data from YAML
    if use_yaml_data:
        try:
            students = load_students_for_quarter(quarter, year)
            projects, name_map = load_projects_for_quarter(quarter, year)
        except Exception as e:
            print(f"Warning: Failed to load YAML data for {quarter} {year}: {e}")
            students = []
            projects = []
            name_map = {}
    else:
        raise ValueError("Legacy data loading not supported in this version")
        
    all_results = """<table>
        <thead>
            <tr>
                <th>Org. Name</th>
                <th>Project Desc.</th>
                <th>Repository</th>
                <th>One-Pager</th>
                <th>Mentor(s)</th>
                <th>Students</th>
                <th>External Mentor(s)</th>
                <th>TA</th>
            </tr>
        </thead>
        <tbody>
    """

    for project in projects:
        # Extract project fields directly from Pydantic model
        project_link = project.org_name
        project_description = project.description
        project_url = project.project_url
        mentor_link = project.mentor
        ta_link = project.ta
        github_link = project.github_link
        is_private_repo = project.is_private_repo
        has_one_pager = project.has_one_pager
        external_mentor_info = project.external_mentor_info
        project_url_valid = project.project_url_valid
        is_11th_hour = project.is_11th_hour

        # Project name -- replace with what is in name map if it exists
        project_name = name_map.get(project_link, project_link)

        # Add url to the name. If the invalid flag is 1, add flag to not check
        # link via the markdown link checker
        if is_11th_hour:
            project_name = f"{project_name}&#8224;"

        if project_url_valid:
            project_name_info = f'<a href="{project_url}">{project_name}</a>'
        else:
            project_name_info = f'<a href="{project_url}">{project_name}</a>'

        # If the repo is private then mark it as such
        if is_private_repo:
            if github_link:
                repo_info = f'<a href="{github_link}">Private Repo</a>'
            else:
                repo_info = "No Repository"
        else:
            repo_info = f'<a href="{github_link}">DSI Repo</a>'

        # Render one-pager info using the new Optional[bool] logic
        one_pager_info = render_one_pager_info(has_one_pager, year, quarter, project_link)

        # Mentor list. split by "&". Make a bullet point list
        mentor_list = [mentor.strip() for mentor in mentor_link.split("&")]

        mentor_info = "<ul>"
        for mentor in mentor_list:
            mentor_info += (
                f"<li>{create_link_for_mentor(all_people[mentor])}</li>"
            )
        mentor_info += "</ul>"

        # Student info - build HTML list
        student_info = "<ul>"
        project_students = [
            student for student in students if student.project_name == project_link
        ]
        if not project_students:
            raise ValueError(f"No Students found for project {project_link}")
        for student in project_students:
            # Convert to legacy format for create_link_for_student function
            student_legacy = [student.project_name, student.student_name, student.github_info]
            student_info += f"<li>{create_link_for_student(student_legacy)}</li>"
        student_info += "</ul>"

        # TA -- same logic as above, but handle the case with no TA
        TA_info = all_people.get(ta_link, None)
        if TA_info:
            ta_str = "<ul>"
            ta_str += f"<li>{create_link_for_mentor(TA_info)}</li>"
            ta_str += "</ul>"
        else:
            ta_str = ""

        # External mentor info. Handle both HTML and plain text formats.
        external_mentor_str = ""
        if external_mentor_info:
            # Check if the external mentor info already contains HTML
            if external_mentor_info.strip().startswith("<ul>") and external_mentor_info.strip().endswith("</ul>"):
                # Already formatted as HTML, use as-is
                external_mentor_str = external_mentor_info.strip()
            else:
                # Plain text format, split by "&" and create HTML list
                external_mentor_str = "<ul>"
                for mentor in external_mentor_info.split("&"):
                    mentor = mentor.strip()
                    if mentor:  # Only add non-empty mentors
                        external_mentor_str += f"<li>{mentor}</li>"
                external_mentor_str += "</ul>"

        project_line = "".join(
            [
                f"<td>{project_name_info}</td>",
                f"<td>{project_description}</td>",
                f"<td>{repo_info}</td>",
                f"<td>{one_pager_info}</td>",
                f"<td>{mentor_info}</td>",
                f"<td>{student_info}</td>",
                f"<td>{external_mentor_str}</td>",
                f"<td>{ta_str}</td>",
            ]
        )
        all_results += f"<tr>{project_line}</tr>\n"

    all_results += "</tbody></table>"

    return all_results


def main() -> None:
    """Main function to generate the index.md file."""
    # Load mentors/TAs data
    try:
        all_people = load_mentors_tas()
    except Exception as e:
        print(f"Error loading mentors/TAs data: {e}")
        return
    
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(PREAMBLE_TEXT)
        f.write("\n")

        for quarter in ALL_QUARTERS:
            f.write("\n<details>\n\n")
            f.write(
                f"<summary style=\"cursor: pointer; font-weight: bold; font-size: 1.5em; margin-bottom: 10px;\">{quarter['quarter']} {quarter['year']}</summary>\n\n"
                f"This quarter's pitchbook, which contains the basic project "
                f"specification can be found "
                f'<a href="./pitchbooks/'
                f"{format_quarter_year_path(quarter['year'], quarter['quarter'])}"
                f'-pitchbook.pdf">here</a>.\n\n'
            )
            f.write(create_single_quarter_table(all_people=all_people, **quarter))
            f.write("\n</details>")


if __name__ == "__main__":
    main()