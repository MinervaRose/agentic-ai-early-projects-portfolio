
from workflow_agents.base_agents import RAGKnowledgePromptAgent
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define the persona for the agent
persona = "You are a college professor, your answer always starts with: Dear students,"

# Instantiate the RAGKnowledgePromptAgent
rag_agent = RAGKnowledgePromptAgent(
    openai_api_key=openai_api_key,
    persona=persona,
    chunk_size=200,   # small, but we won't rely on CSV-based methods
    chunk_overlap=50,
)

# Our own short knowledge text about a fictional podcast
knowledge_text = """
Mira is an oceanographer who hosts a podcast called 'Tidal Signals'.
The podcast explores how oceans, climate, and technology intersect in everyday life.
In each episode, Mira interviews scientists, engineers, and community organizers.
They discuss topics such as rising sea levels, underwater acoustics, renewable energy at sea, and marine conservation.
The goal of the show is to help listeners understand how the ocean shapes our future.
"""

# ---- Simple in-memory "RAG" using the agent's embedding & similarity methods ----

# 1) Split the knowledge into smaller chunks (here: by sentences)
sentences = [s.strip() for s in knowledge_text.split(".") if s.strip()]

# 2) Get an embedding for each chunk using the RAG agent
sentence_embeddings = [rag_agent.get_embedding(s) for s in sentences]

# 3) Get an embedding for the user prompt
prompt = "What is the podcast that Mira hosts about?"
prompt_embedding = rag_agent.get_embedding(prompt)

# 4) Use the agent's similarity function to find the most relevant sentence
best_idx = 0
best_score = -1.0
for idx, emb in enumerate(sentence_embeddings):
    score = rag_agent.calculate_similarity(prompt_embedding, emb)
    if score > best_score:
        best_score = score
        best_idx = idx

best_chunk = sentences[best_idx]

# 5) Ask the LLM to answer based only on the best_chunk
client = OpenAI(
    base_url="https://openai.vocareum.com/v1",
    api_key=openai_api_key,
)

messages = [
    {
        "role": "system",
        "content": f"You are {persona}. Use only the provided context to answer.",
    },
    {
        "role": "user",
        "content": (
            f"Context: {best_chunk}\n\n"
            f"Prompt: {prompt}\n\n"
            "Answer based only on this context."
        ),
    },
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0,
)

answer = response.choices[0].message.content

print(f"Prompt: {prompt}")
print("\nRetrieved context chunk:")
print(best_chunk)
print("\nAnswer from RAGKnowledgePromptAgent:")
print(answer)