# One Pager Grading Rubric

This document outlines the requirements for the one page deliverable for the Data Science Clinic at the University of Chicago. 

The purpose of the one pager is to summarize the work that you did over the course of the quarter in a way that is easily digestible and shareable to others who may be interested in it. This is a useful exercise to think about how you will frame this experience when talking or writing about it in professional settings.

Make sure to frame the problem and then link your contribution to that solution. In your write up you want the link between the high-level problem and your work to be obvious to the reader. The one-pager should also be interesting and informative. Images and figures which are low information, there without context or provide obvious content should be avoided.

Please, before submitting, make sure that your document follows the dos and don’ts outlined below. 

### Requirements 
* One page PDF document submitted to Canvas. **No Word docs, Google Drive links, etc.**
* 150-200 words written in the 3rd person (preferred) or 1st person plural and in past tense. (Figure Titles and axis labels do not count _unless_ descriptions are placed therein.)
* One or two interesting / exciting images or tables. 
* All images and words need to fit on a single page.
* Use the template found [here](../templates/one-pager-template.docx).

### Logistics and Timing 
A draft is due before the final submission. Both submission dates and times can be found on Canvas. After your draft is submitted, you will receive feedback from your mentor on specific improvements that need to be made.

Mentors will provide feedback and grading on the draft. However final grades will be applied by the data science clinic staff and faculty.

There is a short example write-up at the end of this document to give you a sense of the expectations of the level of formality and detail we are expecting.

### Grading 
You will receive a separate grade for the draft and the final version. Each team member will receive the same grade. You will be graded on the following factors:
* Content:
    * Is the document well-written, free of grammar errors and demonstrating a high level of effort and polish?
    * Is the problem well-specified?
    * Is the document written at the correct level of sophistication? 
* Style:
    * Is the writing well-organized and easy to read? 
    * Do the images and tables provide context and make the document better?
    * Are all images and tables readable?

Draft documents should demonstrate a significant level of both effort and polish. All requirements should be satisfied, and the document should be complete. There should be no placeholder images / tables / graphs. Everything should be in its final state.

<u>Draft Document (30 Points)</u>
* 20 Points: Content
* 10 Points: Style

<u>Final Document (50 Points)</u>
* 20 Points: Content
* 10 Points: Style
* 20 Points: Updates, changes and corrections based on feedback

### Dos and Don'ts
* Grammar and organization are incredibly important.
* Do NOT put your name on the doc. We will know who wrote it from the canvas submission information.
* It should be written as a single narrative. There shouldn’t be sections or headers.
* The document should look professional. While we do not expect you and your team to be design or graphics wizards, we do expect you to apply some rudimentary level of formatting and design.
* The document needs to be easy to read. If you need help with this one place to start is the [Hemingway app](https://hemingwayapp.com/) which presents a measure of complexity for each sentence. It isn't perfect, but a great place to start if you are not sure. 
* Avoid mentioning specific quarters (e.g. "Last quarter the team did ...."). The purpose of this one-pager is to create a stand alone document and additional context on _when_ something was completed is less important than focusing on what your team did this quarter.
* Figures should be interesting and useful. Low information figures, such as heat maps/other plots with limited variance, figures that demonstrate a well-known correlation ("As the figure shows, high-wealth counties have longer life spans"), or unexplained exploratory data analysis will be penalized.
* Things that should be in the one-pager:
    * Description of the problem, suitable for a lay person to understand (e.g., think explaining the problem to a family member or friend who is not in data science).
    * An explanation of your team’s contribution to solving the problem. 
    * Results and impact, but keep in mind that both need to be framed to be understood by someone who is not a data science expert.
    * Interesting charts / plots or images that help explain either the impact or the results.
    * Plot axes should be labeled and readable. This includes making them size appropriate.
    * All figures need to be explained.
* Things that should _not_ be in the one-pager:
    * Logistics of the project (“The team met 3 times a week”)
    * Thanking the partners.
    * Proper Names: NO names of students, external or faculty mentors (the exception is if you are working for a specific lab, in which case you can mention the name of the PI associated with the lab).
    * Explanation of techniques (“OLS is…”) or mentioning of tools (“Using Python...”)
    * Industry-specific terms that a non-expert wouldn’t know.
    * Tables with more than a few numbers. 

### Late Policy
Assignments submitted after the due date will receive a grade of zero.

### Grader Notes

When grading the draft one pager, keep in mind that this is not an academic one pager or something that would be sent to a conference.

The intended audience for this is much more general and serves two purposes:

1.	This should force the students to communicate their work in a way commensurate with a job-interview, talking with their family, etc. Many students struggle with stating their work in a non-microfocused way (e.g. “I wrote python functions that took in variables that did this transformation”). 
2.	These documents are how we publicize the clinic. Donors, potential partners, grants and assessment activities all rely on these. These audiences do not need more than a high-level explanation of the problem and how the student’s work fits in.

Because of this we try to make the style as uniform as possible and the writing to be professional, but informal and not filled with jargon.

When grading the draft presentation, please make sure that the requirements below are followed explicitly and aggressively knock points off for failing to fulfill them. In terms of grading standards, generally speaking we expect that most of the submissions will fall within a band 23-28 points (out of the 30 possible), with occasional really good ones hitting higher marks.

Assuming that a student group follows nearly all the requirements and the Do’s and Don’t below, there are no significant grammar or formatting issues and the writing only needs slight improvement, the grade would be about a 27/30.

### Example 

The following is an example of the level of writing we are expecting. Note that the below is less than 200 words and is only the text. For the one pager we would expect two or three interesting images as well as the use of DSI Letterhead.

| Example Write-up | 
| --- | 
| <p>American Family Insurance is a Fortune 500 private insurance company based in the Midwest. As part of their risk assessment activities, they asked the University of Chicago’s Data Science clinic to develop a model which classifies a house’s architectural style based on an image. This is important to AmFam since the architectural style has a significant impact on the costs of reconstruction in the case of an insurance claim.<br><br>The team developed multiple deep learning models to classify the images but ran into a problem with unbalanced data. Specifically, there were architectural styles that didn’t have enough data to build an accurate classifier.  The team decided to leverage state of the art generative models to create fake images that could be used to train the main classifier.<br><br>While the quality of these generated images requires improvement for use as artificial data, this initiative laid the groundwork for reducing the time and resources required for data balancing. At the end of the quarter, the precision of our classifiers was stable across models but varied widely from 14% to 83% across architectural styles. Future work could include improving the quality of generated images to increase the precision across different styles.  </p>| 