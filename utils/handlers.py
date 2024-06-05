import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from utils.embedding import vector_embedding
import time
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

message_history = ChatMessageHistory()



# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")

# Initialize memory outside the function to maintain state across calls
memory = ConversationBufferMemory(memory_key="chat_history")

def handle_text_input(groq_api_key, prompt_text, vectors):
    
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")
    if vectors:
        retriever = vectors.as_retriever()


        retriever_tool = create_retriever_tool(
        retriever,
        "doc/pdf/txt Search",
        "get extra or searching for information in csv or pdf or txt, you must use this tool!",
    )
        tools = [retriever_tool]
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    else:
        tools =[]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
    result = agent_with_chat_history.invoke(
    {"input":prompt_text },
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    config={"configurable": {"session_id": "<foo>"}},
)
    return result['output']

def prepare_vectors(path, fireworks_key):
    os.environ['FIREWORKS_API_KEY'] = fireworks_key
    vectors = vector_embedding(path)
    return vectors
