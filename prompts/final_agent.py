FINAL_AGENT_PROMPT = """
Generate the final travel response for the user.

Human Review:
{review_instructions}

User Request:
{user_query}

Trip Constraints:
{trip_constraints}

Flights:
{flight_results}

Hotels:
{hotel_results}

Weather: 
{weather_results}

Budget Results:
{budget_results}

Draft Itinerary:
{itinerary}


Format the final answer beautifully using these sections:
1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Weather Information
5. Day-by-Day Itinerary
6. Estimated Budget
7. Final Recommendations

Important:
- Be clear and practical.
- Mention that live flight APIs may not provide ticket prices when pricing is unavailable.
- Include weather-based travel advice.
- Keep the response useful for real travel planning.
- Incorporate the human feedback when revision was requested.
"""