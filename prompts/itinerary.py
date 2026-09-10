ITINERARY_AGENT_PROMPT = """
Create a complete travel itinerary.

User Query:
{user_query}

Flight Results:
{flight_results}

Hotel Results:
{hotel_results}

Make the itinerary practical, budget-aware, and easy to follow.
"""