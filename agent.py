# Before running the sample:
#    pip install --pre azure-ai-projects>=2.0.0b1
#    pip install azure-identity

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

user_endpoint = "https://ai-foundry-sample-3-resource.services.ai.azure.com/api/projects/ai-foundry-sample-3"

project_client = AIProjectClient(
    endpoint=user_endpoint,
    credential=DefaultAzureCredential(),
)

agent_name = "my-first-agent"
model_deployment_name = "gpt-5-mini"

# Creates an agent, bumps the agent version if parameters have changed
agent = project_client.agents.create_version(  
    agent_name=agent_name,
    definition=PromptAgentDefinition(
            model=model_deployment_name,
            instructions="Give the user result into one liner not more than that.",
        ),
)

openai_client = project_client.get_openai_client()
storyname = input("Tell me a one line story ")
# Reference the agent to get a response
response = openai_client.responses.create(
    input=[{"role": "user", "content": storyname}],
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Response output: {response.output_text}")


