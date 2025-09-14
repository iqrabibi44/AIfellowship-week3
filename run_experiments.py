
import os
import json
import csv
import argparse
from time import sleep
import streamlit as st
import pandas as pd

try:
    import openai
except Exception:
    openai = None

try:
    import google.generativeai as genai
except Exception:
    genai = None

BASE_DIR = os.path.dirname(__file__)
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_json(fname):
    with open(fname, "r") as f:
        return json.load(f)

def build_prompt_zero_shot(item):
    if 'question' in item:
        passage = item.get('passage', item.get('passage',''))
        q = item['question']
        return f"You are a precise reasoning assistant. Use only the information provided. If missing, say 'NOT ENOUGH INFORMATION'.\nPassage: {passage}\nQ: {q}\nA:"
    if 'problem' in item:
        return f"""You are a clear math solver. Solve the problem step-by-step and provide the final answer. Problem: {item['problem']}"""
    if 'prompt' in item:
        return f"Answer succinctly: {item['prompt']}"
    if 'q' in item:
        return f"Answer succinctly: {item['q']}"
    return "Answer the question: " + str(item)

def build_prompt_few_shot(item):
    example = "Example: If Alice has 3 and gives 1, answer: 2."
    base = build_prompt_zero_shot(item)
    return example + "\n\n" + base

def build_prompt_cot(item):
    base = build_prompt_zero_shot(item)
    return base + "\n\nExplain your reasoning step by step, then give the final answer."

def call_model(prompt, model="gpt-4o-mini", max_tokens=256, temperature=0.0):
    if os.environ.get("DRY_RUN","")=="1":
        return "[DRY RUN] " + prompt[:200].replace("\n"," ") + "..."
    if genai is None:
        raise RuntimeError("google.generativeai package not available; install with pip install google-generativeai")
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(
        max_output_tokens=max_tokens,
        temperature=temperature
    ))
    return response.text.strip()

def score_output(output, gold):
    if isinstance(gold, str):
        a = gold.strip().lower()
        o = output.strip().lower()
        return 5 if a == o else (3 if a in o or o in a else 0)
    return 0

def run_on_dataset(dataset_fname, dry_run=False):
    data = load_json(dataset_fname)
    dataset_name = os.path.basename(dataset_fname).replace('.json','')
    results = []
    for item in data:
        for prompt_type, builder in [("zero-shot", build_prompt_zero_shot), ("few-shot", build_prompt_few_shot), ("cot", build_prompt_cot)]:
            prompt_text = builder(item)
            try:
                out = call_model(prompt_text) if not dry_run else "[DRY RUN] " + prompt_text[:120].replace("\n"," ")
            except Exception as e:
                out = f"[ERROR] {e}"
            gold = item.get('answer') or item.get('solution') or item.get('answer_key') or ""
            accuracy = score_output(out, gold)
            results.append({
                "dataset": dataset_name,
                "item_id": item.get('id',''),
                "prompt_type": prompt_type,
                "prompt_text": prompt_text.replace('\n','\\n')[:8000],
                "model_output": out.replace('\n','\\n'),
                "accuracy_score": accuracy,
                "reasoning_score": 0,
                "conciseness_score": 0,
                "fluency_score": 0,
                "notes": ""
            })
            sleep(0.2)
    out_fname = os.path.join(RESULTS_DIR, dataset_name + "_results.csv")
    with open(out_fname, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = list(results[0].keys()) if results else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            for r in results:
                writer.writerow(r)
    return out_fname

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Do not call API; simulate outputs.")
    args = parser.parse_args()
    if args.dry_run:
        os.environ["DRY_RUN"] = "1"
    datasets = [os.path.join(DATASETS_DIR, fn) for fn in os.listdir(DATASETS_DIR) if fn.endswith('.json')]
    print("Datasets found:", datasets)
    for ds in datasets:
        print("Running:", ds)
        out = run_on_dataset(ds, dry_run=args.dry_run)
        print("Wrote results:", out)

def streamlit_app():
    st.title("Advanced Prompting Experiments with Gemini API")
    st.write("Run prompting experiments across various datasets using Gemini API.")

    if st.button("Run Experiments"):
        with st.spinner("Running experiments... This may take a while."):
            datasets = [os.path.join(DATASETS_DIR, fn) for fn in os.listdir(DATASETS_DIR) if fn.endswith('.json')]
            progress_bar = st.progress(0)
            total_datasets = len(datasets)
            for i, ds in enumerate(datasets):
                st.write(f"Running: {os.path.basename(ds)}")
                out = run_on_dataset(ds, dry_run=False)
                st.write(f"Wrote results: {out}")
                progress_bar.progress((i + 1) / total_datasets)
            st.success("Experiments completed!")

    st.header("Results")
    results_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith('_results.csv')]
    if results_files:
        for file in results_files:
            st.subheader(file.replace('_results.csv', '').replace('-', ' ').title())
            df = pd.read_csv(os.path.join(RESULTS_DIR, file))
            st.dataframe(df)
    else:
        st.write("No results yet. Run the experiments to generate results.")

if __name__ == '__main__':
    streamlit_app()
