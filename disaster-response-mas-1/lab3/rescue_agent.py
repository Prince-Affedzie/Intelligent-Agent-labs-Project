from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State, CyclicBehaviour
from spade.template import Template
from spade.message import Message
import asyncio


# -------- FSM STATES -------- #

class IdleState(State):
    async def run(self):
        print("State: IDLE - Waiting for disaster event...")
        await asyncio.sleep(2)
        self.set_next_state("MONITORING")


class MonitoringState(State):
    async def run(self):
        print("State: MONITORING - Checking severity...")
        await asyncio.sleep(2)

        severity = self.agent.current_severity

        if severity == "HIGH":
            self.set_next_state("RESPONDING")
        else:
            self.set_next_state("IDLE")


class RespondingState(State):
    async def run(self):
        print("State: RESPONDING - Executing rescue operation!")

        # Send REQUEST confirmation back to SensorAgent
        msg = Message(to=self.agent.last_sender)
        msg.set_metadata("performative", "request")
        msg.body = "Rescue operation deployed."

        await self.send(msg)
        print("RescueAgent sent REQUEST confirmation to SensorAgent.")

        await asyncio.sleep(3)
        self.set_next_state("COMPLETED")


class CompletedState(State):
    async def run(self):
        print("State: COMPLETED - Rescue mission finished.")
        await asyncio.sleep(2)

        # Reset severity after mission
        self.agent.current_severity = "LOW"
        self.set_next_state("IDLE")


# -------- MESSAGE RECEIVER -------- #

class ReceiveDisaster(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=5)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "inform":
                disaster_type, severity = msg.body.split(",")

                print(f"\nReceived INFORM from SensorAgent:")
                print(f"Disaster: {disaster_type} | Severity: {severity}")

                # Store severity for FSM decision
                self.agent.current_severity = severity

                # Store sender so FSM can reply
                self.agent.last_sender = str(msg.sender)

            else:
                print(f"Unknown performative received: {performative}")


# -------- AGENT -------- #

class RescueAgent(Agent):
    async def setup(self):
        print("RescueAgent starting...")

        self.current_severity = "LOW"
        self.last_sender = None

        # Template to filter INFORM messages only
        template = Template()
        template.set_metadata("performative", "inform")

        self.add_behaviour(ReceiveDisaster(), template)

        # FSM Behaviour
        fsm = FSMBehaviour()
        fsm.add_state("IDLE", IdleState(), initial=True)
        fsm.add_state("MONITORING", MonitoringState())
        fsm.add_state("RESPONDING", RespondingState())
        fsm.add_state("COMPLETED", CompletedState())

        fsm.add_transition("IDLE", "MONITORING")
        fsm.add_transition("MONITORING", "RESPONDING")
        fsm.add_transition("MONITORING", "IDLE")
        fsm.add_transition("RESPONDING", "COMPLETED")
        fsm.add_transition("COMPLETED", "IDLE")

        self.add_behaviour(fsm)


async def main():
    agent = RescueAgent(
        "rescueagent@xmpp.jp",
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
