# Week 3 — Advanced Prompting: Zero-Shot, Few-Shot, and Chain-of-Thought (CoT)

This package contains:
- prompt templates (zero-shot, few-shot, CoT)
- runnable experiment script (`run_experiments.py`)
- sample datasets (logic, math, reasoning, benchmark)
- evaluation rubric and framework
- example report and sample results
- instructions on how to run and reproduce the experiments

## Quick start

1. Unzip the folder and `cd` into `week03_advanced_prompting`.
2. Install dependencies:
```bash
pip install openai pandas tqdm
```
3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
```
4. Run the sample experiments (this will call the OpenAI API):
```bash
python run_experiments.py
```
Outputs are written to `results/` as CSV files.

If you don't want to call the API, run `python run_experiments.py --dry-run` to simulate runs using the sample dataset and show what would happen.
