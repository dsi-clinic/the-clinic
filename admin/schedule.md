---
title: "Clinic Administrative Schedule"
---

# Clinic Administrative Schedule

The purpose of this document is to centralize resources and create a timeline of administrative tasks involved in running the clinic.

## Resources
- [Application admin link](https://docs.google.com/forms/d/1OAgTju72wNeLYeNbp3xsqxgAGqARuYvTwdYcFrTALus/edit) Best Practice: re-use this form, clearing out the historical responses and changing the date and project names.

## Weekly Calendar

### Week -6
- Verify location of classes and room reservations. We have been doing this in the new building (Room 105) so make sure that is reserved. Also contact building managers to make sure that next quarter is ready to go.
- Create a registration link for the information session via [Zoom](https://uchicago.zoom.us/meeting#/upcoming) website.
- Update the github readme with the Zoom registration information.
- Create a Matching Spreadsheet if one is not created for tracking everything.
- Share the information session registration link with this [list of people](https://docs.google.com/spreadsheets/d/1w_XWoo1csw0A916N6rif86VoGKuOdS3f5U7s59Ym8Yk/edit#gid=0). You can find an email template [here](email_templates.md#registration-initial-outreach).
- Share [TA job description](TA_job_description.md) with appropriate list including DSI Operations team (Kayleigh) to post on website.
- Figure out needed number of TAs (a TA works on two projects) and start interviewing/reviewing applications.
- Ask TAs about continuing into next quarter (if applicable).
- Update the web site to have a link to the information session so that people can register. 
- For Mentors: reach out to Amanda Kube Jotte re:preceptors and Maria Fernandez re:Postdocs. For the postdocs, make sure to get _specific_ information from Maria about who is and isn't paid to do additional work for the DSI. Many of the postdocs around the DSI are paid from external parties which means they do not receive funding contingent on doing the clinic.

### Week -5
Everything below depends upon having a list of projects.
- Create Pitchbook using this [template](https://docs.google.com/document/d/1AINocE0DzRl-1ykH7DF3kfhMMo2u0SQC/edit)
- Upload a PDF of the pitchbook to Google Drive. Change the permissions of the file to allow anyone to view it.
- Update the website so that the pitchbook is linked to the main page.
- Insert the project names into section 3 of the application. The Clinic application can be found in the shared google drive under DSIClinic/admin/"forms/surveys"/Application. Tip: Create one version of the survey question and then replicate it rather than trying to re-enter the names each time. Do _not_ open the survey until after the information session.
- Create tasks for each project, making sure that there are clear instructions on:
    - Where to download / get data (if required)
    - Initial (first week or two) of tasks for the students to complete while the project ramps up. Usually a few EDA tasks, a paper or two, or if there is a dashboard to be built, becoming familiar with the technologies that will be used.

### Week -4
Before the information session:
- Update the Info Session Presentation, which can be found [in this folder](https://drive.google.com/drive/folders/1hPbbp9HTE1DwTkWRc_BMfEkbNoqXElFi). Things to update: dates and projects. 
- On the clinic website, create an "Apply Now" link pointing to the application.
- Turn on the application. Go to the Responses tab and switch the "accepting responses" toggle. 

During the information session:
- Record the session
- Record the number of _registrations_ in the [Clinic Census](https://docs.google.com/spreadsheets/d/1cjh8Nii2IoAxG8nynYUlc9nOkVl3kGgWw2pihY98J6Q/edit#gid=0).

After the information session:
- Upload the recorded Zoom video to this [Box folder](https://uchicago.app.box.com/folder/178277527504?s=35irwnktfazm8sjpdz82z8x6ssnimpcy)
- Add a link to the zoom recording to the clinic webpage.

### Week -3
Applications close on Friday of this week. After the deadline:
- Turn off the toggle in the application to stop accepting responses.
- Remove the "Apply Now" link from the website. Change to something along the lines of "The application for this quarter is closed, please continue to check here about upcoming quarters."

### Week -2
- Clinic Director/Faculty of record should open up the registration button on my.uchicago.edu. Verify that undergrads can enroll with _electronic consent_ for all courses. You need to turn on consent!
- Walk through of Ryerson Annex to verify that all technology works as expected.
- Review applications and match students to projects.
    - Quickly review all resumes before doing any matches. Students tend to lie about (a) graduation date, (b) program and (c) how much CS they actually have. A quick skim of the resume can confirm these.
    - Matching is done via the code in the [clinic automation repository](https://github.com/dsi-clinic/clinic-automation). You can use claude to do it (there is a pretty good AGENTS.md file) in the matching directory. 
    - Before sending out matches verify that all undergrads who are actually 4th years are matched. Generally we let in all 3rd years too, but read resumes to make sure they are actually 3rd years.
- Notify matched students by Friday of this week.
- Have them confirm their participation using a google form, such as [this one](https://docs.google.com/forms/d/1UBVASrhzVyA0c0sm9f0rrE90Xe6U0C51ZhLJstN2SWo/edit).
- Send mass rejection email to students that did not match. Leave a _few_ to fill in holes if they arise. The hit rate on filling things in tends to be small.
- Reach out to TAs about TA training session in the next week. There is a presentation in the presentations folder. NOTE: Last year we started using AI to grade the final technical submissions rather than TA, so this may need to be changed.

### Week -1
- Mark Week -6 on the calendar for the upcoming quarter.
- Once students have confirmed, send them an email inviting them to register. You will need to send multiple emails telling students they will lose their spots when they fail to confirm / register.
- Because we have consent request required you will need to admit each student to the clinic individually through the poorly made my.uchicago.edu interface. The instructor of record will receive emails with each consent request. 
- Make sure that the Canvas page is set up. To do this use the code in the [clinic automation repository](https://github.com/dsi-clinic/clinic-automation). 
    - Add all TAs and Mentors to Canvas.
    - We only use a single canvas page (the one for Data 27100), make sure that all students are in that canvas page.
- Add Org Report and Computer Set up Assignment to Canvas with correct dates and times.
The following tasks depend upon having a list of confirmed students and projects:
- Create Slack channels. Add students, mentors, and TAs.
- Create GitHub repositories. Add students, mentors, and TAs
- Send the DSI cluster admin a list of CNET user IDs and associated projects to grant them access to the cluster.
- Slack message for Mentors & TAs:
```
Notes for next week:
- Class is TuTh from 5-6:30. You do not need to attend. It would be nice if you were available on slack during the tuesday 5-6:30. We do intros and start scheduling then.
- Each of you has been given access to a repository (students will be added next week). In that repository is a list of "initial tasks". This is what the students should work on before they meet their mentors.
- The students are required, by Friday to submit their "Org Report" which contains basic information about when they are meeting. Please assist them in finding available times. Students frequently misrepresent their availability. If you are having any problems scheduling or need me to stomp around please don't hesitate to ask.
- You should also all be connected to the external mentor via email. Please work with them (and the students) on scheduling a time to meet during week 2. Try to have everyone attend, but if it isn't possible do your best.
```
- Send Slack, Email and Canvas Notifications to all students, telling them the date, time and location of the first week of the course.

### Week 1
- Get NDAs signed by students and TAs (if required)
- Set up badge access for the clinic rooms by sending a list of registered student names, emails, and ChicagoID numbers to DSI operations.
- Create when2meet links and put them in the project Slack channels
- Notify the cluster groups that will need to complete step 6 of the computer setup (SSH/Cluster)
- After org reports have been submitted, set up Canvas using these <!-- markdown-link-check-disable -->[instructions](https://github.com/dsi-clinic/clinic-automation)<!-- markdown-link-check-enable-->.
- Send an email connecting all mentors to the external partner introducing them. 

Monday student message:
```
@here Welcome to the Clinic. A few quick notes:
- Today's class from 5-6:20 in XXX is a quick introduction to the clinic, first week logistics, and a chance to meet your team.
- You should all have received an invite to the github repo. Please accept this invitation.
- You should also have received an invitation to Canvas. Make sure you can access the page.
- The org report is due Friday at 5pm. This needs to be submitted via Canvas. Note that you will need to collect the information from the org report Friday at 5pm and make sure all Monday sessions have rooms. You can ignore assigning the rooms for groups which do not have monday meetings till the following week.
- All information, syllabus, grading rubrics, etc. can be found here: https://github.com/dsi-clinic/the-clinic
```

Monday TA/Mentor message:
```
@here Welcome to week 1! A few notes:
- Class is Tuesday and Thursday from 5-6:30pm in XXX. You do not need to attend in person. It would be nice if you were available on Slack during the Tuesday session. We do introductions and start scheduling then.
- On Thursday, students will be required to verify the set up of their computer during the lecture time. TAs: If you do not have a conflict, it would be great if some of you could attend.
- On Friday, the students are required to submit their "Org Report" which contains basic information about when they are meeting. Please assist them in finding available times. If you are having any problems scheduling or need us to help mediate, please don't hesitate to ask.
- You should all be connected to the external mentor via email. Please work with them (and the students) on scheduling a time to meet during week 2. Try to have everyone attend, but if it isn't possible do your best.
```

Wednesday student message:
```
@here Tomorrow we will be checking installation of needed software for the clinic. If you are returning to the clinic from last quarter you do not have to attend. The link below has necessary set up information. Please come with the steps 1-6 and 8 from the doc completed. This project [WILL/WILL NOT] be using the cluster.

We will be doing checks during tomorrow's session. The way the check works is you show us your computer and do the verification step listed for each in the document. Note that your mentor may change the required software depending on the project. https://github.com/dsi-clinic/the-clinic/blob/main/tutorials/clinic-computer-setup.md
```

### Week 2
- Assign rooms for each group's meetings in Skedda
- Send out room assignments to each project

Monday Slack message:
```
@here Some notes for week #2:
1. All room assignments will go out today.
2. You do not need to attend any TA sessions before the first meeting.
```

Room notification message:
```
@here Your room assignments are below. All rooms are located in the Ryerson Annex which is located north of the main Ryerson building. The Annex can be accessed through a set of double doors on the first floor of Ryerson.
```

Mentors-TA Slack Message:
```
@here Welcome to week 2! A few notes:
- Rooms have been assigned for TA and mentor sessions.
- All assignments have been created in Canvas with relevant due dates.
- You should be in contact (and hopefully meeting) with your external mentor this week.
- Students are required to submit their planning document this week after meeting with you.
- Please make sure to follow the best practices outlined in in the "How to run a mentor meeting" and "Mentor Expectations" docs linked below.
- There is quite a bit of documentation in the TA and Mentor Section of the GitHub repo. If you have any questions, please let us know.
https://github.com/dsi-clinic/the-clinic/blob/main/mentor-ta/index.md

```

### Week 3
- Turn on the [peer review form](https://docs.google.com/forms/d/1Ls_YnQQ72J83WqE-7XPMPbC6TtrpXJcdArA0wmdSIOA/edit). 
  - Notify students via Canvas that the peer review is available.
  - Note that in Week 3 you will need to set this up for the specific project list. 
- Ping each mentor/TA combination asking them (1) if they have connected with the external mentor and (2) Have they met with the students and are there any issues.

### Week 4 
- Turn off the peer review
- This is also WEEK -6!!! Start the process for the next quarter.

### Week 5

- Email re:Getting Rooms for next quarter for first week + mid quarter presentations in the new building.
- Reach out, again, to TAs and Mentors about status.
- Monday message to all groups doing the mid quarter presentation

```
@here Quick reminder that next week is the mid quarter presentations! The date of your presentation can be found on canvas. A template, grading rubric and more information can be found on our github. Please read the rubric. https://github.com/dsi-clinic/the-clinic
```

- Also notify the TA and Mentor Channel:

```
Hey everyone -- next week is the mid-quarter presentation (Tuesday).

These are short lightning talks by the students. A few notes: Mentors and TAs are not on the hook for grading anything for this. However you may receive questions. You should refer students to the best practices and rubric online.

If you can impart one thing to the students is that focus and interpretability are the keys here. A short presentation that covers the core tensions/results/goals of the project in a language that a non-expert can understand is an "A". A presentation that goes to the limit of 5 minutes and tries to covers too much = bad grade.

Simplify, simplify, simplify.
```

### Week 6
- Turn on the [peer review form](https://docs.google.com/forms/d/1Ls_YnQQ72J83WqE-7XPMPbC6TtrpXJcdArA0wmdSIOA/edit). 
    - Notify students via Canvas & Slack that the peer review is available
	- For this time, you can keep the same form as week 3, just change the output location. To do this click on "Response" on the form, enter the hamburger menu and then "Select Destination for responses"

### Week 7
- Turn off the peer review

Wednesday message:
```
All – Part of the grade of the clinic is a technical assessment of your code. You can find more information in the links below, including a grading rubric. If you want to receive full credit your code needs to follow the conventions outlined in the rubric.

As you head into the last few weeks of the quarter, please make sure that you add time to apply the changes expected.
Grading Rubric: https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md
Coding standards documentation: https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md
```

### Week 8
- Remind students of upcoming deadlines and technical evaluation
- Remind TAs/Mentors of their responsibilities for final deliverables. Update all dates and times below, verifying that they match canvas.

Student message:
```
@here As this is 8th week, you should start focusing on closing the current quarter and getting ready for the final deliverables. You can find all information about the final deliverables on Canvas and the Clinic Github repo. Additional information is provided as a preview below, but refer to those locations for full details including the time that submissions are due.
There are four final deliverables:
	(1) Video
		a. Draft #1 due 5/21
		b. Draft #2 due 5/23
		c. Final Video due 5/29
	(2) One-pager
		a. Draft due 5/23
		b. Final due 5/29
	(3) Email to external partner due 5/29
	(4) Technical Submission due 5/28

Rubrics can be found here:

https://clinic.ds.uchicago.edu/students/#finals-week-deliverables

Please read the rubrics carefully in order to receive full credit.
```

After the application opens:
```
@here The application for Winter 2025 is now open. If you are enrolled in DATA 271 and will be taking DATA 272 next quarter, you must reapply to get into our matching system. The deadline for submission is Dec 1 at 11:59pm. 

Apply here: https://dsi-clinic.github.io/the-clinic/#application-information
```

Mentor/TA message:
```
@here Just a reminder about your responsibilities as we head into the final weeks of the quarter.
Mentors: Provide written feedback on student drafts within 24 hours of submission. For examples, please see the rubrics below. Students will submit drafts at the following times:
1. Dec 3rd @1pm (video draft 1)
2. 5/23 at 1pm (video draft 2 and one-pager)

Video rubric: https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-video.md
One-pager rubric: https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/one-pager.md
Technical rubric: https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md
```

### Week 9

- There are lots of material due this week. Make sure to remind everyone their responsibilities.

### Week 10
- Turn on the [peer review form](https://docs.google.com/forms/d/1Ls_YnQQ72J83WqE-7XPMPbC6TtrpXJcdArA0wmdSIOA/edit). Notify students via Canvas that the peer review is available.
- Sometimes, especially in the fall, you'll get grading questions. I've responded with the following.

```
@here I've been getting several questions about grades and how they work in the clinic. Here are a few important things to keep in mind:

Grading Process:

- The course is curved. Different mentors have different grading standards, but before final grades are finalized, a normalization process occurs to ensure standards are applied consistently across all sections.

- Final grades are assigned by me personally to maintain fairness and consistency across different mentors.

Draft Submissions:

- Please make sure to carefully address the feedback provided by your mentors on drafts. While some mentors may be stricter than others in their grading, all the feedback I've reviewed has been professional and constructive.

Final Deliverables:

- Client deliverables carry the most weight in your final grade.
We place significant value on professionalism, improvement over the quarter, and effort throughout the project.

**Finally** -- it is finals week and everyone is a bit stressed. Make sure to work through the feedback, be professional in your dealings with others. I have seen really strong work all quarter and the grades will reflect that.

```

### Week 11
- Turn off the peer review.
- Remove all students and TAs from GitHub and Slack (as appropriate).
- Update the web page to add the one-pagers and other information for the projects history
- Update the Clinic Census and Statistic doc [link here](https://docs.google.com/spreadsheets/d/1cjh8Nii2IoAxG8nynYUlc9nOkVl3kGgWw2pihY98J6Q/edit?gid=279684155#gid=279684155)
- Go through the last quarter and review the above instructions. What is missing? What needs to be added? Create a to do list of items.
- Are there any templates that you want to add (email/slack)
- Remember, this is fun, lol.
