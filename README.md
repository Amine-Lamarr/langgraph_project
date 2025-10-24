<h1 align="center">🤖 LangGraph AI Chatbot</h1>

<p align="center">
  <b>An intelligent multi-purpose AI assistant built using LangGraph, LangChain, and OpenRouter GPT models.</b><br>
  <i>Developed by <a href="https://github.com/aminecanfly">Amine</a></i>
</p>

---

<h2>📖 Overview</h2>

<p>
  The <b>LangGraph AI Chatbot</b> is a smart conversational assistant that connects multiple APIs and reasoning flows 
  using <b>LangGraph</b>’s state-based architecture.  
  It can:
</p>

<ul>
  <li>🌦️ Get <b>real-time weather</b> information for any city using the <a href="https://openweathermap.org/api">OpenWeather API</a>.</li>
  <li>🕌 Retrieve <b>Adhan (prayer) times</b> for any city and country using the <a href="https://aladhan.com/prayer-times-api">Aladhan API</a>.</li>
  <li>📚 Search and summarize topics from <b>Wikipedia</b> dynamically.</li>
</ul>

<p>
  The system decides automatically which node to use (<code>Weather</code>, <code>Adhan</code>, or <code>Wikipedia</code>)
  based on the user’s question — powered by an <b>LLM decision layer</b>.
</p>

---

<h2>🧩 Architecture</h2>

<ul>
  <li><b>LangGraph</b>: Handles the logic flow and conditional graph execution.</li>
  <li><b>LangChain</b>: Manages the LLM interface and conversation schema.</li>
  <li><b>OpenRouter + GPT-4o-mini</b>: Provides the intelligence layer.</li>
  <li><b>Streamlit</b>: Web interface for user interaction.</li>
  <li><b>External APIs</b>: OpenWeather, Aladhan, Wikipedia.</li>
</ul>

<h2>🧠 How It Works</h2>

<ol>
  <li>User asks a question in the chat input.</li>
  <li>The <b>decider node</b> uses an LLM to determine the question type: <i>weather, adhan, or search</i>.</li>
  <li>The flow moves to the appropriate node that calls the correct API.</li>
  <li>Results are summarized by the LLM and displayed in the Streamlit chat UI.</li>
</ol>

<h2>🖼️ Example Queries</h2>

<ul>
  <li>“What’s the weather like in Paris?”</li>
  <li>“Give me today’s prayer times in Casablanca, Morocco.”</li>
  <li>“Tell me something about Albert Einstein.”</li>
</ul>

---

<h2>🚀 Technologies Used</h2>

<ul>
  <li>Python</li>
  <li>LangChain & LangGraph</li>
  <li>OpenRouter API (GPT-4o-mini)</li>
  <li>Streamlit</li>
  <li>External APIs (OpenWeather, Aladhan, Wikipedia)</li>
</ul>

---

<h2>💡 Future Improvements</h2>

<ul>
  <li>🧠 Add memory for long-term context.</li>
  <li>🗺️ Extend with more APIs (translation, news, etc.).</li>
  <li>🎙️ Voice input/output support.</li>
</ul>

---

<h2>👨‍💻 Author</h2>

<p align="center">
  Built with ❤️ by <b>Amine</b> — an 18-year-old AI Engineer from Morocco 🇲🇦<br>
  <a href="https://github.com/aminecanfly">GitHub</a> • <a href="https://www.linkedin.com">LinkedIn</a>
</p>
