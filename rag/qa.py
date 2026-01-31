from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

def get_rag_chain(vector_store):
    """
    Creates a RAG chain given a vector store.
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6}
    )

    system_prompt = ( 
        "You are an assistant for question-answering tasks. " 
        "Answer strictly based on the provided context.\n\n" 
        "Rules:\n" 
        "- If the answer is not present in the context, say 'I cannot answer this based on the provided document.'\n" 
        "- Do NOT mix information across different documents unless explicitly asked.\n" 
        "Context:\n" "{context}" 
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # Define how each retrieved chunk is formatted in the context
    # This ensures the LLM sees the filename ("source") associated with each text block
    document_prompt = PromptTemplate(
        input_variables=["page_content", "source"],
        template="Source: {source}\nContent: {page_content}"
    )

    question_answer_chain = create_stuff_documents_chain(
        llm, 
        prompt,
        document_prompt=document_prompt,
        document_variable_name="context"
    )
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain