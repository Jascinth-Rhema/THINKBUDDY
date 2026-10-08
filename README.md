# ThinkBuddy

ThinkBuddy is a prompt engineering workspace built with Streamlit. It lets you send the same question to a large language model using different prompting techniques and compare the answers side by side.

## Features

- Five prompting techniques: Zero-Shot, One-Shot, Few-Shot, Chain of Thought (CoT) and Tree of Thought (ToT)
- Single technique mode and compare mode (view several techniques side by side)
- Temperature slider to control how precise or creative the answers are
- Answer length control (Short, Medium, Detailed, Very Detailed)
- Option to view the exact prompt sent to the model
- Response time shown for every answer
- Math formulas rendered properly in answers
- Clean, animated interface

## Prompting Techniques

| Technique | Description |
|-----------|-------------|
| Zero-Shot | No examples. The question is asked directly. |
| One-Shot | One example is given before the task. |
| Few-Shot | Several examples guide the model. |
| Chain of Thought (CoT) | The model reasons step by step before answering. |
| Tree of Thought (ToT) | The model explores multiple reasoning branches, scores them and picks the best. |

## Project Structure

```
thinkbuddy/
  app.py                # Streamlit user interface
  llm.py                # Connects to the language model API
  prompt_templates.py   # Prompt builders for each technique
  requirements.txt      # Python dependencies
  .gitignore            # Keeps secret files out of Git
  .env                  # Your API key (local only, never upload)
```

## Requirements

- Python 3.9 or higher
- A free Groq API key (https://console.groq.com/keys)

## Local Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/thinkbuddy.git
   cd thinkbuddy
   ```

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a file named `.env` in the project folder and add your key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Run the app:
   ```
   streamlit run app.py
   ```

5. Open the link shown in the terminal, usually http://localhost:8501.

## Configuration

These optional values can be added to the `.env` file:

| Variable | Purpose | Default |
|----------|---------|---------|
| GROQ_API_KEY | Groq API key | none (required) |
| GROQ_MODEL | Groq model name | openai/gpt-oss-120b |
| HF_TOKEN | Hugging Face token (used only if no Groq key is set) | none |
| HF_MODEL | Hugging Face model name | Qwen/Qwen2.5-72B-Instruct |

If the chosen Groq model is not available for your key, the app automatically picks another available model.

## Deploying on Streamlit Community Cloud

1. Push these files to a GitHub repository: `app.py`, `llm.py`, `prompt_templates.py`, `requirements.txt`, `.gitignore`.
2. Do not upload `.env` or any file that contains your key.
3. Go to https://share.streamlit.io and click New app.
4. Select your repository, set the branch to `main` and the main file path to `app.py`.
5. Open Advanced settings and add your key in the Secrets box:
   ```
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
6. Click Deploy.

## How to Use

1. Type a question or task in the text box.
2. Choose Single technique or Compare techniques.
3. Select one or more techniques.
4. Adjust temperature and answer length in the sidebar.
5. Click Generate Response.

Sample questions to try:

- A farmer has 17 sheep. All but 9 run away. How many are left?
- If a bat and a ball cost $1.10 in total and the bat costs $1 more than the ball, how much does the ball cost?
- I have 2 weeks and a small budget. What is the best way to learn Python for a job interview?

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No API key found | Check that `.env` exists in the project folder and contains `GROQ_API_KEY=...`. On Streamlit Cloud, add the key in Secrets. |
| ModuleNotFoundError | Make sure `requirements.txt` is in the main folder of the repository, then reboot the app. |
| Model not found | Remove any `GROQ_MODEL` line from `.env`, or set it to a model available to your key. |
| Changes not showing | Stop Streamlit with Ctrl + C and run it again. |

## Security

- Never put API keys inside `.py` files.
- Never upload `.env` to GitHub.
- If a key is exposed, delete it from the provider dashboard and create a new one.

## Built With

- Streamlit
- Groq API
- python-dotenv

