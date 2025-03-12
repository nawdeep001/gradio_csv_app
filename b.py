import gradio as gr
import pandas as pd
import asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# ✅ Define response model
class CSVResponse(BaseModel):
    answer: str = Field(description="AI-generated response based on the CSV data.")

# ✅ Corrected model selection
csv_agent = Agent(
    model="openai:gpt-4o",
  # ⬅️ Change this based on your available LLM
    result_type=CSVResponse,
    system_prompt="You are an AI assistant that answers questions about CSV files."
)

async def process_query(file, user_question):
    if file is None:
        return "❌ Please upload a CSV file first."

    try:
        df = pd.read_csv(file.name)  
        column_names = ", ".join(df.columns)  
        context = f"CSV Columns: {column_names}. User Question: {user_question}"

        # ✅ Ensure AI receives proper input
        result = await csv_agent.run(context)
        return result.answer  # ✅ Extract AI response

    except Exception as e:
        return f"🚨 Error querying AI: {str(e)}"

# ✅ Gradio does not support async directly, so wrap in `asyncio.run()`
def process_query_wrapper(file, user_question):
    return asyncio.run(process_query(file, user_question))

with gr.Blocks() as app:
    gr.Markdown("# CSV Data AI Assistant 📊🤖")
    
    csv_upload = gr.File(label="Upload CSV File", type="filepath")  
    user_question = gr.Textbox(label="Ask a question about the CSV")
    submit_btn = gr.Button("Ask AI")
    output = gr.Textbox(label="AI Response")

    submit_btn.click(process_query_wrapper, inputs=[csv_upload, user_question], outputs=output)

app.launch()
