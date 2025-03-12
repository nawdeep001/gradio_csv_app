import asyncio
from pydantic_ai import Agent

agent = Agent()

async def query_llm(prompt):
    """Queries the LLM asynchronously."""
    try:
        print("Query sent to Agent:", prompt)
        response = await agent.run(prompt, model="llama3:latest")
        print("Response from Agent:", response)
        return str(response)
    except Exception as e:
        print("Error querying Agent:", str(e))
        return f"Error processing query: {str(e)}"

def process_query(user_query, csv_data):
    """Handles user queries about CSV data."""
    if csv_data is None:
        return "Please upload a CSV file first."

    query_with_context = f"CSV Columns: {', '.join(csv_data.columns)}. User Question: {user_query}"
    response = asyncio.run(query_llm(query_with_context))
    return response
