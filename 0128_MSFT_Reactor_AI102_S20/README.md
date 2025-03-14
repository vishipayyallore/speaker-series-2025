# AI-102 - Build a Conversational Language Understanding Model with Azure AI

## Date Time: 28-Jan-2025 at 03:30 PM IST

## Event URL: [https://www.meetup.com/microsoft-reactor-bengaluru/events/305178630](https://www.meetup.com/microsoft-reactor-bengaluru/events/305178630)

## YouTube URL: [https://www.youtube.com/watch?v=-52GQLl8p-4](https://www.youtube.com/watch?v=-52GQLl8p-4)

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
>    - Pre-requisites
>    - Previous Session(s)
>    - Microsoft Learn Module(s)
> 1. Introduction
> 1. Understand prebuilt capabilities of the Azure AI Language service
> 1. Provision an Azure AI Language resource
> 1. Create a conversational language understanding project
> 1. Create intents
> 1. Label each intent with sample utterances
> 1. Train and test the model
> 1. Deploying a model
> 1. Testing deployments
> 1. Add entities
> 1. Develop an app in VS 2022/Code
> 1. Testing CLU using Postman
> 1. SUMMARY / RECAP / Q&A

### Please refer to the [**Source Code**](https://github.com/Swamy-s-Tech-Skills-Academy/learn-ai-102-code) of today's session for more details

---

![Information | 100x100](../Documentation/Images/SeatBelt.PNG)

---

## 1. The Big Picture

### 1.1. Pre-requisites

> 1. Azure Subscription
> 1. .NET 8 / Python

### 1.2. Previous Session(s)

> 1. <https://youtube.com/playlist?list=PLmsFUfdnGr3wmIh-glyiMkhHS6byEuI59&si=5vlmcUqOuWqFiCRR>

### 1.3. Microsoft Learn Module(s)

> 1. <https://aka.ms/AILanguage>

## 2. Introduction

This is the field of Natural Language Processing, or NLP. NLP encompasses a wide range of tasks, from simple text analysis to complex speech recognition. A key subset of NLP is Natural Language Understanding, or NLU. NLU is all about extracting the meaning from human language. It's not just about recognizing the words, but understanding what those words mean in context. Azure AI Language's Conversational Language Understanding, or CLU, is a specific NLU service on Azure. With CLU, you can train custom models to understand the intent behind user input and extract important details called entities. This allows your applications to have truly meaningful conversations with users.

## 3. Understand prebuilt capabilities of the Azure AI Language service

> 1. Discussion and Demo
> 1. `Pre-trained features`: Azure AI Language offers several pre-trained features that are ready to use out-of-the-box. These features, such as sentiment analysis, language detection, and key phrase extraction, require no model training or data labeling. Simply send your text data to the service, and it will return the results, allowing you to quickly integrate these capabilities into your applications.
> 1. `Custom features`: For more specialized needs, Azure AI Language allows you to create custom models. These features, such as custom text classification and custom named entity recognition, require you to label your own data, train a model, and deploy it before it can be used in your application. This approach provides greater flexibility and control, enabling you to tailor the model to your specific requirements and extract the precise information you need.

## 4. Provision an Azure AI Language resource

> 1. Discussion and Demo

## 5. Create a conversational language understanding project

> 1. Discussion and Demo
> 1. <https://language.cognitive.azure.com/>

![Create CLU Project](./Documentation/Images/Create_CLU_Project.PNG)

![Create CLU Project](./Documentation/Images/Create_CLU_Project_1.PNG)

## 6. Create intents

> 1. Discussion and Demo

![CLU Intents](./Documentation/Images/CLU_Intents_1.PNG)

![CLU Intents](./Documentation/Images/CLU_Intents_2.PNG)

## 7. Label each intent with sample utterances

> 1. Discussion and Demo

![CLU Data Labeling](./Documentation/Images/CLU_DataLabeling_1.PNG)

## 8. Train and test the model

> 1. Discussion and Demo

![CLU Training Jobs](./Documentation/Images/CLU_TrainingJobs_1.PNG)

![CLU Training Jobs](./Documentation/Images/CLU_TrainingJobs_2.PNG)

![CLU Model Performance](./Documentation/Images/CLU_ModelPerformance_1.PNG)

![CLU Model Performance](./Documentation/Images/CLU_ModelPerformance_2.PNG)

### Understanding the Metrics

> 1. `Precision`: Measures how often the model is correct when it predicts an intent. A high precision means the model has few false positives (predicting an intent incorrectly).
>    - `Formula`: True Positives / (True Positives + False Positives)
> 1. `Recall`: Measures how often the model correctly identifies an intent out of all the actual instances of that intent in the dataset. High recall means the model has few false negatives (missing an intent).
>    - `Formula`: True Positives / (True Positives + False Negatives)
> 1. `F1 Score`: The harmonic mean of precision and recall. It provides a balanced measure of the model's accuracy, especially when there's an imbalance between precision and recall.
>    - `Formula`: 2 \* (Precision \* Recall) / (Precision + Recall)
> 1. `Confusion Matrix`: A table that visualizes the performance of the model. It shows how often the model correctly predicted each intent (true positives), how often it incorrectly predicted an intent (false positives), and how often it failed to predict an intent (false negatives).

## 9. Deploying a model

> 1. Discussion and Demo

![CLU Deployment](./Documentation/Images/CLU_Deployment_1.PNG)

## 10. Testing deployments

> 1. Discussion and Demo

![CLU Testing](./Documentation/Images/CLU_Testing_1.PNG)

## 11. Add entities

> 1. Discussion and Demo

![CLU Add Entity](./Documentation/Images/CLU_AddEntity_1.PNG)

## 12. Develop an app in VS 2022/Code

> 1. Discussion and Demo

![CLU App in C#](./Documentation/Images/CLU_App_In_CS.PNG)

## 13. Testing CLU using Postman

> 1. Discussion and Demo

![Testing CLU using Postman](./Documentation/Images/CLU_Using_Postman.PNG)

---

## SUMMARY / RECAP / Q&A

> 1. SUMMARY / RECAP / Q&A
> 2. Any open queries, I will get back through meetup chat/twitter.

---
