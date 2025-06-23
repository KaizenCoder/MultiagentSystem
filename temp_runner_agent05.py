import asyncio
from agents.agent_05_maitre_tests_validation import Agent05MaitreTestsValidation
from core.agent_factory_architecture import Task
import logging

# Configure logging to see output
logging.basicConfig(level=logging.INFO)

async def main():
    print("--- Running Agent 05 ---")
    try:
        agent = Agent05MaitreTestsValidation()
        
        await agent.startup()
        
        # Create a dummy task
        task = Task(id="test_validation_task", type="smoke_test", params={"test_suite": "smoke"})
        
        result = await agent.execute_task(task)
        
        print(f"Agent 05 Result: {result}")
        
        await agent.shutdown()

    except Exception as e:
        print(f"Error running Agent 05: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 