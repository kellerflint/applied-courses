---
title: "From Chat to Real Data"
order: 1
---

By the end of the last unit you had a chatbot that could remember a conversation and chain calls together. It is missing something important though. It only knows what the model knows. Ask it about courses at your school, customers in your database, or the document your team wrote yesterday, and it has nothing to say. The model's training data ended at some date in the past, and your data was never in it to begin with.

This unit fixes that. You'll connect an LLM to a real database and let it answer questions grounded in that data. You will see two different patterns for doing it, and you will get the start of an academic advising bot that actually knows the courses, students, and instructors you give it.

## Why the model can't answer questions about your data

The model is great at language and terrible at facts that weren't in its training set. Three failure modes show up over and over once you try to use an LLM on real work:

**Knowledge cutoff.** Training data has a date. Anything that happened after that date, or that simply never made it onto the open internet, the model has no idea about. Your company's internal docs, your school's course catalog, last quarter's sales numbers, the API you shipped last week. None of it is in there.

**Private data.** Even where data exists somewhere, the model doesn't have a connection to your specific database, your customer list, or your file system. It cannot reach out and look something up on its own.

**Hallucination.** When the model doesn't know an answer, it usually does not say "I don't know." It produces something that sounds right, because that is what the prediction loop does. A confident-sounding wrong answer is the default behavior, not an edge case.

The fix in all three cases is the same. **You give the model the data, then ask the question.** The model goes from generating an answer out of thin air to summarizing or reasoning over text you handed it. That move (data first, question second) is the foundation of almost every real LLM app.

> **With your partner:** Think about a chatbot you'd actually want to build. What information would it need that the model can't possibly know on its own? Where does that information live today (a database, a Google Doc, a spreadsheet, a website)?

## Two ways to get data into the prompt

The notebook for this unit shows two patterns for handing data to a model. They sit on a spectrum.

**RAG (Retrieval-Augmented Generation).** Your code pulls relevant data out of some source, drops it into the prompt as context, and then asks the model the user's question. Your code decides what gets fetched every time. RAG is the simpler pattern and it is the right move when the same kind of context is useful for almost every question.

**Tools (also called function calling).** You describe a handful of functions to the model and let the model pick which one to call. Your code runs the chosen function, hands the result back, and the model writes the final answer. Tools are more flexible than RAG because the model can route different questions to different data sources.

Both patterns share the same underlying trick from earlier units. Whatever the model needs to know has to show up in the messages list before you ask the question. The difference is who decides what shows up.

> **With your partner:** Pick a question a hypothetical academic advising bot might get ("What courses does Susan teach?" or "Has Mei passed her data structures class?"). For each one, sketch in plain English what data the bot would need to answer. Would you want to dump all of it into every prompt, or only fetch what the question needs?

## What you'll build

The notebook sets up a small in-memory SQLite database with four tables (instructors, courses, students, grades) seeded with realistic-looking sample data. You'll build two versions of an advising bot on top of it.

1. A **RAG advising bot** that pulls every course from the database and feeds them to the model with the user's question.
2. A **tool-using advising bot** that has three functions available (`get_courses`, `get_students`, `get_instructors`), lets the model pick the right one, runs it, and uses the result to answer.

By the end of the unit you'll also extend the tool-using bot with at least one of your own tools.

## Open the notebook

Open the example notebook here: [RAG and Tools notebook (Colab)](https://colab.research.google.com/).

Just like last unit, click **File → Save a copy in Drive** so you have your own editable copy. Drop your Groq API key into the `api_key` cell. The rest of this unit walks the notebook section by section, with explanations of what each part is doing and why. Keep both the notebook and these lesson pages open as you work.

Once your copy is open and your API key is in, head to page 2 and we'll plug the model into a database.
