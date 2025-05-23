# filepath: /agent-oai-sdk/agent-oai-sdk/src/main.py
from config.env import config
from agents import Runner, InputGuardrailTripwireTriggered
from team import triager
import asyncio


def load_env():
    if (config):
        print("system loaded...")


async def ask(question: str):
    try:
        result = await Runner.run(triager, question)
        print(result.final_output)

    except InputGuardrailTripwireTriggered as e:
        # Print just the reason/message
        print(e.guardrail_result.output.output_info.reasoning)
        print("refused")

    except Exception as e:
        print(f"Something went wrong: {e}")


async def main():
    # Load environment variables
    load_env()

    await ask("Com'è fatta la bandiera della Turchia?")

    print("🪁 done... ")


if __name__ == "__main__":
    asyncio.run(main())
