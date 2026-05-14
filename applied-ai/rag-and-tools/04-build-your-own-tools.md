---
title: "Build Your Own Tools"
order: 4
---

## The assignment

Extend the advising bot's toolset. Starting from your copy of the notebook, add **at least two new tools** to the tool-using bot. One of them must read data, and one must write data (an `INSERT` or `UPDATE`). Make sure the bot still works end to end after your changes.

You're welcome to base your work directly on the existing tool functions in cell 17. Copy the pattern, swap the SQL, and add an entry to the `tools` list and the `tool_functions` dispatch map.

## Required tools

### A grades tool (read)

The current bot can't answer questions like "What grade did Mei get in Machine Learning?" because the `grades` table is never queried. Add a tool that fixes that.

Decide what your tool should return. A natural shape is one row per grade, joined to the student name and the course name so the model has useful labels:

```sql
SELECT students.name AS student, courses.name AS course, grades.grade
FROM grades
JOIN students ON grades.student_id = students.id
JOIN courses ON grades.course_id = courses.id;
```

Wrap that query in a Python function (look at `get_courses_tool` for the shape), register it in the `tools` list with a clear description, and add it to `tool_functions`. Then run the bot and ask it a grades question. The model should pick your tool and answer correctly.

### A write tool (insert or update)

Pick one of these (or invent your own that fits the schema):

- **`enroll_student_in_course`** that adds a new row to the `grades` table for a given student and course, with an initial grade like `"In Progress"`.
- **`update_grade`** that changes the letter grade for a student in a course they're already enrolled in.
- **`add_instructor`** that inserts a new row into the `instructors` table.
- **`change_advisor`** that updates a student's `advisor_id` to point at a different instructor.

A write tool needs parameters, because the model has to tell your code **what** to write. That's a small upgrade to your tool definition. The Groq docs have the full JSON schema for parameters. The Groq tool-use page is your reference:

[Groq Tool Use docs](https://console.groq.com/docs/tool-use)

A parameter schema for `update_grade` would look something like this:

```python
{
    "type": "function",
    "function": {
        "name": "update_grade",
        "description": "Update a student's letter grade for a specific course.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_name": {"type": "string", "description": "Full name of the student."},
                "course_name": {"type": "string", "description": "Full name of the course."},
                "new_grade": {"type": "string", "description": "The new letter grade, like 'A' or 'B'."}
            },
            "required": ["student_name", "course_name", "new_grade"]
        }
    }
}
```

When the model decides to call this tool, the `tool_calls[0].function.arguments` field comes back as a JSON string. You'll need to `json.loads(...)` it, pass those values to your Python function, and have that function run the right SQL.

Your write tool should return a confirmation dict that the final-response step can summarize, something like:

```python
{"data": [("Mei Chen", "Machine Learning", "A")], "columns": ["student", "course", "new_grade"]}
```

That gives the model something useful to say after the action runs ("Updated Mei Chen's grade in Machine Learning to A.").

## Make the workflow handle parameters

The version of `generate_tool_call` in cell 19 only reads `tool_calls[0].function.name`. It ignores arguments. You'll need to also pull `tool_calls[0].function.arguments` and pass it through to `execute_tool`, then through to your tool function. A clean way to do that is to refactor the three step functions to pass a `tool_args` dict alongside `tool_name`.

If your reader tool doesn't take parameters and your writer tool does, both should still work through the same pipeline.

## Test it

Once your two new tools are in place, run through these prompts and confirm each one picks the right tool and answers correctly:

- "What grade did Mei get in Machine Learning?" (grades read)
- "Update Mei's grade in Machine Learning to A." (your write tool)
- "What grade did Mei get in Machine Learning?" (grades read, should now reflect the change)
- "What courses does Tina teach?" (the existing `get_courses` tool, still working)

Print the chosen tool name and the tool result on every call, the same way cell 19 does. That makes it obvious whether the model is routing correctly.

## Requirements summary

Your submitted notebook must:

1. Include the **existing three tools** plus **at least two new ones**, where one new tool reads from the database and one writes (`INSERT` or `UPDATE`).
2. Use a **parameterized tool definition** for your write tool, with a JSON schema for arguments.
3. Print the chosen tool and tool result for every call so a reader can see the model's choices.
4. Run end to end without errors when a reader pastes their own API key into the key cell.
5. Have a **short markdown cell at the top** (3-5 sentences) that says what your bot does, what tools you added, and one thing you found surprising while testing it.

## Submit

Once your bot works:

1. In Colab, click **Share** in the top right.
2. Under "General access," change it to **"Anyone with the link"** and set the role to **Viewer**.
3. Copy the link.

**Both partners submit individually on Canvas** with the shared notebook link.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=RAG+and+Tools" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
