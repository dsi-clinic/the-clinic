"""Utilities for matching."""

import pandas as pd
import pulp
from IPython.display import display


def generate_data(application_df, technical_project_list):
    """Generate processed data for student-project matching from application data.

    This function processes the application dataframe, extracts relevant information,
    and prepares the data for the student-project matching algorithm.

    Parameters:
    application_df (pandas.DataFrame): A dataframe containing student application data.
        Must include columns: 'Email Address', 'Project 1' through 'Project 5',
        'Priority', 'Strong CS', and a column asking about computer access.
    technical_project_list (list): A list of projects that are considered technical.

    Returns:
    dict: A dictionary containing the following keys:
        - 'ranking': A dataframe with student rankings for each project.
        - 'student_characteristics': A dataframe with student priorities and experience.
        - 'technical_projects': The list of technical projects.
        - 'all_project_list': A list of all available projects.

    Raises:
    AssertionError: If 'Email Address' column contains duplicates, if priority values
        are invalid, or if technical projects are not correctly mapped.
    """
    assert application_df[
        "Email Address"
    ].is_unique, "The 'Email Address' column contains duplicate values."

    # List of all available projects
    all_projects = list(
        pd.concat(
            [
                application_df["Project 1"],
                application_df["Project 2"],
                application_df["Project 3"],
                application_df["Project 4"],
                application_df["Project 5"],
            ]
        ).unique()
    )

    # Clean Priority definition, turning it from 1 (has to be included) to 5
    # Ensure the priority column is in lowercase
    application_df["Priority"] = application_df["Priority"].str.lower()

    # Replace the priority values based on the mapping
    priority_lc_map = {"high": 1, "med-high": 2, "med": 3, "low": 4}
    application_df["Priority"] = application_df["Priority"].map(priority_lc_map)

    # Assert that all values in the 'Priority' column are valid integers
    assert (
        application_df["Priority"].notna().all()
    ), "All rows must have a valid, integer priority."

    # Filter applicants based on having computer access
    has_computer_column_name = (
        "Many of the projects require having access"
        " to a computer with administrator privileges."
        " Do you have access to a computer?"
    )

    no_computer = application_df[has_computer_column_name].str.lower() == "no"
    not_high_priority = ~(application_df["Priority"] == 1)
    drop_list_no_comp = no_computer & not_high_priority
    print(
        f"Dropping {sum(drop_list_no_comp)} students because they "
        f"do not have a computer and not required"
    )
    application_df = application_df.loc[~drop_list_no_comp, :]

    print(f"Total Students available for matching: {application_df.shape[0]}")

    # Reshaping the data to long format
    df_long = pd.melt(
        application_df,
        id_vars=["Email Address"],
        value_vars=[
            "Project 1",
            "Project 2",
            "Project 3",
            "Project 4",
            "Project 5",
        ],
        var_name="Ranking",
        value_name="Project Name",
    )

    # Extract the ranking (1 to 5) from the "Ranking" column
    df_long["Ranking"] = (
        df_long["Ranking"].str.extract("(\d)").astype(int)  # noqa W605
    )

    # Merge all project assignments with rankings
    list_for_df = [
        (student, project)
        for student in application_df["Email Address"]
        for project in all_projects
    ]

    df_all_projects = pd.DataFrame(
        list_for_df, columns=["Email Address", "Project Name"]
    )

    # Merge rankings with all projects for each student
    df_merged = pd.merge(
        df_all_projects,
        df_long,
        on=["Email Address", "Project Name"],
        how="left",
    )
    df_merged["Ranking"] = df_merged["Ranking"].fillna(100)
    df_merged = df_merged.sort_values(by=["Email Address", "Ranking"])

    missnamed_projs = [x for x in technical_project_list if x not in all_projects]

    assert len(missnamed_projs) == 0, "Technical Projects not mapped correctly"

    # Extract student characteristics: priority, experience, and email
    exp_students = application_df.loc[
        (application_df["Strong CS"].str.lower() == "yes"), "Email Address"
    ].tolist()

    student_characteristics = application_df.loc[
        :, ["Email Address", "Priority"]
    ].copy()

    student_characteristics["Experienced"] = application_df["Email Address"].isin(
        exp_students
    )

    result_dict = {
        "ranking": df_merged,
        "student_characteristics": student_characteristics,
        "technical_projects": technical_project_list,
        "all_project_list": all_projects,
    }

    return result_dict


