---
title: "Introduction to Agile"
order: 1
---

Software projects fail all the time. Most failures share the same root cause. 

**The team built the wrong thing.** 

A client asks for one thing, a developer hears something slightly different, six weeks of work later everyone is unhappy, and nobody is technically wrong.

Agile is a set of practices built to close that gap. The core idea is to break work into small, clearly defined pieces, communicate continuously, and validate early. This unit focuses on one of the most practical parts of Agile, defining work clearly before you start building it.

## The Problem With Vague Requirements

> **With your partner:** Before clicking anything in the activity, talk through what you each would have built from that requirement. Did you picture the same thing?

{% activity "requirements-disaster.html", "Requirements Disaster", "560px" %}

## User Stories

A **user story** is a short description of a feature told from the perspective of the person who will use it. The format is:

*As a [type of user], I want [goal] so that [reason].*

Every part of that sentence is doing work.

- **Type of user** names who is asking. "A user" is often too vague. "A registered shopper," "a site admin," or "a first-time visitor" gives the team a much clearer picture of what the feature needs to do.
- **Goal** describes what the user wants to accomplish. Keep it focused on their outcome. Save implementation details for later.
- **Reason** explains why it matters. This often reveals whether the feature is actually worth building and can change how you design it.

Here's a full example:

*As a music fan visiting the site, I want to browse all artists on the label so that I can discover music I might like.*

That single sentence rules out a dozen incorrect interpretations before a single line of code is written.

For each prompt below, write a user story with your partner before revealing the answer.

### Question 1

You're working on an online marketplace where shoppers browse and buy products from independent sellers. The client's request from the kickoff call is one sentence.

"We want users to be able to save things they like."

> **With your partner:** Write a user story for this feature.

<details>
<summary>Reveal answer</summary>

There are multiple valid answers, but the user and reason need to be specific. One example:

*As a logged-in shopper, I want to save products to a wishlist so that I can come back to them later without losing track.*

A version like "As a user, I want to save things so that I can use them" is too vague on all three parts. Who is saving? What exactly are they saving? Why does it matter to them?

</details>

### Question 2

You're building a recipe sharing platform where home cooks post and discover recipes. You get this in an email from the client.

"We need to add some kind of search."

> **With your partner:** Write a user story for this feature.

<details>
<summary>Reveal answer</summary>

Example:

*As a home cook browsing the platform, I want to search for recipes by ingredient so that I can find dishes I can make with what I already have.*

Notice the goal specifies what is being searched and how. A story like "As a user, I want to search so that I can find things" leaves every important decision open. Search by ingredient and search by dish name are two completely different features.

</details>

### Question 3

You're building a freelance services platform where clients hire contractors for short-term projects. Here's the relevant line from their requirements doc.

"The site needs to handle payments."

> **With your partner:** Write a user story for this feature.

<details>
<summary>Reveal answer</summary>

Example:

*As a client completing a project hire, I want to pay a contractor using a credit or debit card so that I can complete the transaction without leaving the platform.*

"Handle payments" could mean a checkout flow, subscription billing, invoice generation, in-person card readers, or a dozen other things. The user story narrows it down immediately.

</details>

## Acceptance Criteria

A user story tells you what to build. **Acceptance criteria** tell you when it's done.

Acceptance criteria make "done" specific and testable. "It works" and "it looks good on mobile" are subjective judgements that two people on a team will interpret differently. A well-written criterion is something you can check with a concrete yes or no.

The format uses three parts, **Given / When / Then**.

- **Given** sets the starting state (where the user is, what conditions exist)
- **When** describes the action the user takes
- **Then** describes the observable result

Here's an example for the artist browsing story from above:

*Given I am on the label's homepage, when the page loads, then all artists are displayed with their name, genre, and bio visible.*

*Given I view the page on a screen 375px wide, when the page loads, then the artist cards stack vertically and all text remains readable without horizontal scrolling.*

Each criterion is a test you can actually run. Either the text is readable at 375px or it isn't. Either every artist shows their genre or it doesn't.

> **With your partner:** For each user story below, write two or three acceptance criteria before revealing the answer.

### Question 4

You're working on the freelance platform from earlier. A client wants contractors to be able to recover their accounts.

*As a registered contractor, I want to reset my password so that I can regain access to my account if I forget it.*

> **With your partner:** Write acceptance criteria for this story.

<details>
<summary>Reveal answer</summary>

Example acceptance criteria:

*Given I am on the login page, when I click "Forgot password" and submit my email address, then I receive a password reset email within two minutes.*

*Given I click the reset link in the email, when I enter a new password and confirm it, then my password is updated and I am redirected to the login page.*

*Given the reset link is more than 24 hours old, when I click it, then I see a message telling me the link has expired and prompting me to request a new one.*

Notice each criterion describes a specific situation, a specific action, and a specific testable outcome.

</details>

### Question 5

You're on the online marketplace from earlier. The client wants shoppers to be able to narrow down what they see.

*As a shopper browsing the marketplace, I want to filter products by category so that I can find what I'm looking for without scrolling through everything.*

> **With your partner:** Write acceptance criteria for this story.

<details>
<summary>Reveal answer</summary>

Example acceptance criteria:

*Given I am on the products page, when I select a category from the filter, then only products in that category are displayed.*

*Given a filter is applied, when there are no matching products, then I see a message saying "No results found."*

*Given I apply a filter, when I clear the filter, then all products are displayed again.*

</details>

### Question 6

You're on the recipe platform. The client wants cooks to feel confident their recipes were saved successfully.

*As a home cook, I want to receive confirmation when I publish a recipe so that I know it's live and visible to others.*

> **With your partner:** Write acceptance criteria for this story.

<details>
<summary>Reveal answer</summary>

Example acceptance criteria:

*Given I click "Publish" on a completed recipe, when the save succeeds, then I see a confirmation message telling me the recipe is now live.*

*Given my recipe is published, when I navigate to the recipe's page, then it is visible and shows the correct title, ingredients, and steps.*

*Given I am viewing the confirmation, when I open it on a mobile device, then the message is readable and not cut off.*

</details>

## Backlogs

Once you have your user stories, they live in a **backlog**. It's a prioritized list of all the work that needs to happen but hasn't been started yet. Stories sit in the backlog until the team is ready to work on them. When work begins on a story, it moves to in progress. When it meets all its acceptance criteria, it moves to done.

{% activity "backlog-kanban.html", "Managing a Backlog", "420px" %}

On the next page you'll write user stories and acceptance criteria for a fictional client project and set up a backlog on GitHub to track them.
