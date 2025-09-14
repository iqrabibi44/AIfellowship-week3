# Week 3 — Experimental Report (Example)

This is an example report showing how to present results.

## Datasets used
- logic-puzzles.json (3 items)
- math-problems.json (3 items)
- reasoning-tasks.json (3 items)

## Prompts used
Prompts are in the `prompts/` folder. For each dataset we ran:
- Zero-shot
- Few-shot (2-shot)
- Chain-of-Thought (CoT)

## Example results
See `results/` CSV files for model outputs. If you ran `--dry-run` the outputs are simulated.

## Comparative insights (example)
- Few-shot improved format and reduced short-answer style errors.
- CoT produced more transparent intermediate steps but occasionally introduced verbosity and minor calculation errors when temperature > 0.
- Zero-shot is fast and clean but less consistent on unusual formats.

Final recommendation: For reasoning-critical tasks use Few-Shot + CoT verification pass (run CoT but evaluate final answer only).
