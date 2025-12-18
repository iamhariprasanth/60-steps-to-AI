Weather Agent — Interactive AutoGen-style

This script provides an interactive terminal agent that:
- Accepts natural-language weather questions
- Uses the OpenAI LLM (if `OPENAI_API_KEY` is present) to extract a city name
- Uses Open-Meteo geocoding and weather APIs to get current conditions (no API key required)
- Prints current conditions with local date/time

Usage

1. Create and activate your virtual environment (if not already):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies (you already have most from `requirements.txt`):

```bash
pip install -r requirements.txt
# ensure 'openai' and 'httpx' are installed; requirements.txt already includes openai via autogen-ext
```

3. (Optional) Add your OpenAI API key to a `.env` file in the project root:

```
OPENAI_API_KEY=sk-xxxx
```

If you do not provide an OpenAI API key, the script will try a simple heuristic to extract the city.

4. Run the agent:

```bash
python weather_agent.py
```

Then type questions like:
- "What's the weather in New York now?"
- "How is the weather for Tokyo today?"
- "Will it rain in London?"

Press `Ctrl+C` or type `exit` to quit.

Notes
- The script uses Open-Meteo's free APIs for geocoding and current weather (no key required).
- Using the LLM improves city recognition for complex questions.
