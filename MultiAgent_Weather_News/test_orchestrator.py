from agents.orchestrator import Orchestrator

orchestrator = Orchestrator()

queries = [
    "What's the weather in Berlin?",
    "Latest news headlines",
    "Weather and news in London",
    "Tell me something"
]

for q in queries:
    print("USER:", q)
    print("ASSISTANT:")
    print(orchestrator.handle(q))
    print("-" * 40)
