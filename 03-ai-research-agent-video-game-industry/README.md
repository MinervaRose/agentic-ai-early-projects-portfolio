# 🎮 UdaPlay – AI Research Agent for Video Game Intelligence

### Retrieval-Augmented Generation, Memory, Web Search, and Stateful AI Agents

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![RAG](https://img.shields.io/badge/RAG-Retrieval_Augmented_Generation-purple?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-green?style=for-the-badge)
![AI Agent](https://img.shields.io/badge/AI_Agent-Stateful_Workflows-red?style=for-the-badge)
![Web Search](https://img.shields.io/badge/Web_Search-Tavily-orange?style=for-the-badge)
![Memory](https://img.shields.io/badge/Long_Term-Memory-teal?style=for-the-badge)

---

# Agentic AI Early Projects Portfolio

### Project 3 of 4

---

## Overview

UdaPlay is an AI-powered research assistant designed to answer questions about video games using both internal knowledge and external information sources.

The project explores how modern AI systems can combine:

* Retrieval-Augmented Generation (RAG)
* Vector databases
* Semantic search
* Web search
* Memory systems
* Evaluation mechanisms

to create more reliable and informative responses than standalone language models.

Developed as part of the Udacity Agentic AI Nanodegree, UdaPlay demonstrates a complete research workflow in which an AI agent first searches its internal knowledge base before expanding to external sources when necessary.

---

## Project Goal

The objective was to build an AI research agent capable of answering questions such as:

* Who developed FIFA 21?
* When was God of War Ragnarök released?
* What platform was Pokémon Red launched on?
* What is Rockstar Games currently developing?

Rather than relying solely on LLM knowledge, the system follows a structured retrieval strategy:

1. Search internal knowledge.
2. Evaluate retrieval quality.
3. Decide whether information is sufficient.
4. Fall back to web search when necessary.
5. Store useful findings in memory.
6. Generate a final answer with citations.

This mirrors the architecture used by many modern AI assistants and research copilots.

---

## System Architecture

UdaPlay uses a layered retrieval strategy.

```text
User Question
      │
      ▼
Internal Knowledge Search
      │
      ▼
 Retrieval Evaluation
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Accept   Web Search
Result   Fallback
 │         │
 └────┬────┘
      ▼
Memory Update
      │
      ▼
Final Response
```

The architecture is designed to prioritize trusted internal information while still allowing the agent to expand its knowledge through external sources when required.

---

## Core Components

### Local Knowledge Base

The project begins with a structured collection of video game information stored as JSON documents.

The dataset contains information including:

* Game titles
* Publishers
* Developers
* Genres
* Platforms
* Release dates
* Descriptions

These documents form the foundation of the retrieval system.

---

### Vector Database

The game dataset is transformed into embeddings and stored within a persistent vector database.

This enables semantic search rather than simple keyword matching.

Example:

A query such as:

```text
"What football games were released recently?"
```

can retrieve relevant FIFA titles even if the exact title is not mentioned.

---

### Retrieval-Augmented Generation (RAG)

The first stage of the agent workflow relies on Retrieval-Augmented Generation.

```text
Question
    │
    ▼
Vector Search
    │
    ▼
Relevant Documents
    │
    ▼
LLM Response
```

The retrieved context is supplied to the language model before answer generation.

This improves factual grounding while reducing hallucinations.

---

### Evaluation Layer

An evaluation tool assesses retrieval quality.

The evaluation process considers:

* Relevance
* Completeness
* Confidence
* Coverage

If confidence falls below a defined threshold, the system activates a secondary retrieval mechanism.

This introduces a simple but powerful decision-making layer into the workflow.

---

### Web Search Fallback

When local knowledge is insufficient, the agent performs a web search.

This allows UdaPlay to answer questions about:

* Recently released games
* Newly announced titles
* Company activities
* Emerging industry news

The project demonstrates how external search can extend the capabilities of a retrieval system beyond its original dataset.

---

### Long-Term Memory

Newly discovered information can be persisted into memory.

This allows the system to gradually expand its knowledge base over time.

Conceptually, the workflow becomes:

```text
Question
    │
    ▼
Retrieve
    │
    ▼
Learn
    │
    ▼
Remember
```

This introduces a foundational capability often associated with next-generation AI assistants.

---

### Stateful Agent Design

Unlike a simple chatbot, UdaPlay maintains conversation state.

The agent can:

* Track previous interactions
* Reuse retrieved information
* Maintain context across questions
* Coordinate multiple tool calls

This creates a more coherent user experience across longer research sessions.

---

## Example Workflow

### User Query

```text
When was God of War Ragnarök released?
```

### Agent Actions

1. Search vector database.
2. Retrieve relevant documents.
3. Evaluate confidence.
4. Generate response.

### Final Answer

```text
God of War Ragnarök was released on
November 9, 2022.

Platforms:
- PlayStation 4
- PlayStation 5

Source:
Internal Knowledge Base
```

---

## AI Engineering Concepts Demonstrated

### Retrieval Systems

* Semantic Search
* Embedding-Based Retrieval
* Vector Databases
* Document Processing

### Agent Design

* Stateful Agents
* Tool Calling
* Workflow Management
* Decision Logic

### Research Systems

* Knowledge Retrieval
* Source Evaluation
* Web Search Integration
* Citation Generation

### Memory Systems

* Long-Term Memory
* Information Persistence
* Knowledge Expansion

---

## Skills Demonstrated

### AI Systems

* Retrieval-Augmented Generation
* Research Agent Design
* Information Fusion
* Memory Architectures

### Python

* JSON Processing
* Database Integration
* Workflow Construction
* Agent Frameworks

### LLM Engineering

* Grounded Generation
* Context Injection
* Retrieval Evaluation
* Confidence-Based Routing

---

## Key Learnings

This project provided practical experience in building AI systems that retrieve information rather than relying entirely on model parameters.

Important lessons included:

* High-quality retrieval often matters more than larger models.
* Vector databases provide powerful semantic search capabilities.
* Evaluation mechanisms improve reliability.
* Web search dramatically expands system usefulness.
* Memory systems create opportunities for continuous learning.
* Research agents benefit from explicit decision-making stages.

Many of these concepts underpin modern AI copilots, enterprise search systems, and knowledge assistants.

---

## Potential Extensions

Future improvements could include:

* Hybrid keyword + semantic retrieval
* Multi-hop reasoning
* Knowledge graph integration
* Source ranking systems
* Citation verification
* Autonomous research workflows
* Multi-agent research teams

---

## Repository Context

This project is part of my **Agentic AI Early Projects Portfolio** and documents my exploration of retrieval systems, AI research agents, memory architectures, and knowledge-grounded language model applications.

It represents an early investigation into many of the technologies powering modern AI assistants and information retrieval platforms.

---

## Author

**S. Palis**

AI Systems • Applied AI Education • Computational Research

Exploring retrieval systems, scientific discovery tools, agentic workflows, and human-centered AI architectures.
