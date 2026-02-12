from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, CyclicBehaviour
from spade.message import Message
from datetime import datetime
from environment.disaster_environment import DisasterEnvironment


class SensorAgent(Agent):

    # 🔹 Periodically monitor environment and send INFORM
    class SenseEnvironment(PeriodicBehaviour):
        async def run(self):
            self.agent.environment.update()
            state = self.agent.environment.get_state()

            disaster_type = state["type"]
            severity = state["severity"]

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_message = (
                f"[{timestamp}] Disaster detected | "
                f"Type: {disaster_type} | Severity: {severity}"
            )

            print(log_message)

            # Create INFORM message
            msg = Message(to="rescueagent@xmpp.jp")
            msg.set_metadata("performative", "inform")
            msg.body = f"{disaster_type},{severity}"

            await self.send(msg)
            print("SensorAgent sent INFORM to RescueAgent.\n")


    # 🔹 Receive REQUEST confirmation from RescueAgent
    class ReceiveResponse(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                performative = msg.get_metadata("performative")

                if performative == "request":
                    print("SensorAgent received REQUEST from RescueAgent.")
                    print(f"Message content: {msg.body}\n")

                else:
                    print(f"SensorAgent received unknown performative: {performative}")


    async def setup(self):
        print("SensorAgent started...")

        self.environment = DisasterEnvironment()

        self.add_behaviour(self.SenseEnvironment(period=5))
        self.add_behaviour(self.ReceiveResponse())
