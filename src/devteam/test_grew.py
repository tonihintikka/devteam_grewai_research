from devteam.crew import Devteam

def test_crew():
    devteam = Devteam()
    inputs = {
        'topic': 'Agents as a programming team'
    }
    devteam.crew().kickoff(inputs=inputs)
    print("Crew executed successfully.")

if __name__ == "__main__":
    test_crew()