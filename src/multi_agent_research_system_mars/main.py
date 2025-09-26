#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv
from multi_agent_research_system_mars.crew import MultiAgentResearchSystemMarsCrew

# Load environment variables
config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.env')
load_dotenv(config_path)

def run():
    """
    Run the crew with interactive input.
    """
    print("🚀 Welcome to MARS - Multi-Agent Research System")
    print("=" * 50)
    
    # Get user inputs
    topic = input("\n📝 Enter your research topic: ").strip()
    if not topic:
        print("❌ Research topic is required!")
        return
    
    recipient_email = input("📧 Enter recipient email address: ").strip()
    if not recipient_email:
        print("❌ Recipient email is required!")
        return
    
    print(f"\n✅ Starting research on: {topic}")
    print(f"📬 Results will be sent to: {recipient_email}")
    print("\n🔄 Research is now running autonomously...")
    print("This may take several minutes. Please wait...")
    
    inputs = {
        'topic': topic,
        'recipient_email': recipient_email
    }
    
    try:
        MultiAgentResearchSystemMarsCrew().crew().kickoff(inputs=inputs)
        print(f"\n✅ Research completed successfully!")
        print(f"📧 Results have been sent to {recipient_email}")
    except Exception as e:
        print(f"\n❌ Error during research: {str(e)}")

def run_with_params(topic, recipient_email):
    """
    Run the crew with provided parameters (for web interface).
    """
    inputs = {
        'topic': topic,
        'recipient_email': recipient_email
    }
    MultiAgentResearchSystemMarsCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'topic': 'AI in healthcare',
        'recipient_email': 'test@example.com'
    }
    try:
        MultiAgentResearchSystemMarsCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MultiAgentResearchSystemMarsCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'topic': 'AI in healthcare',
        'recipient_email': 'test@example.com'
    }
    try:
        MultiAgentResearchSystemMarsCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
