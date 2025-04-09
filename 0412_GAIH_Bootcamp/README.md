# Global AI Bootcamp 2025 Hyderabad - 12 April 2025

## Date Time: 12-Apr-2025 at 09:30 AM IST

## Event URL: [https://www.meetup.com/global-ai-hyderabad/events/306095644](https://www.meetup.com/global-ai-hyderabad/events/306095644)

![Viswanatha Swamy P K |150x150](./Documentation/Images/ViswanathaSwamyPK.PNG)

---

### Software/Tools

> 1. OS: Windows 10/11 x64
> 1. Python / .NET 8
> 1. Visual Studio 2022
> 1. Visual Studio Code

### Prior Knowledge

> 1. Programming knowledge in C# / Python

## Technology Stack

> 1. .NET 8, AI, Open AI

## Information

![Information | 100x100](../Documentation/Images/Information.PNG)

## What are we doing today?

> 1. The Big Picture
> 1. Quick Introduction
> 1. SUMMARY / RECAP / Q&A

### Please refer to the [**Source Code**](https://github.com/Swamy-s-Tech-Skills-Academy/learn-ai-102-code) of today's session for more details

---

![Information | 100x100](../Documentation/Images/SeatBelt.PNG)

---

## Keynote - Apr-2025: From a Developer's Perspective

### Our Progress Over Time

> 1. A visual journey: from black-and-white screens to modern IDEs with advanced syntax highlighting.

### GitHub Copilot in Action

> 1. How it generates code and helps us understand our code better.

### Expanding AI Use Cases

> 1. Leveraging AI for Development, Media, DevOps, Customer Support, and more.

### Accelerating Work with Chatbots Powered by RAG

> 1. Demonstrating how Retrieval-Augmented Generation (RAG) can speed up workflows.

### Streamlining Our Jobs with AI

> 1. Using AI to simplify tasks while keeping security in focus.

### Automating Repetitive Tasks

> 1. Utilizing batch files, PowerShell scripts, etc., to reduce manual work.

### Getting Started with AI

