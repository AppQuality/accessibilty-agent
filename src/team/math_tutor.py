from agents import Agent

math_tutor = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    model="gpt-4o-mini",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)