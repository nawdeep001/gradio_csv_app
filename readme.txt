1. Install necessary dependencies:

pip install gradio pandas matplotlib seaborn ollama pydantic

2. Install ollama:
    For Macbook M1 :
        brew install ollama
    Then, download the recommended Llama 3.1 8B model (or a smaller version for performance).
    I've downloaded Llama3:latest

After that you have to verify whether ollama is properly installed or not. For me it is showing following thing:

    ollama list
NAME             ID              SIZE      MODIFIED    
llama3:latest    365c0bd3c000    4.7 GB    2 hours ago    
nawdeepkumar@NAWDEEPs-MacBook-2 ~ % ollama run llama3 "Hello, what is your name?"
Nice to meet you! I don't have a personal name, as I'm just an AI designed 
to assist and communicate with humans. You can think of me as a friendly 
chatbot or conversational partner! I'm here to help answer questions, 
provide information, and engage in fun conversations. What's on your mind?



3. Ensure Pydantic AI is installed.
    pip install pydantic-ai

4. Now, create a Python script (app.py) with the implementation and run.

5. You can run the a.py also to show clean csv file uploaded message.


