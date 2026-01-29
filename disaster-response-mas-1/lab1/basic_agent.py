from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio

class HelloAgent(Agent):
    class HelloBehaviour(CyclicBehaviour):
        async def run(self):
            print("Hello! Agent is running...")
            await asyncio.sleep(5)

    async def setup(self):
        print("Agent starting...")
        self.add_behaviour(self.HelloBehaviour())

async def main():
    agent = HelloAgent(
        "oheneba@xmpp.jp",
        "Prince5As//2021"
    )
    await agent.start()

    print("Agent started successfully.")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await agent.stop()
        print("Agent stopped.")

if __name__ == "__main__":
    asyncio.run(main())