def print_project_summary(assignment_df, all_projects):
    """Generate and print a summary of project assignments.

    This function creates a summary table for all projects, calculates various statistics
    for each project based on student assignments, and displays the results.

    Parameters:
    assignment_df (pandas.DataFrame): A DataFrame containing student assignment information.
        It should have columns for 'Project Assigned', 'Priority', 'Experienced', and 'Ranking'.
    all_projects (list): A list of all project names to be included in the summary.

    Returns:
    None. The function prints the summary information to the console and displays
    a DataFrame with project statistics.
    """
    # Create summary table for all projects, initializing with zero values
    project_summary = pd.DataFrame(
        {
            "Project Name": all_projects,
            "Number": [0] * len(all_projects),
            "High Priority": [0] * len(all_projects),
            "High-Med Priority": [0] * len(all_projects),
            "Med Priority": [0] * len(all_projects),
            "Low Priority": [0] * len(all_projects),
            "Experienced": [0] * len(all_projects),
            "Rankings": [""] * len(all_projects),
            "Average Ranking": [0.0] * len(all_projects),
        }
    )

    # Total number of students
    total_students = assignment_df.shape[0]

    # Number of matched students (assigned to a project)
    matched_students = assignment_df["Project Assigned"].notna().sum()

    # Iterate through the assignment_df and calculate the summary statistics
    # for each project

    for project in all_projects:
        assigned_students = assignment_df.loc[
            (assignment_df["Project Assigned"] == project), :
        ]

        n_students_in_project = assigned_students.shape[0]
        n_high_priority = (assigned_students["Priority"] == 1).sum()
        n_med_high_priority = (assigned_students["Priority"] == 2).sum()
        n_med_priority = (assigned_students["Priority"] == 3).sum()
        n_low_priority = (assigned_students["Priority"] == 4).sum()
        n_exp_students = assigned_students["Experienced"].sum()
        rank_list = sorted(assigned_students["Ranking"].astype(int).tolist())
        rankings_str = ",".join(map(str, rank_list))
        avg_ranking = (
            round(assigned_students["Ranking"].mean(), 2)
            if n_students_in_project > 0
            else 0
        )

        current_project_rows = project_summary["Project Name"] == project

        project_summary.loc[current_project_rows, "Number"] = n_students_in_project

        project_summary.loc[current_project_rows, "High Priority"] = n_high_priority

        project_summary.loc[current_project_rows, "High-Med Priority"] = (
            n_med_high_priority
        )

        project_summary.loc[current_project_rows, "Med Priority"] = n_med_priority

        project_summary.loc[current_project_rows, "Low Priority"] = n_low_priority

        project_summary.loc[current_project_rows, "Experienced"] = n_exp_students

        project_summary.loc[current_project_rows, "Rankings"] = rankings_str

        project_summary.loc[current_project_rows, "Average Ranking"] = avg_ranking

    # Sort projects so that projects with no students are at the bottom
    project_summary = project_summary.sort_values(
        by=["Number", "Average Ranking"], ascending=[False, True]
    ).reset_index(drop=True)

    # Print the summary table
    print(
        f"\nStudent Summary: {matched_students} of {total_students} students"
        " were matched to a project."
    )

    # Print the summary table
    print("\nProject Summary:")

    display(project_summary)


