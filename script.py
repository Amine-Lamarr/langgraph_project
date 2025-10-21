# %%
from langchain_openai import ChatOpenAI
from typing import List , TypedDict , Literal
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from web_operations import weather_call, Adhan_call, wikipedia_call

# %%
model_name = "openai/gpt-4o-mini"
api_key = os.getenv("API_KEY")
llm = ChatOpenAI(
    model=model_name, 
    openai_api_base = "https://openrouter.ai/api/v1", 
    openai_api_key = api_key, 
    temperature = 0.7
)


# %%
class Messages(TypedDict):
    role : Literal["weather", "Adhan", "Search"]
    content : str

class State(TypedDict):
    messages : List[Messages]

# %%
def Weather(state: State):
    """this node returns the weather info of a city"""
    last_message = state["messages"][-1]
    question = last_message["content"]
    llm_city = [
        SystemMessage(content="based on the user's question, extract the city of the user wants its weather info, return only the city like : Moscow"), 
        HumanMessage(content=question)
    ]
    city = llm.invoke(llm_city).content.strip()
    weather_info = weather_call(city)
    llm_prompt = [
        SystemMessage(content="you're an AI assistant, help the user get the weather info based on the weather api"),
        HumanMessage(content=question),
        SystemMessage(content=f"api weather results : {weather_info}")
    ]
    response = llm.invoke(llm_prompt).content
    state["messages"].append({
        "role": "Weather", 
        "content": response
    })
    # print(state["messages"][-1]["content"])
    return state

# %% [markdown]
# ***The States***

# %%
def Adhan(state: State) -> State:
    """this node returns the prayer time of a given city and country"""
    last_msg = state["messages"][-1]
    question = last_msg["content"]
    city_prompt = [
        SystemMessage(content="you're an AI assistant, your job is just to return the city that the user mention in his text, return only the city with no additional text. just like : 'Madrid' or 'Marrakech', don't add any additional texts"),
        HumanMessage(content=question)
    ]
    city = llm.invoke(city_prompt).content.strip()
    country_prompt = [
        SystemMessage(content="you're an AI assistant, your job is just to return the country that the user mention in his text or from the city mentioned, return only the country with no additional text. just like : 'Germany' or 'Morocco', don't add any additional texts"),
        HumanMessage(content=question)
    ]
    country = llm.invoke(country_prompt).content.strip()
    results = Adhan_call(city=city , country=country)
    llm_prompt = [
        SystemMessage(content="you're an AI assistant, your job is to give the user a professionel answer of prayers time based on the Adhan api results"),
        HumanMessage(content=question),
        SystemMessage(content=f"the api results : {results}")
    ]
    response = llm.invoke(llm_prompt).content
    state["messages"].append({
        "role":"Adhan", 
        "content": response
    })
    # print(state["messages"][-1]["content"])
    return state

# %%


# %%
def wikipedia(state: State) -> State:
    last_msg = state["messages"][-1]
    qst = last_msg["content"]
    results = wikipedia_call(qst)
    if not isinstance(results , str):
        results = str(results)
    llm_prompt = [
        SystemMessage(content=f"""
            The user asked about a topic and you have the raw results from Wikipedia. 
            Your job is to:
            1. Summarize and organize the information clearly.
            2. Write it in a professional, easy-to-read style.
            3. Merge and enrich the response naturally with the Wikipedia content.
            4. Avoid copying text verbatim; make it coherent and concise.                      
            wikipedia results : {results}
            """),
    ]
    response = llm.invoke(llm_prompt).content
    state["messages"].append({
        "role":"Search",
        "content": response
    })
    # print(state["messages"][-1]["content"])
    return state

# %%
def decider(state: State):
    last_msg = state['messages'][-1]
    question = last_msg["content"]
    structured_llm = llm.with_structured_output(Messages)
    prompt = [
        SystemMessage(content="Identify if the user's question is about Weather, Adhan, or general Search. Return only the role value."),
        HumanMessage(content=question)
    ]
    output = structured_llm.invoke(prompt) 
    field = output.get("role", "Search") 

    if field.lower() == "weather":
        return {"next": "weather_node"}
    elif field.lower() == "adhan":
        return {"next": "adhan_node"}      
    else:
        return {"next": "wikipedia_node"}  

# %%
from langgraph.graph import StateGraph, END, START
graph_builder = StateGraph(State) 
graph_builder.add_node("adhan_node", Adhan)
graph_builder.add_node('wikipedia_node', wikipedia)
graph_builder.add_node('weather_node', Weather)
graph_builder.add_node('decider_node', decider)

graph_builder.add_edge(START, "decider_node")

graph_builder.add_conditional_edges(
    "decider_node", 
    {
        "weather": Weather,      
        "adhan": Adhan,          
        "search": wikipedia      
    }
)
graph_builder.add_edge("weather_node", END)
graph_builder.add_edge("adhan_node", END)
graph_builder.add_edge("wikipedia_node", END)

graph = graph_builder.compile()

# %%
# from IPython.display import display, Image
# display(Image(graph.get_graph().draw_mermaid_png()))
# display(Image(filename="mermaid.png"))

# %%
#

# %%
import streamlit as st

st.set_page_config(page_title="LangGraph AI Chat", page_icon="🤖")
st.title("🤖 amine's bot ")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_input" not in st.session_state:
    st.session_state.last_input = ""

user_input = st.chat_input("Ask AI something...")

if user_input and user_input != st.session_state.last_input:
    st.session_state.last_input = user_input
    
    if user_input.lower() == "exit":
        st.session_state.messages = []
        st.session_state.last_input = ""
        st.rerun()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get SINGLE AI response
    with st.spinner("Thinking..."):
        try:
            # Create fresh state for each request
            temp_state = {"messages": [{"role": "user", "content": user_input}]}
            resp_state = graph.invoke(temp_state)
            ai_response = resp_state["messages"][-1]["content"]
            
            # Add only ONE AI response
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error."})
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
with st.sidebar:
    st.header("Debug Info")
    if st.session_state.messages:
        last_msg = st.session_state.messages[-1]
        if last_msg["role"] == "user":
            st.write(f"Last user input: {last_msg['content']}")