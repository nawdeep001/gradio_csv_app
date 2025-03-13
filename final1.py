import pandas as pd
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


ollama_model = OpenAIModel(
    model_name='llama3:latest',
    provider=OpenAIProvider(base_url='http://localhost:11434/v1')  # Ensure Ollama API is running
)

# Function to Load and Preprocess CSV
def load_csv(file_path):
    """Loads CSV file into a Pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

# Define Async Search Function
async def search_csv(query, data):
    
    if data is None:
        return "Error: No data available."

    system_prompt = f"""You are an expert in analyzing tabular data.
    Below is a dataset from a CSV file:
    
    {data} #index=False
    
    Answer concisely based on this data. The user's question is: {query}
    Provide only relevant insights without adding unnecessary information."""

    agent = Agent(
        ollama_model,
        system_prompt=system_prompt,
    )

    response = await agent.run(user_prompt=query)
    return response.data

# Define Main Function
async def main():
    file_path = '/Users/nawdeepkumar/gradio_csv_app/Housing.csv'  # Change this to your actual CSV file path
    new_data= load_csv(file_path)
    data=new_data.to_string()

    if data is None:
        print("Failed to load CSV. Exiting.")
        return

    print("\nOllama CSV Query Chatbot - Type 'quit' to exit\n")

    while True:
        query = input("\nEnter your search query (or 'quit' to exit): ")

        if query.lower() == "quit":
            print("Exiting chatbot.")
            break

        response = await search_csv(query, data)
        print("\nResponse:", response)

# Main Function
if __name__ == "__main__":
    asyncio.run(main())
