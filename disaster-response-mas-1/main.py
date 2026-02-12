import asyncio
from agents.sensor_agent import SensorAgent
from agents.rescue_agent import RescueAgent


async def main():
    print("Starting Disaster Response Multi-Agent System...\n")

    # Create agents
    sensor_agent = SensorAgent(
        "oheneba@xmpp.jp",
        "Prince5As//2021"
    )

    rescue_agent = RescueAgent(
        "rescueagent@xmpp.jp",
        "Prince5As//2021"
    )

    # Start agents
    await sensor_agent.start()
    await rescue_agent.start()

    print("All agents started successfully.\n")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down agents...")
        await sensor_agent.stop()
        await rescue_agent.stop()
        print("System shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
