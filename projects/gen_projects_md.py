# This code generates the projects.md markdown file in this repository.
# To do:
# 1. automate 400 no-400 for has repo

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



def create_link_for_mentor(mentor_info):
    # Takes in a mentor blob (what is in ALL_PEOPLE)
    # and returns a string HTML link
    if mentor_info[1]:
        return f'<a href="{mentor_info[1]}">{mentor_info[0]}</a>'
    else:
        return f"{mentor_info[0]}"


def create_link_for_student(student_info):
    # If the github username is only the username, prepend the GitHub URL.
    # Additional logic as student info is more complicated.
    if student_info[2] is None or student_info[2].startswith("https://"):
        return create_link_for_mentor(student_info[1:3])
    else:
        return create_link_for_mentor(
            [student_info[1], f"https://www.github.com/{student_info[2]}"]
        )


def create_single_quarter_table(
    quarter,
    year,
    name_map,
    project_map,
    student_info_list,
):
    """This returns a single table of information.
    A Table should be considered a single quarter.
    """
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

        # If there is a one-pager, then add a link to it.
        if has_one_pager:
            one_pager_location = f"./one-pagers/{year}-{quarter.lower()}/"
            file_info = one_pager_location + project_link + ".pdf"
            one_pager_info = (
                f'<a href="{file_info.replace(" ", "%20")}">One-Pager</a>'
            )
        else:
            one_pager_info = ""

        # Mentor list. split by "&". Make a bullet point list
        mentor_list = [mentor.strip() for mentor in mentor_link.split("&")]

        mentor_info = "<ul>"
        for mentor in mentor_list:
            mentor_info += (
                f"<li>{create_link_for_mentor(ALL_PEOPLE[mentor])}</li>"
            )
        mentor_info += "</ul>"

        # Student info. Assume that there is more than one and make a list.
        student_info = "<ul>"
        student_project_list = [
            x for x in student_info_list if x[0] == project_link
        ]
        if len(student_project_list) == 0:
            raise Exception(f"No Students found for project {project_link}")
        for student in student_project_list:
            student_info += f"<li>{create_link_for_student(student)}</li>"
        student_info += "</ul>"

        # TA -- same logic as above, but handle the case with no TA
        TA_info = ALL_PEOPLE.get(ta_link, None)
        if TA_info:
            ta_str = "<ul>"
            ta_str += f"<li>{create_link_for_mentor(TA_info)}</li>"
            ta_str += "</ul>"
        else:
            ta_str = ""

        # External mentor info. Assume more than one and make a list.
        external_mentor_str = ""
        if external_mentor_info:
            external_mentor_str = "<ul>"
            for mentor in external_mentor_info.split("&"):
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


if __name__ == "__main__":
    # The creation of this should be automated
    # this is pretty lazy.
    all_quarter_info_list = [
        {
            "quarter": "Spring",
            "year": "2025",
            "name_map": SPRING_25_NAME_MAP,
            "student_info_list": SPRING_25_STUDENT,
            "project_map": SPRING_25_PROJECT,
        },
        {
            "quarter": "Winter",
            "year": "2025",
            "name_map": WINTER_25_NAME_MAP,
            "student_info_list": WINTER_25_STUDENT,
            "project_map": WINTER_25_PROJECT,
        },
        {
            "quarter": "Autumn",
            "year": "2024",
            "name_map": AUTUMN_24_NAME_MAP,
            "student_info_list": AUTUMN_24_STUDENT,
            "project_map": AUTUMN_24_PROJECT,
        },
        {
            "quarter": "Spring",
            "year": "2024",
            "name_map": SPRING_24_NAME_MAP,
            "student_info_list": SPRING_24_STUDENT,
            "project_map": SPRING_24_PROJECT,
        },
        {
            "quarter": "Winter",
            "year": "2024",
            "name_map": WINTER_24_NAME_MAP,
            "student_info_list": WINTER_24_STUDENT,
            "project_map": WINTER_24_PROJECT,
        },
        {
            "quarter": "Autumn",
            "year": "2023",
            "name_map": AUTUMN_23_NAME_MAP,
            "student_info_list": AUTUMN_23_STUDENT,
            "project_map": AUTUMN_23_PROJECT,
        },
        {
            "quarter": "Spring",
            "year": "2023",
            "name_map": SPRING_23_NAME_MAP,
            "student_info_list": SPRING_23_STUDENT,
            "project_map": SPRING_23_PROJECT,
        },
        {
            "quarter": "Winter",
            "year": "2023",
            "name_map": WINTER_23_NAME_MAP,
            "student_info_list": WINTER_23_STUDENT,
            "project_map": WINTER_23_PROJECT,
        },
        {
            "quarter": "Autumn",
            "year": "2022",
            "name_map": AUTUMN_22_NAME_MAP,
            "student_info_list": AUTUMN_22_STUDENT,
            "project_map": AUTUMN_22_PROJECT,
        },
    ]

    with open("projects.md", "w") as f_handle:
        f_handle.write(PREAMBLE_TEXT)
        f_handle.write("\n")

        for quarter in all_quarter_info_list:
            f_handle.write("\n<details>\n\n")
            f_handle.write(
                f"<summary style=\"cursor: pointer; font-weight: bold; font-size: 1.5em; margin-bottom: 10px;\">{quarter['quarter']} {quarter['year']}</summary>\n\n"
                f"This quarter's pitchbook, which contains the basic project "
                f"specification can be found "
                f'<a href="./pitchbooks/'
                f"{quarter['year']}-{quarter['quarter'].lower()}"
                f'-pitchbook.pdf">here</a>.\n\n'
            )
            f_handle.write(create_single_quarter_table(**quarter))
            f_handle.write("\n</details>")
