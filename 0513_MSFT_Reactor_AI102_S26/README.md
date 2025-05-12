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
> 4. 🔈 Use the text to speech API
> 5. 🔋 Manage capacity
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

> Problem: finding relevant information in large, unstructured data sets.

**Example**: Margie’s Travel has thousands of brochures and customer reviews—agents need a fast way to locate answers.

**Solution**: Azure AI Search indexes your data, applies AI enrichment, and exposes a high-scale search API.

With Azure AI Search you can:

- Index documents and databases in a few clicks
- Enrich content with built-in cognitive skills
- Query using full-text search, filters, and facets

## 3. 🏗️ Provision an Azure resource for speech

> 1. Discussion and Demo

## 4. 🔋 Manage capacity

When provisioning your Azure AI Search resource, choose a pricing tier to set capacity limits, features, and cost:

- **Free (F)**: Up to 3 indexes, 50 MB storage—exploration and tutorials
- **Basic (B)**: Up to 15 indexes, 5 GB storage—small workloads
- **Standard (S/S2/S3/S3HD)**: Scalable enterprise tiers with increasing storage and performance
- **Storage optimized (L1/L2)**: Large-index support, higher query latency

> **Note**: You cannot change tiers on an existing resource. To scale up, create a new service and reindex.

Optimize performance with **replicas** and **partitions**:

- **Replicas (R)**: Duplicate service instances for concurrency and high availability
- **Partitions (P)**: Shard index storage for larger datasets

Search units (SU) = R × P (e.g., 4 replicas × 3 partitions = 12 SU)

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

## 6. ⚙️ Understand the indexing process

Azure AI Search processes each document through a multi-stage pipeline:

1. **Initial document**

   - Raw fields from your data source are mapped into a JSON document:

   ```json
   {
     "metadata_storage_name": "...",
     "metadata_author": "...",
     "content": "..."
   }
   ```

2. **Normalize images** _(optional)_

   - Image data extracted into an array:

   ```json
   "normalized_images": [
     { "image": <binary> },
     { "image": <binary> }
   ]
   ```

3. **Apply cognitive skills**

   - Skills run per document or per array item (e.g., OCR on each image):
     - Language detection → `language`
     - OCR on images → `imageText`
     - Any custom or built-in skill adds new fields

4. **Merge content** _(optional)_

   - Use a merge skill to combine original `content` + `imageText` into `merged_content`.

5. **Map to index**
   - **Implicit**: fields with matching names map automatically
   - **Explicit**: define mappings to rename or transform fields

The final enriched JSON is ready for querying once indexed.

```json
{
  "metadata_storage_name": "report.pdf",
  "metadata_author": "Alice",
  "content": "This report outlines the quarterly financial results...",
  "normalized_images": [
    { "image": "<binary>", "imageText": "Sales chart Q1" },
    { "image": "<binary>", "imageText": "Revenue table" }
  ],
  "language": "en",
  "merged_content": "This report outlines the quarterly financial results... Sales chart Q1 Revenue table"
}
```

## 7. 🔎 Search an index

Once your index is populated, query it using Azure AI Search REST API or SDKs.

### Lucene query types

- **Simple**: literal term matching (e.g., `hotel`)
- **Full**: advanced syntax—regex, fuzzy, proximity, and filters

### Common parameters

- `search` — terms to find
- `queryType` — `simple` or `full`
- `searchFields` — fields to search (comma-separated)
- `select` — fields to return
- `searchMode` — `any` (OR) or `all` (AND)

### Sample REST request

```bash
curl -X GET "https://<service>.search.windows.net/indexes/<index>/docs?api-version=2021-04-30-Preview" \
  -H "api-key: <your-key>" \
  --data-urlencode "search=hotel" \
  --data-urlencode "searchFields=content,merged_content" \
  --data-urlencode "select=metadata_storage_name,merged_content" \
  --data-urlencode "searchMode=all"
```

### Query processing stages

1. **Parsing** — build subqueries (term, phrase, prefix)
2. **Lexical analysis** — lowercase, stopword removal, stemming
3. **Retrieval** — match terms to documents
4. **Scoring** — compute relevance via TF/IDF

## 8. 🛠️ Apply filtering & sorting

Refine results using filters, facets, and custom sort orders.

### Filtering

- **Simple syntax**:

  ```bash
  curl -X GET "https://<service>.search.windows.net/indexes/<index>/docs?api-version=2021-04-30-Preview" \
    -H "api-key: <your-key>" \
    --data-urlencode "search=London+author:'Reviewer'" \
    --data-urlencode "queryType=simple"
  ```

- **OData filter (full syntax)**:

  ```bash
  curl -X GET "https://<service>.search.windows.net/indexes/<index>/docs?api-version=2021-04-30-Preview" \
    -H "api-key: <your-key>" \
    --data-urlencode "search=London" \
    --data-urlencode "$filter=author eq 'Reviewer'" \
    --data-urlencode "queryType=full"
  ```

> **Tip**: OData `$filter` expressions are case-sensitive.

### Facets

- **Retrieve facet values**:

  ```bash
  curl -X GET "https://<service>.search.windows.net/indexes/<index>/docs?api-version=2021-04-30-Preview" \
    -H "api-key: <your-key>" \
    --data-urlencode "search=*" \
    --data-urlencode "facet=author"
  ```

- **Filter by facet selection**:

  ```bash
  curl -X GET "https://<service>.search.windows.net/indexes/<index>/docs?api-version=2021-04-30-Preview" \
    -H "api-key: <your-key>" \
    --data-urlencode "search=*" \
    --data-urlencode "$filter=author eq 'SelectedValue'"
  ```

### Sorting

- **By relevance** (default)

- **Custom order**:

  ```bash
  curl -X GET "https://<service>.search.windows.net/indexes/<index>/docs?api-version=2021-04-30-Preview" \
    -H "api-key: <your-key>" \
    --data-urlencode "search=*" \
    --data-urlencode "$orderby=last_modified desc"
  ```

## X. 🔄 SUMMARY / RECAP / Q&A

> 1. SUMMARY / RECAP / Q&A
> 2. Any open queries, I will get back through meetup chat/twitter.

---
