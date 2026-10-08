"""All prompting techniques: Zero-shot, One-shot, Few-shot, CoT, ToT."""

TECHNIQUES = {
    "Zero-Shot": {
        "icon": "🎯",
        "desc": "No examples. Direct question only.",
    },
    "One-Shot": {
        "icon": "1️⃣",
        "desc": "One example is given before the task.",
    },
    "Few-Shot": {
        "icon": "🔢",
        "desc": "Multiple examples guide the model.",
    },
    "Chain of Thought (CoT)": {
        "icon": "🔗",
        "desc": "Model reasons step by step.",
    },
    "Tree of Thought (ToT)": {
        "icon": "🌳",
        "desc": "Explores multiple reasoning branches, then picks the best.",
    },
}


def zero_shot(task: str) -> str:
    return f"{task}\n\nGive a clear and direct answer."


def one_shot(task: str) -> str:
    return f"""Follow the style of the example below.

Example:
Q: What is the capital of France?
A: The capital of France is Paris.

Now answer:
Q: {task}
A:"""


def few_shot(task: str) -> str:
    return f"""Follow the style of the examples below.

Q: What is the capital of France?
A: The capital of France is Paris.

Q: What is 12 multiplied by 8?
A: 12 multiplied by 8 is 96.

Q: Who wrote Romeo and Juliet?
A: Romeo and Juliet was written by William Shakespeare.

Now answer:
Q: {task}
A:"""


def chain_of_thought(task: str) -> str:
    return f"""{task}

Let's think step by step.
1. Break the problem into smaller parts.
2. Solve each part with clear reasoning.
3. Finish with a line starting with "Final Answer:"."""


def tree_of_thought(task: str) -> str:
    return f"""Problem: {task}

Solve this using Tree of Thought reasoning:

Step 1 - Generate 3 different approaches (Branch A, Branch B, Branch C).
Step 2 - For each branch, develop the reasoning in 2-3 steps.
Step 3 - Evaluate each branch: score it from 1-10 for correctness and feasibility,
         and explain why.
Step 4 - Pick the best branch (or merge the best parts).
Step 5 - Give the result as "Final Answer:" with a short justification."""


BUILDERS = {
    "Zero-Shot": zero_shot,
    "One-Shot": one_shot,
    "Few-Shot": few_shot,
    "Chain of Thought (CoT)": chain_of_thought,
    "Tree of Thought (ToT)": tree_of_thought,
}


def build_prompt(technique: str, task: str) -> str:
    return BUILDERS[technique](task)