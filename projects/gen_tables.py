## Checklist:
## 1. Remove access to named students when going through repos

### To do:
# 1. automate 400 no-400 for has repo


# Format: Name (which matches below) and a link to _something_ either github or LinkedIn?
ALL_PEOPLE = {
    "James Turk": ["James Turk", "https://github.com/jamesturk/"],
    "Nick": ["Nick Ross", "https://www.linkedin.com/in/drdata/"],
    "Launa": ["Launa Greer", "https://github.com/LaunaG"],
    "Rahim": ["Rahim Rasool", "https://github.com/rahimrasool"],
    "David U.": [
        "David Uminsky",
        "https://www.linkedin.com/in/david-uminsky-5153b1a8/",
    ],
    "Dan N.": [
        "Dan Nicolae",
        "https://www.linkedin.com/in/dan-nicolae-221991a/",
    ],
    "Tim": ["Tim Hannifan", "https://github.com/timhannifan"],
    "Ali": ["Ali Klemencic", "https://github.com/aliklemencic"],
    "Christian": ["Christian Jordan", "https://github.com/chrjor"],
    "Anthony K": ["Anthony Kanellopoulos", "https://github.com/kanello"],
    "Kenia": ["Kenia Godinez Nogueda", "https://github.com/gnogueda"],
    "Patricia": [
        "Patricia Chiril",
        "https://www.linkedin.com/in/patricia-chiril-27062298",
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
}

# Structure: name / url/ mentor / TA / github / private repo 1/0, has_one_pager 1/0
SPRING_23_PROJECT = [
    [
        "Argonne",
        "https://www.anl.gov/",
        "Rahim",
        "Christian",
        "https://github.com/dsi-clinic/2023-clinic-Argonne",
        0,
        1,
        "[Matthew Dearing](https://www.linkedin.com/in/matthewtdearing/)",
    ],
    [
        "Blue Ocean Gear",
        "https://www.blueoceangear.com/",
        "Launa",
        None,
        "https://github.com/chicago-cdac/bog-anomaly-mapping/",
        1,
        1,
        "XX?",
    ],
    [
        "CRI-SET",
        "https://pediatrics.uchicago.edu/research/set",
        "Anna & Dan N.",
        "Anthony K",
        "https://github.com/dsi-clinic/2023-spring-clinic-set",
        1,
        1,
        "Dr. Henry David",
    ],
    [
        "DRW",
        "https://drw.com/",
        "Tim",
        None,
        "https://github.com/dsi-clinic/2023-clinic-drw",
        1,
        0,
        "Ian Adam",
    ],
    [
        "Fermi",
        "https://www.fnal.gov/",
        "Peter",
        "Ali",
        "https://github.com/dsi-clinic/2023-clinic-fermi-tag",
        1,
        1,
        "<ul><li>Michael Kirby</li><li>Meghna Bhattacharya</li></ul>",
    ],
    [
        "FRB",
        "https://www.firstrepublic.com/",
        "Nick",
        None,
        "https://github.com/dsi-clinic/2023-clinic-first-republic-bank",
        1,
        0,
        "<ul><li>Chris Csiszar</li><li>Mark Woodworth</li></ul>",
    ],
    [
        "Hawaii",
        "https://11thhourproject.org/",
        "Launa",
        "Ali",
        "https://github.com/chicago-cdac/hawaii-pesticides",
        1,
        1,
        "XXX",
    ],
    [
        "IE",
        "https://internetequity.uchicago.edu/",
        "James Turk",
        "Kenia",
        "https://github.com/chicago-cdac/broadbandequity",
        0,
        1,
        "Dr. Nicole Marwell",
    ],
    [
        "Morningstar",
        "https://www.morningstar.com/",
        "Patricia & David U.",
        "Christian",
        "https://github.com/dsi-clinic/2023-clinic-morningstar",
        1,
        0,
        "<ul><li>Josh Charney</li><li>Jazmin Melchor</li></ul>",
    ],
    [
        "Neurocritical Care",
        "https://scholar.google.com/citations?user=cs_tgvwAAAAJ&hl=en",
        "Yuetian",
        "Anthony",
        "https://github.com/dsi-clinic/2023-clinic-neurocritical-care",
        1,
        1,
        "Dr. Ali Mansour",
    ],
    [
        "Perpetual",
        "https://www.perpetualuse.org/",
        "Rahim",
        None,
        "https://github.com/dsi-clinic/2023-clinic-perpetual",
        0,
        1,
        "Ellie Moss",
    ],
    [
        "Prudential",
        "https://www.prudential.com/",
        "Nick",
        "Kenia",
        None,
        1,
        0,
        "Amol Tembe",
    ],
]

SPRING_23_STUDENT = [
    ["Argonne", "Ken Kliesner", "https://github.com/kenkliesner"],
    ["Argonne", "Annabel Mendoza", "https://github.com/amendoza5025"],
    ["Argonne", "Kekun Han", "https://github.com/KekunH"],
    ["Blue Ocean Gear", "Gautam Kapoor", "https://github.com/grkapoor17"],
    ["Blue Ocean Gear", "Henry Herzog", "https://github.com/Hgherzog"],
    ["Blue Ocean Gear", "Irsa Ashraf", "https://github.com/irsa-ashraf"],
    ["Blue Ocean Gear", "Katy Barone", "https://github.com/kbarone"],
    ["CRI-SET", "Varun Mohan", "https://github.com/vmohan96"],
    ["CRI-SET", "Jun Tan", "https://github.com/JunTan2022"],
    ["CRI-SET", "Katherine Miao", "https://github.com/Katherine-Miao"],
    ["DRW", "Mahnoor Khan", "https://github.com/Mfk-han"],
    ["DRW", "Jasmeet Singh Sandhu", "https://github.com/jasmeeetSingh"],
    ["DRW", "Yulun Han", "https://github.com/YLHan97"],
    ["Fermi", "Richard Zhang", "https://github.com/chihavertz"],
    ["Fermi", "Manuel Martinez", "https://github.com/manmartgarc"],
    ["Fermi", "Mingyan Wang", "https://github.com/wmingyan"],
    ["Fermi", "Tarun Arora", "https://github.com/tarun2k"],
    ["FRB", "Guangbo Niu", "https://github.com/ngbdsb"],
    ["FRB", "Zhiyun Hu", "https://github.com/zhiyun0707"],
    ["FRB", "Yu-Hsuan Chou", "https://github.com/yhchou0904"],
    ["FRB", "Ning Tang", "https://github.com/tangn121"],
    ["Hawaii", "Ashley Hitchings", "https://github.com/ashleyhitchings"],
    ["Hawaii", "Qingyi He", "https://github.com/cindyheqy"],
    ["Hawaii", "Caleb Costa", "https://github.com/calebcosta1"],
    ["IE", "Victoria Kielb", "https://github.com/vkielb"],
    ["IE", "Chandler Hall", "https://github.com/cgwhall"],
    ["IE", "Sarah Lueling", "https://github.com/slueling"],
    ["Morningstar", "Rishabh Shastry", "https://github.com/rishabhshastry"],
    ["Morningstar", "Dhairya Karna", "https://github.com/DhairyaKarna"],
    ["Morningstar", "Max de Saint-Exupery", "https://github.com/MaxSaint01"],
    ["Neurocritical Care", "Soren Dunn", "https://github.com/sorendunn"],
    ["Neurocritical Care", "Alex Przybycin", "https://github.com/AlexPrizzy"],
    [
        "Neurocritical Care",
        "Prashant Kumar",
        "https://github.com/Prashant-Kumar700",
    ],
    ["Perpetual", "Ziyu Ren", "https://github.com/AshleyZR"],
    ["Perpetual", "Yushu Qiu", "https://github.com/yushuqiu1"],
    ["Perpetual", "Avery Schoen", "https://github.com/averyschoen"],
    ["Perpetual", "Ekansh Trivedi", "https://github.com/ekanshtrivedi"],
    ["Prudential", "Sunvid Aneja", "https://github.com/sunvidaneja"],
    ["Prudential", "Peihan Gao", "https://github.com/peihan12"],
    ["Prudential", "Sai Omkar Kandukuri", "https://github.com/S-Omkar-K"],
    ["Prudential", "Hantang Qin", "https://github.com/jenniferqinnn"],
]


SPRING_23_NAME_MAP = {
    "Argonne": "Argonne Knowledge Graph",
    "Fermi": "Fermi: Kirby Lab",
    "Hawaii": "Hawaii Pesticides",
    "IE": "Internet Equity",
    "FRB": "First Republic Bank",
}

SPRING_23_ONE_PAGER_LOCATION = "./one-pagers/2023-spring/"


def create_link_for_mentor(mentor_info):
    return f"[{mentor_info[0]}]({mentor_info[1]})"


def create_link_for_student(student_info):
    return create_link_for_mentor(student_info[1:3])


#### --- ###
name_map = SPRING_23_NAME_MAP
one_pager_location = SPRING_23_ONE_PAGER_LOCATION
student_info_list = SPRING_23_STUDENT
all_results = "\n| Project Name | Repository | One-Pager | Mentors | Students | \
    External Mentor | TA | \n | --- |  --- | --- | --- | --- | --- | --- |\n"

for project_info in SPRING_23_PROJECT:
    [
        project_link,
        project_url,
        mentor_link,
        ta_link,
        github_link,
        is_private_repo,
        has_one_pager,
        external_mentor_info,
    ] = project_info

    project_name = name_map.get(project_link, project_link)

    if is_private_repo:
        if github_link:
            repo_info = f"<!-- markdown-link-check-disable --> [Private Repo]({github_link}) <!-- markdown-link-check-enable -->"
        else:
            repo_info = "No Repository"
    else:
        repo_info = f"[DSI Repo]({github_link})"

    if has_one_pager:
        file_info = one_pager_location + project_link + '.pdf'
        one_pager_info = f"[One-Pager]({file_info.replace(' ', '%20')})"
    else:
        one_pager_info = ""

    mentor_list = [mentor.strip() for mentor in mentor_link.split("&")]

    if len(mentor_list) == 1:
        mentor_info = create_link_for_mentor(ALL_PEOPLE[mentor_list[0]])

    else:
        mentor_info = "<ul>"
        for mentor in mentor_list:
            mentor_info += (
                f"<li>{create_link_for_mentor(ALL_PEOPLE[mentor])}</li>"
            )
        mentor_info += "</ul>"

    student_info = "<ul>"
    for student in [x for x in student_info_list if x[0] == project_link]:
        student_info += f"<li>{create_link_for_student(student)}</li>"
    student_info += "</ul>"

    TA_info = ALL_PEOPLE.get(ta_link, None)
    if TA_info:
        TA_info = create_link_for_mentor(TA_info)
    else:
        TA_info = ''        

    project_line = ' | ' .join([project_name, repo_info, one_pager_info, mentor_info, student_info, external_mentor_info, TA_info])
    all_results += ' | ' + project_line + '\n'

print(all_results)