> 1. Key resources and starting points: [Microsoft AI Developer Resources](https://developer.microsoft.com/en-us/ai).

### Data-Driven Learning in AI

> 1. How AI learns from our data to continuously improve and adapt.

### The Future of AI-Driven Development

> 1. Exploring emerging trends, innovations, and ethical considerations that will shape the next generation of developer tools and practices.
> 1. A look at how the evolving AI landscape will further empower developers, and how we can prepare for these changes.

---

## 1. Mastering Prompt Engineering with Azure OpenAI Service

> 1. Discussing the importance of prompt engineering in AI applications.
> 1. Key strategies for effective prompt design.
> 1. Real-world examples of prompt engineering in action.

## 2. 30,000 foot view of Azure OpenAI

> 1. Discussion and Demo

### 2.1. What is Azure OpenAI Service?

> 1. Discussion and Demo
> 1. [https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview)

### 2.2. Azure OpenAI Service quotas and limits

> 1. Discussion and Demo
> 1. [https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quotas-limits](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quotas-limits)

### 2.3. Azure OpenAI Service models

> 1. Discussion and Demo
> 1. [https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models)

## 3. Access Azure OpenAI Service

> 1. Discussion and Demo

### 3.1. Creating Azure Open AI using Azure Portal

> 1. Discussion and Demo

### 3.2. Creating Azure Open AI using az CLI

> 1. Discussion and Demo
> 1. <https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models#model-summary-table-and-region-availability/?azure-portal=true>

```powershell
$aoaiName = "azoai-ai102-dev-" + (Get-Random)
$resourceGroup = "rg-ai102-dev-001"
$subscriptionID = "YourSubscriptionId"

az account show

az account list-locations --output table

az cognitiveservices account list --subscription $subscriptionID --output table

az cognitiveservices account create -n $aoaiName -g $resourceGroup -l eastus --kind OpenAI --sku s0 --subscription $subscriptionID
```

## 4. Use Azure OpenAI Foundry

> 1. Discussion and Demo
> 1. Deploying OpenAI models using Azure OpenAI Foundry.

## 10. Tokens Tokens Tokens and more Tokens

> 1. Discussion and Demo

**References:**

> 1. [https://platform.openai.com/tokenizer](https://platform.openai.com/tokenizer)

## 2. What is Prompt Engineering ?

Prompt engineering is an essential practice when working with language models like those offered by Azure OpenAI. It revolves around the concept of creating, refining, and optimizing input prompts to elicit specific and desired outputs from these models. Here's a breakdown of what it entails:

### Core Concept

At its core, prompt engineering involves carefully crafting the input that you provide to a language model. The aim is to guide the model's output, making it more accurate, relevant, and aligned with the desired outcome.

### Importance

Since language models generate text based on the prompts they receive, the quality, structure, and clarity of the prompt significantly affect the output. This is why prompt engineering is crucial for tasks that require high precision and contextual relevance.

## 3. Components of Effective Prompt Engineering

### Clarity

The prompt should be clear and unambiguous. This ensures that the model understands the task and generates relevant outputs.

### Specificity

Providing detailed instructions within the prompt can help the model focus on what is most important, reducing the likelihood of irrelevant or off-topic responses.

### Context

Adding context to the prompt can significantly improve the model’s ability to generate appropriate responses. Context can include background information, examples, or specific constraints.

### Formatting

Specifying the format of the desired output, such as bullet points, paragraphs, or specific structures, can help guide the model to produce text that is easier to use.

## 4. Techniques in Prompt Engineering

### Single Turn

> 1. Discussion and Demo

### Iterative

> 1. Discussion and Demo

### Conversational

> 1. Discussion and Demo
> 1. Memory / Context between Completions VS Chat

### Role play

> 1. Discussion and Demo
> 1. `Cardiologist` versus `Assistant`
> 1. Prompt: What is `TV`?

### Zero Shot

> 1. Discussion and Demo

### Single Shot

> 1. Discussion and Demo

### Few Shots

> 1. Discussion and Demo

### CoT

> 1. Chain of Thought (CoT) is a problem-solving approach that involves breaking down a complex problem into a series of smaller, logical steps or intermediate reasoning points. This method helps ensure a clear and systematic progression from the initial conditions to the final solution, enhancing accuracy and understanding by explicitly documenting the thought process at each stage.
> 1. Prompt designed to encourage the use of Chain of Thought (CoT) reasoning.

```text
"Please solve the following problem using a Chain of Thought (CoT) approach, which involves breaking the problem down into smaller, logical steps to ensure a clear and systematic progression to the solution. Show each intermediate step and explain your reasoning."

Example Problem: "A bakery had 50 cupcakes. They sold 15 in the morning and then baked 20 more in the afternoon. How many cupcakes do they have now?"

**Expected CoT Response:**

1. Start with the initial number of cupcakes: 50.
2. Subtract the number of cupcakes sold in the morning: \( 50 - 15 = 35 \).
3. Add the number of cupcakes baked in the afternoon: \( 35 + 20 = 55 \).
4. The bakery now has 55 cupcakes.
```

```text
Q: Roger has 5 tennis balls. He buys 2 more cans of
tennis balls. Each can has 3 tennis balls. How many
tennis balls does he have now?

A: Roger started with 5 balls. 2 cans of 3 tennis balls
each is 6 tennis balls. 5 + 6 = 11. The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 to
make lunch and bought 6 more, how many apples
do they have?
```

## 5. Best Practices for Text-Based Prompt Engineering

### Be Explicit

The more explicit and detailed your prompt, the better the model can align its output with your expectations.

### Test and Iterate

Start with a basic prompt and refine it based on the results. Use iterative testing to improve the model’s performance.

### Leverage Context

Whenever possible, include context that can help the model understand the nuances of the task.

### Monitor and Adjust

Regularly monitor the outputs and adjust your prompts to address any inaccuracies or undesired behaviors.

> Prompt engineering in the context of Azure OpenAI is about using these techniques to maximize the efficiency and effectiveness of AI-driven text generation, making it a powerful tool for developers and content creators alike.

## Prompts for reference

```text
Input: Please write a Happy Birthday wishes for my Mother

Input: Give the top 5 food items from South India

Input: Give the top 5 Populated states in India

Inputs:
1. Which is the tallest building in the world
2. Which is the tallest building in Hyderabad

Input: Tell me two jokes about simple people

Write a promotional email for a new wildlife rescue, including the following: - Rescue name is Contoso - It specializes in elephants, as well as zebras and giraffes - Call for donations to be given at our website \n Include a list of the current animals we have at our rescue after the signature, in the form of a table. These animals include elephants, zebras, gorillas, lizards, and jackrabbits.
```

## 5. Chat playground

> 1. Discussion and Demo
> 1. Using the chat playground to interact with OpenAI models.

## 6. Chat using Rest API

> 1. Discussion and Demo
> 1. [https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart](https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart)

## 6. Chat using `C#`

> 1. Discussion and Demo

## 7. Chat using `Python`

> 1. Discussion and Demo

---

## SUMMARY / RECAP / Q&A

> 1. SUMMARY / RECAP / Q&A
> 2. Any open queries, I will get back through meetup chat/twitter.

---
