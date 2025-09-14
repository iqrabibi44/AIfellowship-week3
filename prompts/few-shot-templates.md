# Few-Shot Prompt Templates

Use at least 2 examples in each few-shot prompt. Examples shown are short; replace with dataset-specific examples.

## Few-shot template (Q&A / reasoning)
You are a helpful and precise reasoning assistant. Use the examples to model the format and then answer the user's question.

Example 1:
Passage: "Alice has 3 apples and gives 1 to Bob."
Q: How many apples does Alice have now?
A: Alice has 2 apples.

Example 2:
Passage: "A train travels 60 km/h for 2 hours."
Q: How far did the train travel?
A: The train traveled 120 km.

Now answer:
Passage:
<<<PASSAGE>>>
Q: <<<QUESTION>>>
A:
