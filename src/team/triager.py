from agents import Agent, InputGuardrail
from .math_tutor import math_tutor
from .history_tutor import history_tutor
from .guardrail_agent import homework_guardrail

agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor, math_tutor],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)