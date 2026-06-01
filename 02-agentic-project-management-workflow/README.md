# 🤖 AI-Powered Agentic Workflow for Project Management

### Multi-Agent Project Planning, Routing, Evaluation, and Workflow Orchestration

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT_Powered-green?style=for-the-badge)
![AI Agents](https://img.shields.io/badge/AI_Agents-Agent_Architecture-purple?style=for-the-badge)
![Multi-Agent](https://img.shields.io/badge/Multi--Agent-Workflow_Orchestration-red?style=for-the-badge)
![Embeddings](https://img.shields.io/badge/Embeddings-Semantic_Routing-orange?style=for-the-badge)
![Evaluation](https://img.shields.io/badge/LLM-Evaluation_Loops-teal?style=for-the-badge)

---

# Agentic AI Early Projects Portfolio

### Project 2 of 4

---

## Overview

This project explores the design and implementation of a reusable multi-agent workflow framework for technical project management.

Developed as part of the Udacity Agentic AI Nanodegree, the project demonstrates how specialized AI agents can collaborate to transform a high-level product specification into a structured development plan containing:

* User stories
* Product features
* Engineering tasks

The system simulates a project management organization composed of specialized AI teams, coordinated through routing, planning, evaluation, and workflow orchestration mechanisms.

---

## Project Goal

The objective was to build a scalable AI workflow capable of assisting Technical Project Managers (TPMs) by transforming product ideas into actionable development plans.

The workflow must:

1. Analyze a project objective.
2. Decompose the objective into manageable tasks.
3. Route tasks to specialized agents.
4. Generate project artifacts.
5. Evaluate output quality.
6. Refine responses when necessary.
7. Produce a structured final project plan.

The pilot use case focuses on a fictional product called:

**Email Router**

but the architecture was intentionally designed as a reusable workflow framework applicable to future projects.

---

## System Architecture

The project is divided into two major components:

### Phase 1 — Agentic Toolkit

A reusable library of AI agent classes was implemented.

The toolkit includes:

* DirectPromptAgent
* AugmentedPromptAgent
* KnowledgeAugmentedPromptAgent
* RAGKnowledgePromptAgent
* EvaluationAgent
* RoutingAgent
* ActionPlanningAgent

Each agent encapsulates a distinct reasoning or orchestration capability and can be reused in larger workflows.

---

### Phase 2 — Project Management Workflow

The second phase combines multiple agents into a coordinated workflow capable of managing technical planning activities.

```text
High-Level Project Request
            │
            ▼
   Action Planning Agent
            │
            ▼
      Workflow Steps
            │
            ▼
       Routing Agent
            │
 ┌──────────┼──────────┐
 ▼          ▼          ▼
Product   Program   Development
Manager   Manager   Engineer
 Agent     Agent      Agent
 │          │          │
 ▼          ▼          ▼
Evaluation Evaluation Evaluation
 Agent      Agent      Agent
 └──────────┼──────────┘
            ▼
     Final Project Plan
```

---

## Key Agent Types

### Action Planning Agent

Responsible for breaking complex objectives into smaller actionable steps.

This agent serves as the workflow coordinator's initial planning mechanism.

Example output:

```text
1. Define user personas
2. Create user stories
3. Identify product features
4. Define engineering requirements
5. Generate implementation tasks
```

---

### Routing Agent

The routing agent determines which specialist should handle a given task.

Routing decisions are made using semantic similarity between:

* task descriptions
* agent capabilities

Embeddings are used to identify the most appropriate destination for each workflow step.

---

### Knowledge-Augmented Agents

Three specialist roles were simulated:

#### Product Manager

Responsible for:

* User personas
* User stories
* Product requirements

---

#### Program Manager

Responsible for:

* Product features
* Functional specifications
* Capability definition

---

#### Development Engineer

Responsible for:

* Engineering tasks
* Acceptance criteria
* Implementation planning

---

### Evaluation Agents

Each specialist agent is paired with an evaluator.

The evaluator:

1. Reviews generated output.
2. Compares it against predefined criteria.
3. Produces correction instructions.
4. Requests revisions when necessary.

This creates an iterative quality-control loop before results are accepted.

---

## Workflow Example

For the Email Router pilot project, the system:

1. Receives a product specification.
2. Generates workflow steps.
3. Routes each step to an expert team.
4. Evaluates outputs.
5. Produces:

### User Stories

```text
As a customer support agent,
I want incoming emails automatically categorized
so that I can respond more efficiently.
```

### Product Features

```text
Feature Name: Intelligent Email Classification

Description:
Automatically classify incoming emails based on content.

User Benefit:
Reduced manual triage workload.
```

### Engineering Tasks

```text
Task ID: ENG-001

Task Title:
Implement Email Classification Service

Acceptance Criteria:
Classification accuracy exceeds defined threshold.
```

---

## AI Engineering Concepts Demonstrated

### Agent Design

* Prompt-based agents
* Persona-driven agents
* Knowledge-augmented agents

### Workflow Orchestration

* Task decomposition
* Agent coordination
* Multi-stage pipelines

### Multi-Agent Systems

* Specialized agent teams
* Agent routing
* Collaborative workflows

### Quality Assurance

* Evaluation agents
* Iterative refinement
* Automated review loops

### Semantic Search

* Text embeddings
* Similarity scoring
* Intelligent routing

---

## Skills Demonstrated

### AI Systems

* Agent Architecture
* Workflow Engineering
* LLM Orchestration
* Multi-Agent Design

### Python

* Object-Oriented Design
* Agent Framework Development
* Modular Architecture

### Large Language Models

* Prompt Engineering
* Evaluation Pipelines
* Knowledge Augmentation

---

## Key Learnings

This project provided practical experience in designing AI systems composed of multiple cooperating agents.

Important observations included:

* Specialized agents often outperform general-purpose agents for structured tasks.
* Routing mechanisms become increasingly important as workflows grow in complexity.
* Evaluation loops significantly improve output consistency.
* Agent orchestration resembles traditional software architecture more than standalone prompting.
* Multi-agent systems require careful management of responsibilities and information flow.

Many concepts explored in this project appear in modern enterprise AI systems, agent frameworks, and autonomous workflow platforms.

---

## Potential Extensions

Future improvements could include:

* Real-world vector databases
* Retrieval-Augmented Generation (RAG)
* Human-in-the-loop approval stages
* Dynamic agent creation
* Workflow monitoring dashboards
* Cost-aware routing
* Multi-step autonomous execution

---

## Repository Context

This project is part of my **Agentic AI Early Projects Portfolio** and documents my exploration of agent orchestration, workflow automation, evaluation pipelines, and collaborative AI systems.

It represents an early investigation into many of the architectural concepts that underpin modern agentic AI platforms and multi-agent decision systems.

---

## Author

**S. Palis**

AI Systems • Applied AI Education • Computational Research

Exploring agentic workflows, multi-agent systems, scientific discovery tools, and human-centered AI architectures.
