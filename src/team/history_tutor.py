from agents import Agent

history_tutor = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    model="gpt-4o-mini",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)