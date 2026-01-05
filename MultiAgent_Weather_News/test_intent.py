from agents.intent_parser import detect_intent

tests = [
    "What's the weather in Paris?",
    "Latest news headlines",
    "Weather and news in London",
    "Hello there"
]

for t in tests:
    print(t, "->", detect_intent(t))
