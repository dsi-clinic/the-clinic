# Welcome to the Data Science Clinic at the University of Chicago

This repository contains information and documentation regarding the Data Science Clinic at the University of Chicago.

# Table of Contents

<!-- do not change TOC, generated from script -->
<!-- `npx markdown-toc -i README.md` --> 
<!-- tried automating but ran afoul of branch protections.>

<!-- toc -->

- [Welcome to the Data Science Clinic at the University of Chicago](#welcome-to-the-data-science-clinic-at-the-university-of-chicago)
- [Table of Contents](#table-of-contents)
- [Logistics](#logistics)
  - [Application Information](#application-information)
  - [Meeting times / Simultaneous Enrollment](#meeting-times--simultaneous-enrollment)
  - [In-person requirements](#in-person-requirements)
  - [People](#people)
  - [Weekly Calendar](#weekly-calendar)
- [Documents](#documents)
  - [Syllabus](#syllabus)
  - [Progress and Planning Docs](#progress-and-planning-docs)
  - [First Week Org Report](#first-week-org-report)
  - [Mid-quarter presentation](#mid-quarter-presentation)
- [Finals Week Deliverables](#finals-week-deliverables)
- [Additional Tutorials and Assistance](#additional-tutorials-and-assistance)
- [Previous Projects](#previous-projects)
- [Coding Standards](#coding-standards)
- [TA and Mentor Information](#ta-and-mentor-information)
- [FAQ](#faq)
    - [I am doing an internship/research experience/project in data science, can I waive out of the clinic?](#i-am-doing-an-internshipresearch-experienceproject-in-data-science-can-i-waive-out-of-the-clinic)
    - [As a Data Science Major, can I take the clinic over two non-consecutive quarters?](#as-a-data-science-major-can-i-take-the-clinic-over-two-non-consecutive-quarters)

<!-- tocstop -->

# Logistics 

This section contains information on important logistics and contact information for the clinic.

## Application Information

Students must apply to take the Data Science Clinic. An information session is held a few weeks before the start of each quarter which describes the application process as well as the available projects.

For more information on the application process including dates for upcoming information sessions, please go [here](https://sites.google.com/uchicago.edu/dsclinic).

## Meeting times / Simultaneous Enrollment

During the first week of clinic students are expected to meet at the time specified in the schedule, commonly TuTh 5-6:20, for orientation and introduction activities. 

During the first week, each project will identify meeting times specific to their project (two TA sessions and one mentor sessions). These meeting times are dependent on the TA, Mentor(s) and students schedule. These meeting times will be used for the rest of the quarter.

During the sixth week of the quarter there are a set of mid-quarter presentations. These presentations are not required for all team members -- though failing to support your team is a bad signal. The mid-quarter presentations are in-person and in the room scheduled for the class.

Since outside the times listed above we do not meet during the scheduled time it is not uncommon for students to enroll in a class with some overlap. If you do have a course which has some overlap or conflict with the scheduled time you may need to fill out a "Simultaneous Enrollment" form with your advisor. If this is the case please send an email to the clinic director stating that you will be doing this.

## In-person requirements

We expect all TA sessions and mentor meetings (unless the mentor chooses otherwise) to be done _in-person_ during normal business hours. If your schedule makes it difficult to be on the Hyde Park Campus during normal business hours, such as being in a program based down town or another commitment which takes you off campus for significant time then we recommend _not_ taking this course.

## People

The Data Science Clinic is administered by [Nick Ross](https://nickross.site) and [Tim Hannifan](https://github.com/timhannifan). Questions about the clinic should be addressed to them either over slack or via their UChicago email addresses.  

## Weekly Calendar

You can find a weekly calendar [here](./syllabus/weekly-plan.md). 

# Documents 

This section contains links to many of the important documents used in the clinic. 

## Syllabus

The Syllabus, including all course expectations can be found [here](./syllabus/syllabus.md).

## Progress and Planning Docs

Each week you are required to upload a planning and progress doc (due dates are specific to your project and can be found on Canvas). 

The planning doc can be found [here](./templates/planning-doc.md) in markdown format. There is a rubric [here](./rubrics/planning-doc-rubric.md).

The progress doc can be found [here](./templates/progress-doc.md) in markdown format. There is a rubric [here](./rubrics/progress-doc-rubric.md).

Note that in the `templates` directory you can also find MS-word versions of the two documents.

## First Week Org Report

The first week org report can also be found in the `templates` directory in a MS-WORD format. There is a markdown version [here](./templates/week-1-org-report.md). Grading for this is simple: if it is turned in on time and complete it receives full credit, otherwise zero.

## Mid-quarter presentation

In week 6 of the clinic students will be required to complete a short mid-quarter presentation. There is a template for the presentation in the directory `templates`. 

If you want to receive an "A" on this assignment, _make sure to follow the [rubric](./rubrics/mid-quarter-presentation-rubric.md) precisely_.

# Finals Week Deliverables

As this is a projects based course most of the work is designed around a set of final deliverables. There are four set of requirements, each with their own rubric that you can find in the table below. These are to be completed during the last week of the quarter and finals week.


| Item | Requirement Information | Submission information and Rubric | 
| --- | --- | --- |
| Code | You are required to turn in the code that you wrote in a well-kept repository and conforms to the [coding standards](./coding-standards/coding-standards.md) of the data science clinic. | For the final code submission you will need to fill out the worksheet [here](./templates/final-technical-submission.md) and submit that worksheet in Canvas. | 
| One pager | There is a one page project description that needs to be completed as part of the final submission. Note that you will be required to provide both a draft and final version. | Grading rubrics can be found [here](./rubrics/one-pager.md) and a template can be found [here](./templates/one-pager-template.docx). Both versions are to be submitted via Canvas. |
| Final Video | A short, recorded, video presentation is also required to be created. This includes two drafts and a final version. | Grading will be done according to the [rubric](./rubrics/final-video.md) and submission will be completed via Canvas. |
| Partner Email | Each team should designate one person to send a final email to the external partner with the video, one-pager and link to the code they developed. | Information on requirements for this email can be found [here](./rubrics/final-email.md). | 


# Additional Tutorials and Assistance

We keep a list of frequently asked questions and answers as well as "How-to"'s for specific technologies in this repo:

* [How to set up your computer](./tutorials/clinic-computer-setup.md)
* [SSH to Github and the Cluster](./tutorials/ssh_github_cluster.md)
* [Slurm](./tutorials/slurm.md)
* [Using Submitit on the cluster](./tutorials/submit-it.md)
* [Writing well-documented code](./coding-standards/code-example.md)
* [Docker Common Questions](./tutorials/Docker.md)
* [Understanding File Systems](./tutorials/filepaths.md)
* [Using GDAL](./tutorials/geopandas-dockerfile.md)
* [Using Podman on the Cluster](./tutorials/podman.md)
* [Speaking Code](./tutorials/speaking-code.md)
* [WSL FAQ](./tutorials/WSL.md)
* [Web scraping](./tutorials/web_scraping.md)
* [X11 on the Cluster](./tutorials/X11.md)
* [How to talk about the clinic on your resume and in interviews](./tutorials/resume-interviews.md)
* [Removing Sensitive Data from Git](./tutorials/remove_data_git.md)

Finally, The University of Chicago's Computer Science Department has an in-depth list of related resources that you can find [here](https://uchicago-cs.github.io/student-resource-guide/). 

If you need help using Unix, docker or any of the tools used in the clinic this is an invaluable resource.

# Previous Projects

We keep information on all of our previous projects [here](./projects/projects.md).

# Coding Standards

You can find information on Data Science Clinic Coding Standards and expectations [here](./coding-standards/coding-standards.md).

# TA and Mentor Information

In addition to the information above, this section contains best practices for mentors and TAs. 

* [Mentor Intro Presentation](./presentations/2024-Autumn-Clinic-Mentor-Info.pptx)
* [General Mentor Expectations](./mentor-ta/mentor-expectations.md)
* [Weekly Calendar](./syllabus/weekly-plan.md)
* [TA Expectations](./mentor-ta/ta-expectations.md)
* [How to run a Mentor Meeting](./mentor-ta/how-to-run-a-meeting.md)
* [How to run a TA Session](./mentor-ta/how-to-run-a-ta-session.md)

# FAQ

In this section you can find a list of frequently asked questions about the clinic.

### I am doing an internship/research experience/project in data science, can I waive out of the clinic? 

Unfortunately these classes are required for the major and there is no method of substituting them. Internships, Research experiences and projects come in all shapes and sizes and it isn't possible to guarantee any specific learning outcome, supervision or experience with them.

### As a Data Science Major, can I take the clinic over two non-consecutive quarters? 

It is strongly recommended to take the clinic in consecutive quarters. If you take it over non-consecutive quarters you will likely end up on two different projects which will significantly diminish the experience. At the individual level the most important learning experience occurs after you have internalized the domain and background of the project which frequently occurs in the second quarter.