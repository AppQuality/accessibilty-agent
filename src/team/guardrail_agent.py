from agents import Agent, GuardrailFunctionOutput, Runner
from .base import HomeworkOutput

guardrail = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    # Meglio usare il modello più cheap per verificare se la richiesta è ok
    model="gpt-4o-mini",
    output_type=HomeworkOutput,
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )
