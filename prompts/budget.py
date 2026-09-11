BUDGET_AGENT_PROMPT = """
Analyze whether this trip is realistic for the user's budget.

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

Return:
1. Estimated cost categories
2. Budget risk areas
3. Money-saving suggestions
4. Overall feasibility

If exact live prices are unavailable, clearly label estimates as approximate.
"""
