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
