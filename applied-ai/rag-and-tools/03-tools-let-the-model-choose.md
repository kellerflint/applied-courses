---
title: "Tools: Let the Model Choose"
order: 3
---

The RAG bot from page 2 had a fixed retrieval step. It always pulled courses, whether the user asked about courses or not. This page swaps that fixed step for one where the model itself picks which function to call. That capability is called **tool use** (some APIs call it **function calling**). It is the same idea behind the way ChatGPT can suddenly run Python or browse the web mid-conversation.

We're walking through cells 13 through 19 in the notebook.

## A small tweak to generate_response

Cell 14 redefines `generate_response` with one new argument:

```python
def generate_response(messages, tools=[], model="llama-3.1-8b-instant", max_tokens=150, temperature=0.7):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        tools=tools
    )
    response = chat_completion.choices[0].message
    return response
```

Two changes from the version you used last unit.

**It now accepts a `tools` list.** That list is where you describe the functions the model is allowed to call. We'll fill it in below.

**It returns the whole `message` object, not just `.content`.** That matters because when the model decides to call a tool, the answer comes back on `message.tool_calls`, not on `message.content`. You need access to both.

## Three real Python functions

Cell 17 defines three query functions. Each one is a regular Python function that runs a SQL query and returns a dict with rows and column names. Your code is what actually runs these functions. The model's only job is to pick which one should run.

```python
def get_courses_tool():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT courses.name, description, instructors.name AS instructor, quarter
        FROM courses
        JOIN instructors ON courses.instructor_id = instructors.id;
    """)
    results = cursor.fetchall()
    return {"data": results, "columns": [description[0] for description in cursor.description]}
```

There are two more like it: `get_students_tool` (students with their advisor names) and `get_instructors_tool` (instructor contact info). Each is a hard-coded SQL query packaged as a Python function. You'd write the same code in any web app.

## Telling the model what's available

The model has no way to see your Python source code. You hand it a JSON description of each function instead:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_courses",
            "description": "Retrieve information about courses and who teaches them.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_students",
            "description": "Retrieve information about students and who their advisors are.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_instructors",
            "description": "Retrieve information about instructors.",
        }
    }
]
```

That JSON is everything the model knows about your tools. It gets:

- A **name** to refer to the function by.
- A **description** of what the function does and what it returns. **This is the most important part.** The model picks tools by matching the user's question against these descriptions. A vague description gets you wrong tool picks. A specific one gets you right ones.

Real-world tool descriptions also list parameters with types and required-vs-optional, so the model knows how to fill them in. The notebook keeps things simple and uses parameterless tools, but the same JSON schema scales up to "send_email with `to`, `subject`, `body`" or "search_orders with `customer_id` and `date_range`."

Cell 17 also builds a dispatch map so your code can look up the real Python function from a name string:

```python
tool_functions = {
  "get_courses": get_courses_tool,
  "get_students": get_students_tool,
  "get_instructors": get_instructors_tool
}
```

That dict is the bridge between "the model said `get_courses`" and "actually run `get_courses_tool()`."

## The three-step tool workflow

Cell 19 is the whole thing wired up. It runs in three steps. Look at each one in isolation, because every tool-using LLM app you ever build follows this same shape.

### Step 1: ask the model which tool to call

```python
def generate_tool_call(user_query):
    messages = add_system_message([], "You are an academic advising assistant. Use the provided tools to retrieve relevant information based on the user's query.")
    messages = add_user_message(messages, user_query)

    response = generate_response(
        messages=messages,
        tools=tools,
        model="llama-3.1-8b-instant",
        max_tokens=50,
        temperature=0.2,
    )

    return response.tool_calls[0].function.name
```

Send the user's question along with the tool descriptions. The model reads the question, reads the descriptions, and replies with something like:

```json
{
  "tool_calls": [{
    "function": { "name": "get_courses" }
  }]
}
```

Notice `max_tokens=50` and `temperature=0.2`. Picking a tool is a short, deterministic decision. You don't need creativity here, and you don't need many tokens. Use the cheapest, tightest settings that get the job done.

### Step 2: execute the chosen tool

```python
def execute_tool(tool_name):
    if tool_name in tool_functions:
        return tool_functions[tool_name]()
    else:
        raise ValueError(f"Unknown tool: {tool_name}")