def student_assignment(
    ranking,
    student_characteristics,
    technical_projects,
    priority_weights,
    max_students_dict=None,
    preassigned_students=None,
    number_of_projects_to_run=None,
    drop_projects=[],
    verbose=False,
):
    """Assign students to projects based on rankings and various constraints.

    This function uses linear programming to optimize student-project assignments
    while considering student preferences, project requirements, and other constraints.

    Parameters:
    ranking (pandas.DataFrame): DataFrame containing student rankings for each project.
    student_characteristics (pandas.DataFrame): DataFrame with student information including priority and experience.
    technical_projects (list): List of projects considered technical.
    priority_weights (list): Weights for different priority levels.
    max_students_dict (dict, optional): Maximum number of students per project. Defaults to None.
    preassigned_students (dict, optional): Dictionary of pre-assigned students to projects. Defaults to None.
    number_of_projects_to_run (int, optional): Exact number of projects to run. Defaults to None.
    drop_projects (list, optional): List of projects to exclude from assignment. Defaults to empty list.
    verbose (bool, optional): If True, print additional information during execution. Defaults to False.

    Returns:
    pandas.DataFrame: DataFrame containing the final student-project assignments,
                      including student email, priority, experience, assigned project, and ranking.
    """
    # Determine which projects to run
    all_projects = ranking["Project Name"].unique()
    assert (
        len([x for x in drop_projects if x not in all_projects]) == 0
    ), "A project to drop is not in the project list"

    projects = [x for x in all_projects if x not in drop_projects]
    technical_projects = [x for x in technical_projects if x not in drop_projects]
    assert (
        len([x for x in technical_projects if x not in projects]) == 0
    ), "A technical project is not in the list"

    if number_of_projects_to_run is not None:
        assert number_of_projects_to_run <= len(projects), "Not enough projects to run"

    # Update Rankings based on projects to drop
    # The logic is to set the
    ranking.loc[~(ranking.loc[:, "Project Name"].isin(projects)), "Ranking"] = 100

    # Define the problem
    problem = pulp.LpProblem("Student_Project_Assignment", pulp.LpMinimize)

    # Extract data from inputs
    students = ranking["Email Address"].unique()

    # Set default max students per project (4 unless otherwise specified)
    if max_students_dict is None:
        max_students_dict = {}

    # Fill in default max of 4 for any project not explicitly in
    # max_students_dict
    max_students_dict = {
        project: max_students_dict.get(project, 4) for project in projects
    }

    # Handle pre-assigned (immutable) students
    if preassigned_students is None:
        preassigned_students = {}
        preassigned_projects = {}
    else:
        preassigned_projects = {}
        for student, project in preassigned_students.items():
            if project not in preassigned_projects:
                preassigned_projects[project] = []
            preassigned_projects[project].append(student)

    # Verify preassigned students are in the student characteristics:
    preassigned_student_email_list = list(preassigned_students.keys())

    assert (
        len(preassigned_student_email_list)
        == student_characteristics.loc[:, "Email Address"]
        .isin(preassigned_student_email_list)
        .sum()
    ), "Preassigned students not in student characteristics"

    # Create binary decision variables only for students not preassigned
    x = pulp.LpVariable.dicts(
        "x",
        [(i, j) for j in projects for i in students if i not in preassigned_students],
        cat="Binary",
    )

    # Create binary decision variables to track if a project is running
    # (i.e., has any students)
    y = pulp.LpVariable.dicts("y", list(projects), cat="Binary")

    # Objective: Minimize ranking cost with weighted priorities
    problem += pulp.lpSum(
        ranking.loc[
            (ranking["Email Address"] == i) & (ranking["Project Name"] == j),
            "Ranking",
        ].to_numpy()[0]
        * priority_weights[
            int(
                student_characteristics.loc[
                    student_characteristics["Email Address"] == i, "Priority"
                ].to_numpy()[0]
                - 1
            )
        ]
        * x[(i, j)]
        for j in projects
        for i in students
        if i not in preassigned_students
    )

    # Constraint: Prevent students from being assigned to projects with
    # a max ranking
    MAX_ALLOWED_RANK = 4
    for j in projects:
        for i in students:
            if i not in preassigned_students:
                student_ranking = ranking.loc[
                    (ranking["Email Address"] == i) & (ranking["Project Name"] == j),
                    "Ranking",
                ].to_numpy()[0]
                if student_ranking > MAX_ALLOWED_RANK:
                    problem += x[(i, j)] == 0

    # Constraints: Priority 1 students must be assigned to a project
    priority_1_students = student_characteristics.loc[
        student_characteristics["Priority"] == 1, "Email Address"
    ]
    for i in priority_1_students:
        if i not in preassigned_students:
            problem += pulp.lpSum(x[(i, j)] for j in projects) == 1

    # Maximum number of students per project
    for j in projects:
        preassigned_count = len(preassigned_projects.get(j, []))

        max_allowed = (
            max_students_dict.get(j, 4) - preassigned_count
        )  # Adjust max based on pre-assigned students

        problem += (
            pulp.lpSum(x[(i, j)] for i in students if i not in preassigned_students)
            == max_allowed
        )

    # Link y[j] to student assignments: If any student is assigned to project
    # j, y[j] must be 1
    for j in projects:
        problem += (
            pulp.lpSum(x[(i, j)] for i in students if i not in preassigned_students)
            <= 4 * y[j]
        )  # If y[j] = 0, no students can be assigned

    # Conditional minimum number of students:
    # If a project is running (y[j] = 1), it must have at least 3 students
    for j in projects:
        preassigned_count = len(preassigned_projects.get(j, []))
        problem += (
            pulp.lpSum(x[(i, j)] for i in students if i not in preassigned_students)
            + preassigned_count
            >= 3 * y[j]
        )

    # Technical projects must have at least 1 experienced students
    # (including preassigned)
    keep_technical_constraint = True
    if keep_technical_constraint:
        for j in technical_projects:
            preassigned_exp_count = sum(
                1
                for i in preassigned_projects.get(j, [])
                if i
                in student_characteristics.loc[
                    (student_characteristics["Experienced"]), "Email Address"
                ]
            )
            problem += (
                pulp.lpSum(
                    x[(i, j)]
                    for i in student_characteristics.loc[
                        student_characteristics["Experienced"], "Email Address"
                    ]
                    if i not in preassigned_students
                )
                + preassigned_exp_count
                >= 1
            )

    # Ensure that the exact number of projects are running:
    if number_of_projects_to_run is not None:
        problem += pulp.lpSum(y[j] for j in projects) == number_of_projects_to_run

    # Each student can be assigned to at most one project (if not pre-assigned)
    for i in students:
        if i not in preassigned_students:
            problem += pulp.lpSum(x[(i, j)] for j in projects) <= 1

    # Solve the problem using the default solver
    problem.solve()

    # Create DataFrame for assignments
    assignment_df = pd.DataFrame(
        {"Email Address": students, "Project Assigned": None, "Ranking": None}
    )

    # Update assignments for non-preassigned students
    for i in students:
        if i not in preassigned_students:
            for j in projects:
                if pulp.value(x[(i, j)]) == 1:
                    student_ranking = ranking.loc[
                        (ranking["Email Address"] == i)
                        & (ranking["Project Name"] == j),
                        "Ranking",
                    ].to_numpy()[0]
                    assignment_df.loc[
                        assignment_df["Email Address"] == i, "Project Assigned"
                    ] = j
                    assignment_df.loc[
                        assignment_df["Email Address"] == i, "Ranking"
                    ] = student_ranking

    # Handle pre-assigned students
    for project, assigned_students in preassigned_projects.items():
        for student in assigned_students:
            assignment_df.loc[
                assignment_df["Email Address"] == student, "Project Assigned"
            ] = project
            assignment_df.loc[assignment_df["Email Address"] == student, "Ranking"] = (
                0  # Pre-assigned students have no ranking cost
            )

    # Merge priority and experience info
    assignment_df = assignment_df.merge(
        student_characteristics, on="Email Address", how="left"
    )

    # Reorder columns
    assignment_df = assignment_df[
        [
            "Email Address",
            "Priority",
            "Experienced",
            "Project Assigned",
            "Ranking",
        ]
    ]

    return assignment_df


