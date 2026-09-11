ITINERARY_AGENT_PROMPT = """
Create a complete travel itinerary.

User Query:
{user_query}

Trip Constraints:
{trip_constraints}

Flight Results:
{flight_results}

Hotel Results:
{hotel_results}

Weather Results: 
{weather_results}

Budget Results:
{budget_results}


Make the itinerary practical, budget-aware, and easy to follow.
Create a clear draft that is ready for human review.
"""