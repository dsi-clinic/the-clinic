import pandas as pd
from IPython.display import display
import pulp


def generate_data(file_name, technical_project_list, priority_lc_map):
    application_df = pd.read_excel(file_name, sheet_name="Applications")

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
    application_df["Priority"] = (application_df["Priority"]
                                  .map(priority_lc_map)
                                  )

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
        (
            f"Dropping {sum(drop_list_no_comp == True)} students because they "
            f"do not have a computer and not required"
        )
    )
    application_df = application_df.loc[~drop_list_no_comp, :]

    # Filter applicants based on taking next quarter
    next_quarter_column_name = (
        "Are you planning to take the clinic next " "quarter?"
    )
    no_continue = application_df[next_quarter_column_name].str.lower() == "no"
    drop_list_no_cont = no_continue & not_high_priority
    print(
        (
            f"Dropping {sum(drop_list_no_cont == True)} students because they"
            " are not high priority and not continue"
        )
    )
    application_df = application_df.loc[~drop_list_no_cont, :]

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
        df_long["Ranking"].str.extract("(\d)").astype(int) # noqa W605
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

    missnamed_projs = [
        x for x in technical_project_list if x not in all_projects
    ]

    assert len(missnamed_projs) == 0, "Technical Projects not mapped correctly"

    # Extract student characteristics: priority, experience, and email
    exp_students = application_df.loc[
        (application_df["Strong CS"].str.lower() == "yes"), "Email Address"
    ].tolist()

    student_characteristics = application_df.loc[
        :, ["Email Address", "Priority"]
    ].copy()

    student_characteristics["Experienced"] = application_df[
        "Email Address"
    ].isin(exp_students)

    result_dict = {
        "ranking": df_merged,
        "student_characteristics": student_characteristics,
        "technical_projects": technical_project_list,
        "all_project_list": all_projects,
    }

    return result_dict


