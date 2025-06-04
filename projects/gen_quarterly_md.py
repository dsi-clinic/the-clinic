"""This script generates markdown files for each quarter's projects.

It uses the data from `all_data.py` to create a structured list of projects,
students, mentors, and other relevant information. The output is saved in the
`past/` directory with filenames formatted as `year_quarter_projects.md`. The
markdown files are used by the clinic chatbot.
"""

from pathlib import Path

from all_data import (
    ALL_PEOPLE,
    AUTUMN_22_NAME_MAP,
    AUTUMN_22_PROJECT,
    AUTUMN_22_STUDENT,
    AUTUMN_23_NAME_MAP,
    AUTUMN_23_PROJECT,
    AUTUMN_23_STUDENT,
    AUTUMN_24_NAME_MAP,
    AUTUMN_24_PROJECT,
    AUTUMN_24_STUDENT,
    SPRING_23_NAME_MAP,
    SPRING_23_PROJECT,
    SPRING_23_STUDENT,
    SPRING_24_NAME_MAP,
    SPRING_24_PROJECT,
    SPRING_24_STUDENT,
    SPRING_25_NAME_MAP,
    SPRING_25_PROJECT,
    SPRING_25_STUDENT,
    WINTER_23_NAME_MAP,
    WINTER_23_PROJECT,
    WINTER_23_STUDENT,
    WINTER_24_NAME_MAP,
    WINTER_24_PROJECT,
    WINTER_24_STUDENT,
    WINTER_25_NAME_MAP,
    WINTER_25_PROJECT,
    WINTER_25_STUDENT,
)

PREAMBLE = """This is a list of projects run during the quarter, along with their relevant details.
"""


def create_single_quarter_table(
    quarter,
    year,
    name_map,
    project_map,
    student_info_list,
):
    """Create a markdown table for a single quarter's projects.

    Args:
        quarter (str): The quarter name (e.g., "Spring", "Winter", "Autumn").
        year (int): The year of the projects.
        name_map (dict): A mapping of project links to project names.
        project_map (list): A list of project information tuples.
        student_info_list (list): A list of student information tuples.

    Returns:
        str: A markdown formatted string containing the project details.
    """
    all_results = ""

    for project_info in project_map:
        # Loop over each project in project_map as the main loop
        # If a project does not appear in the project map then
        # it will not appear in the table.

        [
            project_link,
            project_description,
            project_url,
            mentor_link,
            ta_link,
            github_link,
            is_private_repo,
            has_one_pager,
            external_mentor_info,
            project_url_valid,
            is_11th_hour,
        ] = project_info

        # Project name -- replace with what is in name map if it exists
        project_name = name_map.get(project_link, project_link)

        eleventh_hour_text = " (11th Hour Sponsored)" if is_11th_hour else ""
        project_name_info = f"{project_name}{eleventh_hour_text}"

        # If there is a one-pager, then add a link to it.
        if has_one_pager:
            one_pager_location = f"https://dsi-clinic.github.io/the-clinic/projects/one-pagers/{year}-{quarter.lower()}/"
            file_info = one_pager_location + project_link + ".pdf"
            one_pager_info = f'{file_info.replace(" ", "%20")}'
        else:
            one_pager_info = ""

        # Mentor info. Assume that there is more than one and make a list.
        mentor_info = ""
        mentor_list = [mentor.strip() for mentor in mentor_link.split("&")]
        for mentor in mentor_list:
            # If the mentor is not in ALL_PEOPLE, then use the mentor name directly.
            if mentor not in ALL_PEOPLE:
                mentor_info += f"{mentor}, "
            else:
                mentor_info += f"{ALL_PEOPLE[mentor][0]}, "
        mentor_info = mentor_info[:-2]

        # Student info. Assume that there is more than one and make a list.
        student_info = ""
        student_project_list = [
            x for x in student_info_list if x[0] == project_link
        ]
        if len(student_project_list) == 0:
            raise Exception(f"No Students found for project {project_link}")
        for student in student_project_list:
            student_info += f"{student[1]}, "
        student_info = student_info[:-2]

        project_line = "".join(
            [
                f"## {project_name_info}\n",
                f"Description: {project_description}\n",
                f"One-pager: {one_pager_info}\n",
                f"Mentor: {mentor_info}\n",
                f"Students: {student_info}\n",
            ]
        )

        all_results += f"{project_line}\n"

    return all_results


if __name__ == "__main__":
    current_path = Path(__file__).parent
    out_path = current_path / "past"

    # Ensure the output directory exists
    if not out_path.exists():
        out_path.mkdir()

    # Define the quarters and years for which we want to generate markdown files
    quarters = ["Spring", "Winter", "Autumn"]
    years = [2025, 2024, 2023, 2022]

    # Define a mapping for the data associated with each quarter and year
    data_mapping = {
        "Spring": {
            2025: {
                "name_map": SPRING_25_NAME_MAP,
                "student_info_list": SPRING_25_STUDENT,
                "project_map": SPRING_25_PROJECT,
            },
            2024: {
                "name_map": SPRING_24_NAME_MAP,
                "student_info_list": SPRING_24_STUDENT,
                "project_map": SPRING_24_PROJECT,
            },
            2023: {
                "name_map": SPRING_23_NAME_MAP,
                "student_info_list": SPRING_23_STUDENT,
                "project_map": SPRING_23_PROJECT,
            },
        },
        "Winter": {
            2025: {
                "name_map": WINTER_25_NAME_MAP,
                "student_info_list": WINTER_25_STUDENT,
                "project_map": WINTER_25_PROJECT,
            },
            2024: {
                "name_map": WINTER_24_NAME_MAP,
                "student_info_list": WINTER_24_STUDENT,
                "project_map": WINTER_24_PROJECT,
            },
            2023: {
                "name_map": WINTER_23_NAME_MAP,
                "student_info_list": WINTER_23_STUDENT,
                "project_map": WINTER_23_PROJECT,
            },
        },
        "Autumn": {
            2024: {
                "name_map": AUTUMN_24_NAME_MAP,
                "student_info_list": AUTUMN_24_STUDENT,
                "project_map": AUTUMN_24_PROJECT,
            },
            2023: {
                "name_map": AUTUMN_23_NAME_MAP,
                "student_info_list": AUTUMN_23_STUDENT,
                "project_map": AUTUMN_23_PROJECT,
            },
            2022: {
                "name_map": AUTUMN_22_NAME_MAP,
                "student_info_list": AUTUMN_22_STUDENT,
                "project_map": AUTUMN_22_PROJECT,
            },
        },
    }

    # Build the list programmatically
    all_quarter_info_list = []
    for year in years:
        for quarter in quarters:
            if year in data_mapping.get(quarter, {}):
                all_quarter_info_list.append(
                    {
                        "quarter": quarter,
                        "year": year,
                        **data_mapping[quarter][year],
                    }
                )

    # Generate markdown files for each quarter
    for quarter in all_quarter_info_list:
        filename = f"{quarter['year']}_{quarter['quarter']}_projects.md"
        filename = out_path / filename
        with Path.open(filename, "w") as f_handle:
            f_handle.write(
                f"# {quarter['quarter']} {quarter['year']} Projects\n"
            )
            f_handle.write(PREAMBLE)
            f_handle.write(create_single_quarter_table(**quarter))
        print(f"Created {filename}")