def process_applications(
    file_location, deprioritized_students, prioritized_students, projects_to_drop
):
    """Process student applications for project assignments.

    This function reads an Excel file containing student applications,
    cleans the data, generates priority and CS strength columns,
    and creates forced assignments for returning students.

    Parameters:
    file_location (str): The file path of the Excel spreadsheet containing
                         student application data.
    deprioritized_students (list): A list of student email addresses to be
                                   deprioritized in the assignment process.
    prioritized_students (list): A list of student email addresses to be
                                   prioritized in the assignment process.
    projects_to_drop (list): A list of projects that will not run.

    Returns:
    tuple: A tuple containing two elements:
        - application_df (pandas.DataFrame): Processed application data with
          additional columns for priority and CS strength.
        - forced_assignments (dict): A dictionary of forced project assignments
          for returning students, with student email as key and project name
          as value.
    """
    application_df = pd.read_excel(
        file_location, sheet_name="Application Before Editing"
    )

    # Clean up project columns
    prev_proj_col = "If you are currently enrolled or have taken the clinic in a previous quarter, on which project did you work?"

    def strip_chars(df):
        cols = [
            "Project 1",
            "Project 2",
            "Project 3",
            "Project 4",
            "Project 5",
            prev_proj_col,
        ]
        for col in cols:
            df[col] = df[col].str.replace("*", "")
        return df

    application_df = strip_chars(application_df)

    # Generate Priority column
    def generate_priorities(df, deprioritized_students, prioritized_students):
        # Default everyone to low priority
        df["Priority"] = "low"

        def adj_priority(filter, priority):
            df.loc[filter, "Priority"] = priority

        # Adjust priority for third year data science majors
        adj_priority(
            (df["Current Degree Program"] == "Undergrad: 3rd year")
            & (
                df["Academic Program / Concentration"].str.contains(
                    r"data science", na=False, case=False
                )
            ),
            "med",
        )

        # Adjust priority for general fourth years (non-DS majors)
        adj_priority((df["Current Degree Program"] == "Undergrad: 4th year"), "med")

        # Adjust priority for second year masters students
        adj_priority((df["Current Degree Program"] == "MA or MS 2nd year"), "med-high")

        # Adjust priority for fourth year data science majors
        adj_priority(
            (df["Current Degree Program"] == "Undergrad: 4th year")
            & (
                df["Academic Program / Concentration"].str.contains(
                    r"data science", na=False, case=False
                )
            ),
            "high",
        )

        # Adjust priority for fifth year data science majors
        adj_priority(
            (df["Current Degree Program"] == "Undergrad: 5th year")
            & (
                df["Academic Program / Concentration"].str.contains(
                    r"data science", na=False, case=False
                )
            ),
            "high",
        )

        # Adjust priority for prioritized students
        for email in prioritized_students:
            adj_priority(df["Email Address"] == email, "high")

        # Adjust priority for deprioritized students
        for email in deprioritized_students:
            adj_priority(df["Email Address"] == email, "low")

        # Adjust priority for specific programs
        adj_priority(
            (df["Academic Program / Concentration"] == "MA Public Policy (MPP)"), "low"
        )
        adj_priority(
            (
                df["Academic Program / Concentration"]
                == "MA Computational Social Science (MACSS)"
            ),
            "med-high",
        )
        adj_priority(
            (
                df["Academic Program / Concentration"]
                == "MS Computational Analysis and Public Policy (MSCAPP)"
            ),
            "med-high",
        )

        return df

    application_df = generate_priorities(
        application_df, deprioritized_students, prioritized_students
    )

    # Generate Strong CS column
    cscol1 = 'If you have taken an introduction to computer science / "Computer Science 1" course (such as CMSC 141, 151 or 161), please list that course here. DATA courses do not count.'
    cscol2 = 'If you have taken a course that would be considered the equivalent of "Computer Science 2" (such as CMSC 142, 152 or 162), please list that course here. DATA courses do not count.'

    def generate_cs_column(df):
        df["Strong CS"] = "No"

        def adjust_col(filter, column, newvalue):
            df.loc[filter, column] = newvalue

        # Adjust CS strength
        adjust_col((df[cscol1].notna() & df[cscol2].notna()), "Strong CS", "Yes")
        return df

    application_df = generate_cs_column(application_df)

    # Generate forced assignments for returning students
    prev_col = "Are you currently enrolled in the Data Science Clinic or have you taken the clinic in a previous quarter?"

    returning_students = application_df[application_df[prev_col] == "Yes"][
        ["Email Address", prev_proj_col]
    ].to_numpy()

    forced_assingments = {}
    for student, project in returning_students:
        if project not in projects_to_drop:
            forced_assingments[student] = project

    # Remove deprioritized students from forced assignments
    for student in deprioritized_students:
        if student in forced_assingments:
            del forced_assingments[student]

    return application_df, forced_assingments


