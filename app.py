import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import asyncio
from pydantic_ai import Agent
import ollama

# Global CSV Data
csv_data = None

# Initialize the AI Agent
agent = Agent()





async def query_llm(prompt):
    try:
        print("Query sent to Agent:", prompt)
        response = await agent.run(prompt, model="llama3:latest")  
        print("Response from Agent:", response)
        return str(response)
    except Exception as e:
        print("Error querying Agent:", str(e))
        return f"Error processing query: {str(e)}"



def upload_csv(file_path):
    """Handles CSV upload and validation."""
    global csv_data
    try:
        csv_data = pd.read_csv(file_path)
        return f"CSV '{file_path}' uploaded! {csv_data.shape[0]} rows, {csv_data.shape[1]} columns."
    except Exception as e:
        return f"Error loading CSV: {str(e)}"

def process_query(user_query):
    """Handles user queries about CSV data."""
    global csv_data
    if csv_data is None:
        return "Please upload a CSV file first."

    # Provide column names for context
    query_with_context = f"CSV Columns: {', '.join(csv_data.columns)}. User Question: {user_query}"

    # Run the LLM in an async-safe way
    response = asyncio.run(query_llm(query_with_context))
    return response

def plot_graph(x_column, y_column):
    """Generates a scatter plot for the selected columns."""
    global csv_data
    if csv_data is None:
        return "Please upload a CSV file first."

    if x_column not in csv_data.columns or y_column not in csv_data.columns:
        return f"Invalid column selection: {x_column}, {y_column}"

    plt.figure(figsize=(6, 4))
    plt.scatter(csv_data[x_column], csv_data[y_column], alpha=0.5)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{x_column} vs {y_column}")

    # Save and return the plot
    plt.savefig("plot.png")
    return "plot.png"

# Gradio Interface
with gr.Blocks() as app:
    gr.Markdown("# CSV Question Answering & Visualization")

    with gr.Row():
        csv_upload = gr.File(label="Upload CSV File", type="filepath")
        upload_btn = gr.Button("Upload")
        upload_output = gr.Textbox(label="Upload Status")

    with gr.Row():
        user_input = gr.Textbox(label="Ask a Question")
        query_btn = gr.Button("Get Answer")
        query_output = gr.Textbox(label="AI Answer")

    with gr.Row():
        x_column = gr.Textbox(label="X-Axis Column")
        y_column = gr.Textbox(label="Y-Axis Column")
        plot_btn = gr.Button("Plot Graph")
        plot_output = gr.Image(label="Graph")

    upload_btn.click(upload_csv, inputs=[csv_upload], outputs=[upload_output])
    query_btn.click(process_query, inputs=[user_input], outputs=[query_output])
    plot_btn.click(plot_graph, inputs=[x_column, y_column], outputs=[plot_output])

# Run the Gradio App
if __name__ == "__main__":
    app.launch()
