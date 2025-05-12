# AI-102 - Building Intelligent Search Solutions with Azure AI Search

## Date Time: 13-May-2025 at 03:30 PM IST

## Event URL: [https://www.meetup.com/microsoft-reactor-bengaluru/events/307042690](https://www.meetup.com/microsoft-reactor-bengaluru/events/307042690)

## YouTube URL: [https://www.youtube.com/watch?v=RKFELXBefeY](https://www.youtube.com/watch?v=RKFELXBefeY)

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
> 2. 🔊 Introduction
> 3. 🏗️ Provision an Azure resource for speech
> 4. 🗣️ Use the Azure AI Speech to Text API
> 5. 🔈 Use the text to speech API
> 6. 🔄 SUMMARY / RECAP / Q&A

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

> 1. <https://aka.ms/AISpeech-Service>

---

## 2. 🔊 Introduction

To be done

## 3. 🏗️ Provision an Azure resource for speech

To be done

## 4. 🔋 Manage capacity

To be done

## 5. 🔍 Understand search components

An Azure AI Search solution is built from several core components, each contributing to data ingestion, enrichment, indexing, and querying.

### • Data source

A data source is a connection to a repository of content. It defines how to connect to the content and how to pull data from it. Azure AI Search supports several types of data sources, including:

- **Blob storage** (unstructured files)
- **Azure SQL Database** (tables)
- **Cosmos DB** (JSON documents)

Alternatively, applications can push JSON data directly into an index.

### • Skillset

> 1. A skillset is a collection of AI skills that can be applied to content in an index. It defines how to extract insights from your data and how to map those insights into the index schema.
> 1. Skillsets define an enrichment pipeline of AI skills that extract insights from your source content. Common AI skills include:

- Language detection
- Key phrase extraction
- Sentiment analysis
- Entity recognition (people, locations, organizations)
- OCR and image analysis
- You can also create **custom skills** to handle specialized processing.

### • Indexer

An indexer is a component that connects a data source to an index. It defines how to pull data from the source, run the skillset, and map the extracted fields into the index schema.

The indexer orchestrates the indexing workflow by:

1. Pulling data from the data source
2. Running the skillset to enrich content
3. Mapping the extracted fields into the index

Indexers can run on demand or on a schedule. If you update your index schema or skillset, reset the index before rerunning.

### • Index

An index is a searchable store of JSON documents. It defines the schema for the data you want to search and how to query it.
Each field in the index can be configured with these attributes:

- **Key**: Unique identifier for each document
- **Searchable**: Include in full-text search
- **Filterable**: Support filter expressions
- **Sortable**: Enable sorting of results
- **Facetable**: Generate facet counts
- **Retrievable**: Include in query results (default is true)

## 6. 🔄 SUMMARY / RECAP / Q&A

> 1. SUMMARY / RECAP / Q&A
> 2. Any open queries, I will get back through meetup chat/twitter.

---
