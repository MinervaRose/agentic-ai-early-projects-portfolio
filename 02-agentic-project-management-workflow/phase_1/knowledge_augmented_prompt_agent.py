# TODO: 1 - Import the KnowledgeAugmentedPromptAgent class from workflow_agents
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"

# TODO: 2 - Instantiate a KnowledgeAugmentedPromptAgent
knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona,
    knowledge=knowledge
)

# Generate the response using the agent
response = knowledge_agent.respond(prompt)

# TODO: 3 - Write a print statement demonstrating the agent using the provided knowledge
print(response)
print(
    "\nNote: This response intentionally uses the *provided incorrect knowledge* "
    "('The capital of France is London, not Paris') rather than the LLM's real-world knowledge."
)