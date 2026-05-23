# EviCare

This repository contains the implementation of our paper **"EviCare: Enhancing Diagnosis Prediction with Deep Model-Guided Evidence for In-Context Reasoning"**, accepted at **KDD 2026**.

---

## Data

### Data Sources

In accordance with the requirements of the **PhysioNet Clinical Databases**, we are unable to openly share the raw data without prior permission. Researchers interested in accessing the data can apply through the following links:


- [MIMIC-III](https://physionet.org/content/mimiciii/1.4/)
- [MIMIC-IV](https://physionet.org/content/mimiciv/2.2/)

CCS-related data is sourced from the [Clinical Classifications Software Refined (CCSR)](https://hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp).

### Data Preprocessing

Initial data processing follows the pipeline from [TRANS](https://github.com/The-Real-JerryChen/TRANS). 

The data files required by our model must then be preprocessed using the scripts in the `preprocess/` folder.

We thank the [TRANS](https://github.com/The-Real-JerryChen/TRANS) repository for sharing their data processing code.

---

## Reproduction Steps

### 1. Environment Setup

Install the following dependencies:

- Python
- PyTorch
- [PyHealth](https://github.com/sunlabuiuc/PyHealth)
- [LLaMA-Factory](https://github.com/hiyouga/LlamaFactory)

### 2. Deep Model Training

We recommend using the corresponding repositories to train the deep models:

- [TRANS](https://github.com/The-Real-JerryChen/TRANS) — for training and evaluating RETAIN and related models
- [BoxLM](https://github.com/Melinda315/BoxLM) — for training and evaluating BoxLM and related models

We provide `deep/main_test.py` to save deep model prediction results, which are used as evidence in the subsequent stages.

### 3. Diagnosis Prediction Corpus Construction

Run `corpus/m3_dp_construction.ipynb` to build the corpus. The following files are required:

| File | Description |
|---|---|
| `mimic3_dataset_0.05.pkl` | Dataset files; refer to [BoxLM](https://github.com/Melinda315/BoxLM) for construction |
| `ccs_ccs.pkl` | CCS–CCS co-occurrence graph built from pairwise statistics over the training set |
| `visit_ccs.pkl` | Priority-ranked CCS codes produced by the deep model |
| `patient_time_m3_0.05_y_results.pkl` | Deep model prediction results; refer to `deep/main_test.py` |
| `ICD9CM.csv` | ICD-9-CM code descriptions |
| `CCS9.csv` | CCS category descriptions |
| `ICD9CM_to_CCSCM.csv` | Mapping between ICD-9-CM codes and CCS categories |

### 4. LLM Inference

**Step 1 — Deploy the LLM:**

```bash
API_PORT=9000 CUDA_VISIBLE_DEVICES=0 nohup llamafactory-cli api LLM/qwen3-8B.yaml \
    > logs/run_qwen3-8B.log 2>&1 &
```

**Step 2 — Run inference:**

```bash
python LLM/llm_inference.py
```

**Step 3 — Convert predictions:**

Match the `pred` field in the output sequentially against `CCS9.csv` to obtain EviCare's final diagnosis predictions for evaluation.

---

## Acknowledgements

We gratefully acknowledge the following open-source projects:

- [TRANS](https://github.com/The-Real-JerryChen/TRANS) — for training and evaluating RETAIN
- [BoxLM](https://github.com/Melinda315/BoxLM) — for training and evaluating BoxLM
- [LLaMA-Factory](https://github.com/hiyouga/LlamaFactory) — for LLM deployment

Their contributions have been instrumental to this work.