def print_project_summary(assignment_df, all_projects):
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

        project_summary.loc[
            current_project_rows, "Number"
        ] = n_students_in_project

        project_summary.loc[
            current_project_rows, "High Priority"
        ] = n_high_priority

        project_summary.loc[
            current_project_rows, "High-Med Priority"
        ] = n_med_high_priority

        project_summary.loc[
            current_project_rows, "Med Priority"
        ] = n_med_priority

        project_summary.loc[
            current_project_rows, "Low Priority"
        ] = n_low_priority

        project_summary.loc[
            current_project_rows, "Experienced"
        ] = n_exp_students

        project_summary.loc[current_project_rows, "Rankings"] = rankings_str

        project_summary.loc[
            current_project_rows, "Average Ranking"
        ] = avg_ranking

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
    """
    ranking, student_characteristics, technical_projects are all as described
    from generate data

    * priority weights describes how to weight the different priorities.
    Priorities are 1,2,3,4 (or however many) with lower being more important
    * the algorithim currently assigns everyone a project who is high priority
    * med-high should be 2nd year masters students ad no one below that really
    gets assigned to a project.

    max_students_dict: If a project needs a number less than 4 on a project
    use this to override that number.

    preassigned_students: this hard codes specific students onto projects. This
    will be used for 2nd quarter students.

    number_of_project_to_run: If you want to only do X projects
    use this override

    drop_projects: A list of projects to not place students in.

    verbose: When set to true it outputs additional info from the fitting algo.

    """

    # Determine which projects to run
    all_projects = ranking["Project Name"].unique()
    assert (
        len([x for x in drop_projects if x not in all_projects]) == 0
    ), "A project to drop is not in the project list"

    projects = [x for x in all_projects if x not in drop_projects]
    technical_projects = [
        x for x in technical_projects if x not in drop_projects
    ]
    assert (
        len([x for x in technical_projects if x not in projects]) == 0
    ), "A technical project is not in the list"

    if number_of_projects_to_run is not None:
        assert number_of_projects_to_run <= len(
            projects
        ), "Not enough projects to run"

    # Update Rankings based on projects to drop
    # The logic is to set the
    ranking.loc[
        ~(ranking.loc[:, "Project Name"].isin(projects)), "Ranking"
    ] = 100

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
        [
            (i, j)
            for j in projects
            for i in students
            if i not in preassigned_students.get(j, [])
        ],
        cat="Binary",
    )

    # Create binary decision variables to track if a project is running
    # (i.e., has any students)
    y = pulp.LpVariable.dicts("y", [j for j in projects], cat="Binary")

    # Objective: Minimize ranking cost with weighted priorities
    problem += pulp.lpSum(
        ranking.loc[
            (ranking["Email Address"] == i) & (ranking["Project Name"] == j),
            "Ranking",
        ].values[0]
        * priority_weights[
            int(
                student_characteristics.loc[
                    student_characteristics["Email Address"] == i, "Priority"
                ].values[0]
                - 1
            )
        ]
        * x[(i, j)]
        for j in projects
        for i in students
        if i not in preassigned_students.get(j, [])
    )

    # Add constraints to prevent students from being assigned to projects with
    # a ranking of 100
    for j in projects:
        for i in students:
            student_ranking = ranking.loc[
                (ranking["Email Address"] == i)
                & (ranking["Project Name"] == j),
                "Ranking",
            ].values[0]
            if student_ranking == 100 or student_ranking > 3:
                problem += x[(i, j)] == 0

    # Add constraints for forced assignments
    for student, project in preassigned_students.items():
        # Ensure the student is assigned to the specified project
        problem += x[(student, project)] == 1

        # Prevent the student from being assigned to any other project
        for other_project in projects:
            if other_project != project:
                problem += x[(student, other_project)] == 0

    # Constraints: Priority 1 students must be assigned to a project
    priority_1_students = student_characteristics.loc[
        student_characteristics["Priority"] == 1, "Email Address"
    ]
    for i in priority_1_students:
        problem += pulp.lpSum(x[(i, j)] for j in projects) == 1

    # Maximum number of students per project
    for j in projects:
        preassigned_count = len(preassigned_students.get(j, []))
        max_allowed = (
            max_students_dict.get(j, 4) - preassigned_count
        )  # Adjust max based on pre-assigned students
        problem += (
            pulp.lpSum(
                x[(i, j)]
                for i in students
                if i not in preassigned_students.get(j, [])
            )
            == max_allowed
        )

    # Link y[j] to student assignments: If any student is assigned to project
    # j, y[j] must be 1
    for j in projects:
        problem += (
            pulp.lpSum(
                x[(i, j)]
                for i in students
                if i not in preassigned_students.get(j, [])
            )
            <= 4 * y[j]
        )  # If y[j] = 0, no students can be assigned

    # Conditional minimum number of students:
    # If a project is running (y[j] = 1), it must have at least 3 students
    for j in projects:
        preassigned_count = len(preassigned_students.get(j, []))
        problem += (
            pulp.lpSum(
                x[(i, j)]
                for i in students
                if i not in preassigned_students.get(j, [])
            )
            + preassigned_count
            >= 3 * y[j]
        )

    # Technical projects must have at least 2 experienced students
    # (including preassigned)
    for j in technical_projects:
        preassigned_exp_count = sum(
            1
            for i in preassigned_students.get(j, [])
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
                if i not in preassigned_students.get(j, [])
            )
            + preassigned_exp_count
            >= 2
        )

    # Ensure that the exact number of projects are running:
    if number_of_projects_to_run is not None:
        problem += (
            pulp.lpSum(y[j] for j in projects) == number_of_projects_to_run
        )

    # Each student can be assigned to at most one project (if not pre-assigned)
    for i in students:
        if not any(i in preassigned_students.get(j, []) for j in projects):
            problem += pulp.lpSum(x[(i, j)] for j in projects) <= 1

    # Solve the problem
    # These parameters are all gu
    problem.solve(
        pulp.GUROBI_CMD(
            msg=verbose,
            timeLimit=None,
            options=[
                ("MIPgap", 0.0001),  # Tighten the optimality gap
                ("MIPFocus", 2),  # Focus on proving optimality
                (
                    "ImproveStartTime",
                    60,
                ),  # Spend time improving the current solution
                ("Cuts", 2),  # Increase the aggressiveness of cuts
                ("Threads", 4),  # Use 4 threads
                ("Heuristics", 0.01),  # Reduce heuristic focus
                ("Symmetry", 2),  # Increase symmetry detection
            ],
        )
    )

    print(pulp.value(problem.objective))

    # Create DataFrame for assignments
    assignment_df = pd.DataFrame(
        {"Email Address": students, "Project Assigned": None, "Ranking": None}
    )

    # Update assignments for non-preassigned students
    for i in students:
        for j in projects:
            if pulp.value(x[(i, j)]) == 1:
                student_ranking = ranking.loc[
                    (ranking["Email Address"] == i)
                    & (ranking["Project Name"] == j),
                    "Ranking",
                ].values[0]
                assignment_df.loc[
                    assignment_df["Email Address"] == i, "Project Assigned"
                ] = j
                assignment_df.loc[
                    assignment_df["Email Address"] == i, "Ranking"
                ] = student_ranking

    # Handle pre-assigned students
    for project, assigned_students in preassigned_students.items():
        for student in assigned_students:
            assignment_df.loc[
                assignment_df["Email Address"] == student, "Project Assigned"
            ] = project
            assignment_df.loc[
                assignment_df["Email Address"] == student, "Ranking"
            ] = 0  # Pre-assigned students have no ranking cost

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
