---
title: "RAG: Just Add the Data"
order: 2
---

This page walks through cells 1 through 12 in the notebook. Cells 1 through 8 are the same imports, formatting helpers, `generate_response`, and `add_*_message` helpers you used in the last unit. Skim them and run each one. The interesting stuff starts at cell 10.

## A fake backend: the in-memory database

Cell 10 sets up a tiny **SQLite** database that lives entirely in RAM. SQLite is a real SQL database that runs inside your Python process. The `:memory:` argument tells it to skip the file system entirely and just keep the data in memory for the life of the notebook.

```python
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
```

The rest of the cell creates four tables and seeds them with sample rows:

- **instructors** with names, emails, departments, and offices
- **courses** with a name, description, quarter, and `instructor_id` foreign key
- **students** with an `advisor_id` that points back at an instructor
- **grades** that connect a student to a course with a letter grade

The whole thing exists so the rest of the notebook has something realistic to query. It's a stand-in for whatever real backend you'd connect to in a production app (Postgres, MySQL, your school's actual SIS, a vendor API). The pattern you're about to learn works the same way against any of them. Swap the SQL connection, keep the rest.

Run the cell. There is no output. The data is now sitting in memory waiting to be queried.

## The retrieval function

Cell 12 contains the RAG bot. It has two pieces. The first is a function that pulls data out of the database:

```python
def retrieve_courses():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT courses.name, description, instructors.name, quarter FROM courses
        JOIN instructors ON courses.instructor_id = instructors.id;
    """)
    results = cursor.fetchall()
    return results, [description[0] for description in cursor.description]
```

It runs one SQL query that joins courses against instructors so each row carries both the course details and the instructor's name. It returns the rows and the column names. Nothing about this is AI specific. It is the same data-access code you would write for any web app.

This is the **R** in RAG. Your code retrieves something before the model gets involved.

## The advising bot

The second piece is where the model shows up:

```python
def advising_bot(user_query):
    courses, column_names = retrieve_courses()

    if not courses:
        context = "No courses found."
    else:
        context = "Here are the courses:\n"
        for course in courses:
            course_details = []
            for i in range(len(column_names)):
                course_details.append(f"{column_names[i]}: {course[i]}")
            context += ", ".join(course_details) + "\n"

    prompt = f"""
    You are an academic advising assistant. Answer the user's query using the following course information:

    {context}

    User Query: {user_query}
    """

    messages = [{"role": "user", "content": prompt}]
    response = generate_response(messages, model="llama-3.1-8b-instant", max_tokens=300, temperature=0.2)
    return response
```

Four things are happening in that function. Walk through them in order.

**Fetch.** Call `retrieve_courses()` and get back rows and column names.

**Format.** Turn the rows into plain text the model can read. The loop produces lines like `name: Machine Learning, description: ..., instructor: Susan Uland, quarter: Winter`. There is nothing magical about this format. You could use a CSV, a JSON dump, a bullet list, or a table. What matters is that the model can read it.

**Stuff it into the prompt.** Use an f-string to drop the formatted context into a prompt template along with the user's question. Notice the **shape** of the prompt: role assignment first ("You are an academic advising assistant"), then the data the model is allowed to use, then the user's actual question. That order helps the model understand the data is reference material.

**Generate.** Send the whole thing to the model with `temperature=0.2`.

## Try it

Run cell 12. When the input box pops up, try each of these:

- `What courses are offered in Winter?`
- `What courses are offered by Susan Uland?`
- `Which course covers the design of operating systems?`

The bot answers all three correctly because the data it needs is sitting right there in the prompt. The model is just reading the rows you handed it and summarizing them in plain English.

> **With your partner:** Why does `temperature=0.2` make more sense here than the `0.7` to `0.9` you used in the chain example last unit? What would happen if you bumped it up?

<details>
<summary>Reveal answer</summary>

The advising bot's job is to read a list of facts and report on them accurately. That is a focused, deterministic task. Low temperature keeps the model close to the actual data instead of dressing the answer up with extra detail it might invent. Higher temperature would make the model more likely to add flourishes or speculate when the question doesn't have a clean answer in the data. Same kind of mismatch you'd get from a creative writing model trying to do tax prep.

</details>

## The limits of "just dump everything"

This pattern is fast to build and works surprisingly well, but the cracks show up quickly.

**It is wasteful.** Every call sends every course, even when the user only asks about one. With four tables, you'd be sending all of them on every call.

**It doesn't scale.** Five courses is fine. Five thousand will blow past the context window from page 1 of the last unit. Once your data is bigger than the prompt, this pattern stops working.

**It is one-shaped.** The retrieval function fetches courses. Always. If the user asks about students or instructors, the bot has no idea, because the prompt only contains course data.

**It can't take actions.** The bot can describe the data, but it can't update a record, send an email, or trigger a workflow. Read-only by design.

Real RAG systems get around the first two limits by doing smart retrieval. They use embeddings, keyword search, or filtering rules to pull only the rows that are relevant to the question. That is a topic for a later unit. The third and fourth limits (one-shaped, read-only) are what the next page solves.
