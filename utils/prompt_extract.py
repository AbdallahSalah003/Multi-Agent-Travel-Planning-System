from services.llm import instrumented_llm

async def extract_destination(query: str):
    prompt = f"""
    Extract only the destination city or country.

    Query:
    {query}

    Return only destination name.
    """
    llm = instrumented_llm.get_llm()
    response = await llm.ainvoke(prompt)

    return response.content.strip()