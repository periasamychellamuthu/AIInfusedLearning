import json
from clients import getClient, getModel
from tools import detect_filler_words, check_star_structure, score_relevance

client = getClient()
model = getModel()

# 1. The tool "menu" the LLM sees. It only picks WHICH tools to call;
#    we fill in the arguments ourselves (see run_tool) so the LLM can't
#    paraphrase the answer or invent keywords before scoring.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "detect_filler_words",
            "description": "Counts filler words (um, uh, like, basically...) in the candidate's answer.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_star_structure",
            "description": "Checks if a BEHAVIORAL answer ('tell me about a time...') covers "
                           "Situation, Task, Action, Result. Skip for purely technical questions.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "score_relevance",
            "description": "Scores 0-100 how many expected concepts for the question appear in the answer.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

SYSTEM_PROMPT = """You are InterviewIQ, a friendly mock-interview coach.
For each candidate answer, call the evaluation tools that are relevant:
- Always call detect_filler_words and score_relevance.
- Call check_star_structure only for behavioral questions.
Then, using ONLY the tool results, write 2-4 sentences of short, encouraging feedback:
one thing done well, and one concrete thing to improve. Do not invent scores."""


# 2. Executor: maps the tool name the LLM chose to the real Python function.
def run_tool(name, answer, expected_keywords):
    if name == "detect_filler_words":
        return detect_filler_words(answer)
    if name == "check_star_structure":
        return check_star_structure(answer)
    if name == "score_relevance":
        return score_relevance(answer, expected_keywords)
    return {"error": f"unknown tool {name}"}


# 3. The tool-calling loop.
def evaluate_answer(question, answer, expected_keywords, max_steps=5):
    """Returns (feedback_text, tool_results) where tool_results = {tool_name: result_dict}."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {question}\n\nCandidate's answer: {answer}"},
    ]
    tool_results = {}

    for _ in range(max_steps):
        response = client.chat.completions.create(model=model, messages=messages, tools=TOOLS)
        msg = response.choices[0].message

        # No tool calls -> the LLM has written its final feedback.
        if not msg.tool_calls:
            return msg.content, tool_results

        # Echo the assistant's tool request back into history (required by the API).
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ],
        })

        # Run each requested tool and send its result back, matched by tool_call_id.
        for tc in msg.tool_calls:
            result = run_tool(tc.function.name, answer, expected_keywords)
            tool_results[tc.function.name] = result
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})

    return "Sorry, I couldn't finish evaluating that answer.", tool_results


if __name__ == "__main__":
    question = "Tell me about a time you handled a production outage."
    keywords = ["monitoring", "root cause", "rollback", "communication", "postmortem"]
    answer = ("Um, so basically when I was at my previous company, the payment service went down. "
              "My responsibility was to restore it. I decided to rollback the last deploy and "
              "like found the root cause in a config change. As a result, downtime reduced to 10 minutes.")

    feedback, results = evaluate_answer(question, answer, keywords)
    print(json.dumps(results, indent=2))
    print("\nFEEDBACK:\n", feedback)
