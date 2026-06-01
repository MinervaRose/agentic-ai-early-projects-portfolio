# ✈️ AgentsVille Trip Planner

### Agentic AI Travel Planning with Structured Outputs, ReAct Agents, and Tool Use

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=for-the-badge\&logo=jupyter)
![LLM](https://img.shields.io/badge/LLM-Prompt_Engineering-purple?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-Structured_Outputs-green?style=for-the-badge)
![ReAct](https://img.shields.io/badge/Agent-ReAct_Framework-red?style=for-the-badge)
![AI Agents](https://img.shields.io/badge/Agentic_AI-Workflow_Design-teal?style=for-the-badge)

---

## Overview

This project explores the design of a multi-stage AI travel planning system capable of generating, evaluating, and refining travel itineraries through structured reasoning and tool use.

The system was developed as part of the Udacity Agentic AI Nanodegree and focuses on several foundational concepts in modern AI engineering:

* Prompt engineering
* Structured LLM outputs
* Pydantic validation
* ReAct (Reasoning + Acting) workflows
* Tool-calling agents
* Multi-stage planning systems

The fictional city of **AgentsVille** serves as a controlled environment for experimenting with agentic workflows and itinerary generation.

---

## Project Goal

The objective was to design an AI assistant capable of:

1. Understanding traveler preferences and constraints.
2. Generating detailed day-by-day travel itineraries.
3. Producing structured outputs that conform to predefined schemas.
4. Revising plans based on additional user requests.
5. Using external tools during the reasoning process.
6. Evaluating itinerary quality before final delivery.

Rather than generating a simple block of text, the system demonstrates how an LLM can participate in a larger decision-making workflow.

---

## System Architecture

### Stage 1 — Expert Planner

The first agent acts as an expert travel planner.

Given:

* Destination information
* Travel dates
* Budget constraints
* Traveler interests
* Weather conditions
* Available activities

the LLM generates a complete itinerary as a validated JSON object.

The output conforms to a predefined Pydantic schema, ensuring predictable downstream processing.

```text
User Preferences
        │
        ▼
Travel Planning Agent
        │
        ▼
Structured TravelPlan JSON
```

---

### Stage 2 — Resourceful Travel Assistant

The second agent revises and improves itineraries.

This agent follows a ReAct-style workflow:

```text
THINK
  ↓
ACT
  ↓
OBSERVE
  ↓
THINK
  ↓
FINAL ANSWER
```

The assistant can:

* Analyze user modification requests
* Call available tools
* Retrieve activity information
* Evaluate itinerary quality
* Revise plans dynamically

This creates a more realistic AI workflow where reasoning and external information retrieval are combined.

---

## Key Components

### Prompt Engineering

Several system prompts were designed to guide:

* Itinerary generation
* Weather compatibility evaluation
* Tool selection
* Agent reasoning
* Itinerary revision

Particular attention was given to obtaining:

* Detailed outputs
* Consistent formatting
* Structured JSON responses
* Reliable tool invocation

---

### Structured Outputs

Pydantic models were used to define:

* Traveler information
* Vacation constraints
* Travel plans
* Daily itinerary structures

This approach improves robustness by validating AI outputs before further processing.

---

### ReAct Agent Design

The itinerary revision agent was implemented using the ReAct paradigm.

The agent explicitly cycles through:

1. Thinking about the problem.
2. Selecting an action.
3. Calling a tool.
4. Observing the result.
5. Continuing reasoning.

This mirrors the architecture used by many modern agentic AI systems.

---

### Tool Use

The system includes tools that allow the agent to access external information during planning.

Example capabilities include:

* Retrieving activities by date
* Evaluating itinerary quality
* Supporting itinerary revisions

The project demonstrates how tool descriptions influence LLM decision-making and tool selection.

---

## Skills Demonstrated

### AI Engineering

* Prompt Engineering
* Agent Workflow Design
* Structured Output Generation
* Tool Calling
* ReAct Agents

### Python

* Pydantic Models
* JSON Validation
* Workflow Orchestration
* API-style Tool Design

### LLM Systems

* Multi-Step Reasoning
* Planning Systems
* Evaluation Pipelines
* Context Management

---

## Key Learnings

This project highlighted several important realities of agentic system development:

* Prompt design strongly influences planning quality.
* Structured outputs dramatically improve reliability.
* Tool descriptions significantly affect agent behavior.
* ReAct workflows provide a practical framework for iterative reasoning.
* Validation layers are essential when integrating LLM outputs into larger systems.

These lessons transfer directly to more advanced agent architectures used in production environments.

---

## Possible Extensions

Future improvements could include:

* Real-world travel APIs
* Retrieval-Augmented Generation (RAG)
* Budget optimization algorithms
* Multi-agent planning systems
* Preference memory across conversations
* Interactive itinerary negotiation
* Automated itinerary scoring

---

## Repository Context

This project is part of my **Agentic AI Early Projects Portfolio**, documenting my exploration of practical AI agent architectures, workflow orchestration, and decision-support systems.

While educational in origin, the project provided hands-on experience with several concepts that underpin modern AI assistants and agentic applications.

---

## Author

**S. Palis**

AI Systems • Applied AI Education • Computational Research

Exploring agentic workflows, governed AI systems, scientific discovery tools, and human-centered AI design.
