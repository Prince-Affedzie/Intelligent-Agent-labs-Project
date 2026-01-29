from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
import asyncio
from datetime import datetime
from environment.disaster_environment import DisasterEnvironment

class SensorAgent(Agent):
    class SenseEnvironment(PeriodicBehaviour):
        async def run(self):
            self.agent.environment.update()
            severity = self.agent.environment.get_state()

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] Disaster detected | Severity: {severity}"

            print(log_message)
            with open("event_logs.txt", "a") as log_file:
                log_file.write(log_message + "\n")

    async def setup(self):
        print("SensorAgent started and monitoring environment...")
        self.environment = DisasterEnvironment()
        self.add_behaviour(self.SenseEnvironment(period=5))

async def main():
    agent = SensorAgent(
         "oheneba@xmpp.jp",
         "Prince5As//2021"
    )
    await agent.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