```

Look up the Python function in the dispatch map and call it. This step is pure Python with the model sitting out. The model gave you a string, you turned it into a function call.

The `ValueError` branch matters more than it looks. The model is allowed to invent function names that don't exist. A defensive check stops a fabricated tool name from crashing the whole app.

### Step 3: send results back to the model for the final answer

```python
def generate_final_response(user_query, tool_name, tool_results):
    if not tool_results["data"]:
        context = f"No data was found using the {tool_name} tool."
    else:
        context = "Here is the retrieved information:\n"
        for row in tool_results["data"]:
            row_details = [f"{column}: {value}" for column, value in zip(tool_results["columns"], row)]
            context += ", ".join(row_details) + "\n"

    final_prompt = f"""
    You are an academic advising assistant. Answer the user's query using the following retrieved information:

    {context}

    User Query: {user_query}
    """

    messages = add_system_message([], final_prompt)
    final_response = generate_response(
        messages=messages,
        model="llama-3.1-8b-instant",
        max_tokens=300,
        temperature=0.2
    )
    return final_response
```

Same prompt-stuffing trick from page 2, except now the data was chosen on the fly instead of pulled blindly. The model writes the actual answer the user sees.

This step uses bigger `max_tokens` because the answer might be a paragraph, not a single function name. Still low temperature because the job is reading data and reporting on it.

## Putting the three steps together

`advising_bot_with_tool_calls` chains the three steps:

```python
def advising_bot_with_tool_calls(user_query):
    tool_name = generate_tool_call(user_query)
    print(colored("Tool Calls:", "cyan"), colored(tool_name, "blue"))

    tool_results = execute_tool(tool_name)
    print(colored(f"Tool Results for {tool_name}:", "green"), colored(tool_results, "blue"))

    response = generate_final_response(user_query, tool_name, tool_results)
    return response
```

The colored print statements are deliberate. They make the model's reasoning visible so you can watch it pick a tool, see what came back, and read the final answer. That kind of visibility is gold when you're debugging a tool-using app.

Run the cell and try a few questions:

- `What courses are offered in Winter?` (should pick `get_courses`)
- `Who is Mei's advisor?` (should pick `get_students`)
- `What's Tina Ostrander's email?` (should pick `get_instructors`)

Each one should print the chosen tool, then the rows that came back, then a clean answer.

> **With your partner:** Try a question that doesn't cleanly match any tool, like `What's the weather today?` or `Who got an A in Machine Learning?`. What happens? Why?

<details>
<summary>Reveal answer</summary>

The model still tries to pick a tool. For the weather, it might pick `get_courses` or `get_instructors` essentially at random, then write a final answer that says something like "I don't have weather information." For the grades question, the model picks something close (`get_courses` or `get_students`) but the data it gets back doesn't include grades, so the final answer is wrong or evasive. The model can only do as well as the tools you've given it. A question outside the available data is the most common failure mode of a tool-using bot, and it's the reason you're going to add a grades tool on page 4.

</details>

## Why this beats RAG

Compare cell 12 and cell 19 side by side. Same database, same model, same prompt-stuffing pattern at the end. The tool-using version is more code, and more API calls per request, and yet it is a real upgrade.

**Right data, not all data.** A question about students fetches student rows, not the entire courses table. Prompts stay tight, calls stay cheap.

**Multiple data sources.** You can wire up tools that pull from completely different places (one tool reads SQL, another calls a REST API, another runs a Python calculation), and the model picks the right one per question.

**The same bot grows.** Adding a new capability is adding a tool. The model figures out when to use it from your description. No new orchestration code per tool.

**Read and write.** Tools can be `get_courses`, but they can also be `enroll_student` or `send_advising_email`. You'll add a tool that writes to the database on the next page.

## Where tools fall short

Tool use is a powerful pattern, and it still has real costs and limits worth knowing before you reach for it.

**It is not free.** Every request is now two LLM calls (pick the tool, then write the answer) plus the tool itself. Latency and cost both go up.

**The model can still pick wrong.** If your descriptions are vague, the model will guess. Write descriptions as if you were writing docs for another developer who hasn't seen the code.

**Multi-tool flows are harder.** This notebook calls exactly one tool per request. Real apps often need the model to call tool A, look at the result, then decide to also call tool B. That's the realm of **agents**, and it's its own can of worms. Same building blocks, more orchestration.

For now, the single-tool-call pattern is the right starting point. Page 4 is where you stretch it.
