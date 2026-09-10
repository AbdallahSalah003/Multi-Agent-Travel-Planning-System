FINAL_AGENT_PROMPT = """
Generate the final travel response for the user.

User Request:
{user_query}

Flights:
{flight_results}

Hotels:
{hotel_results}

Weather: 
{weather_results}

Itinerary:
{itinerary}

Format the final answer beautifully using these sections:

1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Day-by-Day Itinerary
5. Estimated Budget
6. Final Recommendations

Important:
- Be clear and practical.
- Mention that live flight API may not provide ticket prices if pricing is unavailable.
- Keep the response useful for real travel planning.
"""