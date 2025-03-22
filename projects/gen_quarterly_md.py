# This code generates quarterly reports of historical projects

from all_data import (
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
# Previous Projects

This page contains a list of projects organized by quarter with the list of \
students who worked on the project and the faculty mentor. Note that the \
dates listed below are by _calendar year_ not academic year.

---
"""

# Format: Name which links : [Name to display, github link]
# DON'T USE LinkedIn as it breaks b/c the github runner does not
# have an account

# This should be for people who appear more than once
# Specifically TAs and Mentors.
ALL_PEOPLE = {
    "Bill Trok": [
        "Bill Trok",
        "https://datascience.uchicago.edu/people/bill-trok/",
    ],
    "YJ Choe": ["YJ Choe", "https://yjchoe.github.io/"],
    "Isaac": ["Isaac Mehlhaff", "http://imehlhaff.net/"],
    "Rituparno Mandal": [
        "Rituparno Mandal",
        "https://scholar.google.co.in/citations?user=ObZopO8AAAAJ&hl=en",
    ],
    "Chong Liu": ["Chong Liu", "https://chong-l.github.io/"],
    "Jonatas Marques": ["Jonatas Marques", "https://jonatasamarques.com/"],
    "Chris": [
        "Chris Redmond",
        "https://datascience.uchicago.edu/people/chris-redmond/",
    ],
    "Satadisha Saha Bhowmick": [
        "Satadisha Saha Bhowmick",
        "https://datascience.uchicago.edu/people/satadisha-saha-bhowmick/",
    ],
    "Eddie": [
        "Ming-Chieh (Eddie) Liu",
        "https://datascience.uchicago.edu/people/ming-chieh-eddie-liu/",
    ],
    "Jessica J": ["Yuxin Ji (Jessica)", "https://github.com/Yuxin-Ji"],
    "Yiran": ["Yiran Hao", "https://github.com/chiertu"],
    "Soham": ["Soham Gurjar", "https://github.com/soham239"],
    "James Turk": ["James Turk", "https://github.com/jamesturk/"],
    "Nick": ["Nick Ross", "https://www.nickross.site/"],
    "Launa": ["Launa Greer", "https://github.com/LaunaG"],
    "Rahim": ["Rahim Rasool", "https://github.com/rahimrasool"],
    "David U.": [
        "David Uminsky",
        "https://cs.uchicago.edu/people/david-uminsky/",
    ],
    "Dan N.": [
        "Dan Nicolae",
        "https://www.stat.uchicago.edu/~nicolae/",
    ],
    "Tim": ["Tim Hannifan", "https://github.com/timhannifan"],
    "Ali": ["Ali Klemencic", "https://github.com/aliklemencic"],
    "Christian": ["Christian Jordan", "https://github.com/chrjor"],
    "Anthony K": ["Anthony Kanellopoulos", "https://github.com/kanello"],
    "Kenia": ["Kenia Godinez Nogueda", "https://github.com/gnogueda"],
    "Patricia": [
        "Patricia Chiril",
        "https://scholar.google.com/citations?user=AzsyeyIAAAAJ&hl=en",
    ],
    "Peter": ["Peter Lu", "https://github.com/peterparity"],
    "Anna": [
        "Anna Woodard",
        "https://scholar.google.com/citations?user=1Gs8kcYAAAAJ&hl=en",
    ],
    "Todd": ["Todd Nief", "https://github.com/toddnief"],
    "Yuetian": ["Yuetian Luo", "https://yuetianluo.github.io/"],
    "Victor": ["Victor Perez Martin", "https://github.com/vperezmartin"],
    "UT": ["Utkarsh Tripathi", "https://github.com/redgene"],
    "Avery": ["Avery Schoen", "https://github.com/averyschoen"],
    "Sunvid": ["Sunvid Aneja", "https://github.com/sunvidaneja"],
    "Trevor": ["Trevor Spreadbury", "https://github.com/trevorspreadbury"],
    "Riley": [
        "Riley Tucker",
        "https://scholar.google.com/citations?user=j8TVqU8AAAAJ&hl=en",
    ],
    "Jeffrey": [
        "Jeffrey Negrea",
        "https://scholar.google.ca/citations?user=woSzLBMAAAAJ&hl=en",
    ],
    "Yu-Wei Chen": ["Yu-Wei Chen", "https://github.com/ywchen814"],
    "Amanda": ["Amanda Kube", "https://github.com/amandakube"],
    "Evelyn": ["Evelyn Campbell", "https://github.com/campbelle1"],
    "Utkarsh": ["Utkarsh Tripathi", "https://github.com/redgene"],
    "Susanna": ["Susanna Lange", "https://github.com/SusannaLange"],
    "Fei": ["Fei Wang", "https://github.com/chenhuifei01"],
    "Grant": ["Yuwei (Grant) Chen", "https://github.com/ywchen814"],
    "Rita": ["Rita Xu", "https://github.com/catalystxu"],
    "Sarah": ["Sarah Walker", "https://github.com/sarahwalker10"],
    "Vasileios": [
        "Vasileios Charisopoulos",
        "https://scholar.google.com/citations?user=X3V6rM8AAAAJ&hl=el",
    ],
    "Ridhi": ["Ridhi Purohit", "https://github.com/ridhi96"],
    "Cristina": [
        "Cristina Garbacea",
        "https://scholar.google.com/citations?user=302eGI0AAAAJ&hl=en",
    ],
    "Rishabh": ["Rishabh Shastry", ""],
    "Satadisha": [
        "Satadisha Saha Bhowmick",
        "https://scholar.google.com.hk/citations?user=B-cTWkEAAAAJ",
    ],
    "Owen": ["Owen Melina", ""],
    "Alexander": [
        "Alexander Bogatskiy",
        "https://datascience.uchicago.edu/people/alexander-bogatskiy/",
    ],
    "Jie Jian": [
        "Jie Jian",
        "https://datascience.uchicago.edu/people/jie-jian/",
    ],
    "Jonatas": [
        "Jonatas Marques",
        "https://datascience.uchicago.edu/people/jonatas-marques/",
    ],
    "Liya": [
        "Liya Ding",
        "https://datascience.uchicago.edu/people/liya-ding/",
    ],
    "Julia": [
        "Julia Mendelsohn",
        "https://scholar.google.com/citations?user=-RVWgYUAAAAJ&hl=en",
    ],
    "Meghan": [
        "Meghan Hutch",
        "https://datascience.uchicago.edu/people/meghan-hutch-she-her/",
    ],
    "Seyed": [
        "Seyed Esmaeili",
        "https://datascience.uchicago.edu/people/seyed-a-esmaeili/",
    ],
    "Susan": [
        "Susan Paykin",
        "https://datascience.uchicago.edu/people/susan-paykin/",
    ],
    "Kelly": [
        "Kelly Smalenberger",
        "https://datascience.uchicago.edu/people/kelly-smalenberger/",
    ],
    "Kriti": [
        "Kriti Sehgal",
        "https://datascience.uchicago.edu/people/kriti-sehgal/",
    ],
    "Jingchao": ["Jingchao Fang", "https://jc-fang.github.io/"],
    "Ganghua": [
        "Ganghua Wang",
        "https://scholar.google.com/citations?user=GpbeNCsAAAAJ&hl=en",
    ],
    "Cassie": ["Cassie Tang", "https://github.com/cassietang717"],
    "Ian": ["Ian Joffe", "https://github.com/IanJoffe"],
    "Justin": ["Justin Wang", "https://github.com/jiazheng-wang-yes"],
    "Stella": ["Stella Chen", "https://github.com/stellaaachen"],
    "Grace": ["Grace Shao", "https://github.com/graceshaoy"],
    "Yukai": ["Yukai Yang", "https://github.com/YukaiYang0803"],
    "Austin": ["Austin Steinhart", "https://github.com/asteinhart"],
    "Francesco Pinto": [
        "Francesco Pinto",
        "https://datascience.uchicago.edu/people/francesco-pinto/",
    ],
    "Harper": ["Harper Lyu", "https://github.com/dwlyu"],
    "Harper Schwab": ["Harper Schwab", "https://github.com/hwschwab"],
    "Gayathri Jayaraman": [
        "Gayathri Jayaraman",
        "https://github.com/gayathrij-hub",
    ],
    "Jack Sanderson": ["Jack Sanderson", "https://github.com/jcksanderson"],
    "Polly Ren": ["Polly Ren", "https://github.com/pollyren"],
}


def create_link_for_mentor(mentor_info):
    # Takes in a mentor blob (what is in ALL_PEOPLE)
    # and returns a string HTML link
    if mentor_info[1]:
        return f'{mentor_info[0]}'
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
    """
    This returns a single table of information.
    A Table should be considered a single quarter.
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
        project_name_info = f'{project_name}{eleventh_hour_text}'

        # If the repo is private then mark it as such
        if is_private_repo:
            if github_link:
                repo_info = f'[Private]({github_link})'
            else:
                repo_info = "No Repository"
        else:
            repo_info = f'[DSI Repo]({github_link})'

        # If there is a one-pager, then add a link to it.
        if has_one_pager:
            one_pager_location = f"https://dsi-clinic.github.io/the-clinic/projects/one-pagers/{year}-{quarter.lower()}/"
            file_info = one_pager_location + project_link + ".pdf"
            one_pager_info = (
                f'{file_info.replace(" ", "%20")}')
        else:
            one_pager_info = ""

        # Mentor list. split by "&". Make a bullet point list
        mentor_list = [mentor.strip() for mentor in mentor_link.split("&")]

        mentor_info = ""
        for mentor in mentor_list:
            mentor_info += (
                f"{create_link_for_mentor(ALL_PEOPLE[mentor])}, ")
        mentor_info = mentor_info[:-2]

        # Student info. Assume that there is more than one and make a list.
        student_info = ""
        student_project_list = [x for x in student_info_list if x[0]
                                == project_link]
        if len(student_project_list) == 0:
            raise Exception(f"No Students found for project {project_link}")
        for student in student_project_list:
            student_info += f"{create_link_for_student(student)}, "
        student_info = student_info[:-2]

        # TA -- same logic as above, but handle the case with no TA
        TA_info = ALL_PEOPLE.get(ta_link, None)
        if TA_info:
            ta_str = f"{create_link_for_mentor(TA_info)}"
        else:
            ta_str = ""

        # External mentor info. Assume more than one and make a list.
        external_mentor_str = ""
        if external_mentor_info:
            for mentor in external_mentor_info.split("&"):
                external_mentor_str += (
                    f"{mentor} ")

        project_line = "".join(
            [
                f"## {project_name_info}\n",
                f"Description: {project_description}\n",
                # f"Repo: {repo_info}\n",
                f"One-pager: {one_pager_info}\n",
                f"Mentor: {mentor_info}\n",
                # f"Students: {student_info}\n",
                # f"TA: {ta_str}\n",
                # f"External Mentor:{external_mentor_str}\n",
            ]
        )

        all_results += f"{project_line}\n"


    return all_results


if __name__ == "__main__":
    # The creation of this should be automated
    # this is pretty lazy.
    all_quarter_info_list = [
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

    for quarter in all_quarter_info_list:
        filename = f"past/{quarter['year']}_{quarter['quarter']}_projects.md"
        with open(filename, "w") as f_handle:
            f_handle.write(f"# {quarter['quarter']} {quarter['year']} Projects\n")
            f_handle.write("""This is a list of project run during the quarter, along with their relevant details.\n""")
            f_handle.write(
                f"Pitchbook: [Link](./pitchbooks/"
                f"{quarter['year']}-{quarter['quarter'].lower()}"
                f"-pitchbook.pdf)\n"
            )
            f_handle.write(create_single_quarter_table(**quarter))