def generate_roster(application_df, assignment_df):
    """Generate a roster of students assigned to projects by merging application and assignment data.

    This function filters out unassigned students, merges application and assignment data,
    selects relevant columns, renames them for clarity, sorts the data, and reorders columns
    to create a final roster.

    Parameters:
    application_df (pandas.DataFrame): DataFrame containing student application information.
        Must include columns for student details such as name, GitHub username, email, etc.
    assignment_df (pandas.DataFrame): DataFrame containing project assignments for students.
        Must include columns 'Email Address' and 'Project Assigned'.

    Returns:
    pandas.DataFrame: A DataFrame representing the final roster, containing columns for
        Project, Name, GitHub, Email, Chicago ID, Degree Program, and Concentration.
        The DataFrame is sorted by Project and Name, with the index reset.
    """
    # Filter out students not assigned to a project
    assignment_df = assignment_df[assignment_df["Project Assigned"].notna()]

    # Merge application and assignment data
    merged_df = assignment_df.merge(application_df, on="Email Address", how="left")

    # Select columns
    merged_df = merged_df[
        [
            "Project Assigned",
            "Full Name",
            "GitHub Username",
            "Email Address",
            "ChicagoID from the back of your ID card (8 numbers + letter). This is NOT the same as your student ID number.",
            "Current Degree Program",
            "Academic Program / Concentration",
            "Ranking",
        ]
    ]

    # Create Returning column
    merged_df["Returning"] = 0
    merged_df.loc[merged_df["Ranking"] == 0, "Returning"] = 1
    merged_df = merged_df.drop(columns="Ranking")

    # Rename columns for better readability
    merged_df.columns = [
        "Project",
        "Name",
        "GitHub",
        "Email",
        "Chicago ID",
        "Degree Program",
        "Concentration",
        "Returning",
    ]

    # Sort by project and name
    merged_df = merged_df.sort_values(
        by=["Project", "Name"],
        ascending=[True, True],
    )

    merged_df = merged_df.reset_index(drop=True)

    return merged_df


def generate_rejections(assignment_df):
    """Generate a list of students who were not assigned to a project.

    This function filters out students assigned to a project, selects relevant columns,
    and renames them for clarity.

    Parameters:
    assignment_df (pandas.DataFrame): DataFrame containing project assignments for students.
        Must include columns 'Email Address' and 'Project Assigned'.

    Returns:
    pandas.DataFrame: A DataFrame representing the list of students who were not assigned to a project,
        containing columns for Email Address.
    """
    # Filter out students assigned to a project
    rejections_df = assignment_df[assignment_df["Project Assigned"].isna()]

    # Select columns
    rejections_df = rejections_df[["Email Address"]]

    # Rename columns for better readability
    rejections_df.columns = ["Email"]

    # Drop index
    rejections_df = rejections_df.reset_index(drop=True)

    return rejections_df
