Here are a few things that successful Clinic teams tend to do.

## Communication Cadence

Successful teams use the Slack channel regularly. This includes asking questions, giving each other updates on work progress ("Heads up that I just finished the function that \<does something\>. I still need to handle some edge cases, but it should be ready to start integrating into the pipeline."), and sharing resources relevant to the project.

For less successful teams, the channel tends to be very quiet.

## Start Each Week's Tasks Early

In most classes, your weekly assignments consists of reading, problem sets, or writing papers. Given the workload of some classes, it's easy to fall into a pattern of starting an assignment the day before a deadline, working until just before the deadline, then submitting what you have.

While stressful, this can _kind of_ work for most classes!

This is an _extremely bad_ strategy for Clinic, though. For Clinic, you will often have a loosely defined task that no one has actually done before. Because of this, you will probably encounter all kinds of unexpected errors. The data may be incorrect, the task you were assigned may not actually make sense with the existing code base, the DSI Cluster may be down, there may be some idiosyncratic issue with your computer and other resources that you need to use, etc.

Because of this, you should at least _start_ your tasks as early as possible so that, when you run into these blockers, you can ask for help quickly. Mentors really, really dislike getting messages at 10:30pm the night before a team meeting with students realizing that they can't build the conda environment they need for this week's task.

Additionally, since the tasks for Clinic often have some ambiguity, starting to think about them as early as possible will give you ample time to come up with different ideas on how to approach your work.

## Project Manager

Usually, one student steps up to function as the project manager for the group. This includes making sure that weekly reports are submitted on time (and ideally not minutes before the deadline), making sure that everyone on the team understands their tasks, and communicating between people working on different pieces of the project.

## Run Each Other's Code

One of the most challenging things in working in a group on a software project is understanding other people's code. Both understanding others' code and writing code that other people can understand are skills that improve with practice.

Good teams will run each other's code, ask questions, and improve the code base collaboratively so it is robust and easy to understand.

## Debugging Strategies

There are two failure modes for debugging:
1. Immediately asking for help without putting forth a reasonable effort to resolve an issue yourself
1. Never asking for help and getting stuck on a technical issue (especially one that is not the point of the project) for a full week

If you encounter a confusing error or a bug, here's a good sequence of steps to try.
1. Google the exact error message you receive
	- There will usually be several Stack Overflow threads with other users encountering a similar issue. You may need to read a few of them to find a good solution.
	- Avoid copying and pasting solutions without understanding what you are pasting. Sometimes users suggest things that work but have unintended consequences.
1. Read the documentation for the tool you are using
	- Most mature software tools have documentation that you can find by searching "\<tool\> documentation". Find the section related to what you are using and make sure you understand what the expected behavior of the tool is.
1. Ask a large language model
	- Large language models are surprisingly good at helping understand and debug code. As above, avoid copying and pasting things from language models that you don't understand.
	- If you see a solution that you don't understand from Stack Overflow or are having a hard time understanding documentation, asking a language model can be very helpful. Prompts like "Please explain this to me in a clear, intuitive mannger" can give good results.
1. Ask for help
	- Once you've tried searching, reading the documentation, and asking a language model, ask for help on Slack. Please don't wait until the next mentor session or TA session to ask for help if you are stuck! The quarters are very short and losing a whole week to a bug can really impact how you're able to accomplish.