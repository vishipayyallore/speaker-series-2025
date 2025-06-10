# AI-102 - Creating a Knowledge Store with Azure AI Search

## Date Time: 10-Jun-2025 at 03:30 PM IST

## Event URL: [https://www.meetup.com/microsoft-reactor-bengaluru/events/307800670](https://www.meetup.com/microsoft-reactor-bengaluru/events/307800670)

## YouTube URL: [https://www.youtube.com/watch?v=Ds9kQmWKRBU](https://www.youtube.com/watch?v=Ds9kQmWKRBU)

![Viswanatha Swamy P K |150x150](./Documentation/Images/ViswanathaSwamyPK.PNG)

---

### Software/Tools

> 1. OS: Windows 10/11 x64
> 2. Python / .NET 8
> 3. Visual Studio 2022
> 4. Visual Studio Code

### Prior Knowledge

> 1. Programming knowledge in C# / Python

## Technology Stack

> 1. .NET 8, AI, Open AI

## Information

![Information | 100x100](../Documentation/Images/Information.PNG)

## What are we doing today?

> 1. 🔭 The Big Picture
>    - Pre-requisites
>    - Previous Session(s)
>    - Microsoft Learn Module(s)
> 2. 🔄 SUMMARY / RECAP / Q&A

### Please refer to the [**Source Code**](https://github.com/Swamy-s-Tech-Skills-Academy-AI-ML-Data/learn-ai102) of today's session for more details

---

![Information | 100x100](../Documentation/Images/SeatBelt.PNG)

---

## 1. 🔭 The Big Picture

### 1.1. Pre-requisites

> 1. Azure Subscription
> 2. .NET 8 / Python

### 1.2. Previous Session(s)

> 1. <https://youtube.com/playlist?list=PLmsFUfdnGr3wmIh-glyiMkhHS6byEuI59&si=5vlmcUqOuWqFiCRR>

### 1.3. Microsoft Learn Module(s)

> 1. <https://aka.ms/Azure-AISearch>

## 2. 🔍 Introduction to Knowledge Stores

Azure AI Search enables you to create search solutions in which a pipeline of AI skills is used to enrich data and populate an index. The data enrichments performed by the skills in the pipeline supplement the source data with insights such as:

- **Language Detection**: The language in which a document is written
- **Key Phrases**: Main themes or topics discussed in a document
- **Sentiment Analysis**: Sentiment score that quantifies how positive or negative a document is
- **Entity Recognition**: Specific locations, people, organizations, or landmarks mentioned in the content
- **OCR & Image Analysis**: AI-generated descriptions of images, or image text extracted by optical character recognition (OCR)

The enriched data in the index makes it possible to create a comprehensive search solution that goes beyond basic full text search of the source content.

### 🗄️ What are Knowledge Stores?

While the index might be considered the primary output from an indexing process, the enriched data it contains might also be useful in other ways. For example:

- **Data Integration**: Export objects as JSON files for integration into a data orchestration process using tools such as Azure Data Factory
- **Analytics & Reporting**: Normalize the index records into a relational schema of tables for analysis and reporting with tools such as Microsoft Power BI
- **File Storage**: Save extracted embedded images from documents as files

### 🏗️ Knowledge Store Architecture

Azure AI Search supports these scenarios by enabling you to define a **knowledge store** in the skillset that encapsulates your enrichment pipeline. The knowledge store consists of **projections** of the enriched data, which can be:

1. **JSON Objects** - For data integration scenarios
2. **Tables** - For relational analysis and reporting
3. **Image Files** - For extracted images and media

When an indexer runs the pipeline to create or update an index, the projections are generated and persisted in the knowledge store.

### 🎯 Session Objectives

In this session, you'll implement a knowledge store for **Margie's Travel**, a fictitious travel agency that uses information in brochures and hotel reviews to help customers plan trips. You will learn how to:

✅ **Create a knowledge store** from an Azure AI Search pipeline  
✅ **View data in projections** in a knowledge store  
✅ **Query and analyze** enriched data from multiple perspectives

---

## 8. 🔄 SUMMARY / RECAP / Q&A

> 1. SUMMARY / RECAP / Q&A
> 2. Any open queries, I will get back through meetup chat/twitter.

---
