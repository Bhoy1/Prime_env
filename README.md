# Congressional Records Q&A Evaluation System

> **Status:** 🚧 Work in Progress

A RAG-based evaluation system for testing AI agents on question-answering tasks using Congressional Records data.

## Overview

This project evaluates AI agents' ability to search, retrieve, and answer questions about Congressional Records using:
- **ChromaDB** for semantic search and vector storage
- **OpenAI Embeddings** for document chunking and retrieval
- **Verifiers Framework** for agent evaluation and scoring
- **Judge LLM** to assess answer correctness

## Current Results

**Evaluation Performance (gpt-5-mini):**
- ✅ **90% Accuracy** (9/10 correct)
- 🎯 Average Reward: 0.9 / 1.0
- 📊 Successfully answers questions about bills, votes, reports, and congressional proceedings

## Project Structure

```
.
├── congressional_eval.py      # Main evaluation environment setup
├── run_evaluation.py           # Run evaluations and compare models
├── fix_questions.py            # Add date context to vague questions
├── tes.py                      # Q&A pair generation from records
├── .env                        # Configuration (API keys, models)
├── data/                       # Congressional record text files
├── output/
│   └── qa_pairs.json          # Generated Q&A pairs
└── .chroma_db/                # Vector database storage
```

## Setup

### 1. Install Dependencies

```bash
pip install chromadb verifiers datasets openai python-dotenv tqdm
```

### 2. Configure Environment

Create a `.env` file with:

```bash
# API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
JUDGE_MODEL=gpt-5-mini
JUDGE_BASE_URL=https://api.openai.com/v1
EMBED_MODEL=text-embedding-3-small
EMBED_BASE_URL=https://api.openai.com/v1

# Paths
CHROMA_DB_DIR=.chroma_db
DATA_DIR=data
QA_PAIRS_FILE=output/qa_pairs.json

# Evaluation Settings
MAX_TURNS=15
N_SEARCH_RESULTS=10
MAX_EXAMPLES=10
```

### 3. Prepare Data

Place Congressional Record text files in the `data/` directory.

### 4. Generate Q&A Pairs (Optional)

```bash
python tes.py
```

This generates question-answer pairs from the congressional records.

### 5. Fix Questions (Add Date Context)

```bash
python fix_questions.py
```

This adds specific dates to questions that are too vague (e.g., "When did the House adjourn?" → "When did the House adjourn? (from the congressional record dated Wednesday, July 2, 2025)")

## Usage

### Run Evaluation

```bash
python run_evaluation.py
```

This will:
1. Run a single example demo (detailed output with tool calls)
2. Evaluate on 5 examples (aggregate metrics)
3. Save results to `evaluation_results_{model_name}.json`

### Customize Evaluation

Edit `run_evaluation.py` to:

```python
# Run on more examples
await run_full_evaluation(model_name="gpt-5-mini", max_examples=10)


# Test single example
await run_single_example(model_name="gpt-5-mini")
```

## How It Works

### 1. Data Loading & Chunking
- Loads Congressional Records from text files
- Chunks long documents (~1500 tokens per chunk) to fit embedding limits
- Stores chunks in ChromaDB with metadata (date, record_id)

### 2. Agent Tools
The agent has access to three tools:

- `search_records(query)` - Semantic search across all records
- `read_record(record_id)` - Read full content of a specific record
- `list_records()` - List all available records with dates

### 3. Evaluation Process
1. Agent receives a question
2. Agent searches for relevant records
3. Agent reads the full record content
4. Agent extracts the answer
5. Judge LLM compares agent's answer to expected answer
6. Score: 1.0 if correct, 0.0 if incorrect

### 4. Scoring System
- **Tool Rubric**: Tracks tool usage (weight 0.0 by default)
- **Judge Rubric**: LLM judge evaluates correctness (weight 1.0)
- **Max Score**: 1.0 (correct) or 0.0 (incorrect)

## System Prompt Strategy

The agent is instructed to:
1. **Always search first** using `search_records()`
2. **Always read full records** using `read_record()`
3. **Never answer from previews alone** (they're incomplete)
4. **Be concise** - answer only what was asked
5. **Use exact phrasing** from the record when possible

## Example Questions

✅ **Working Well:**
- "What public bills and resolutions were introduced on Wednesday, July 2, 2025?"
- "Which Representative resigned, from which district, and when did the resignation take effect?"
- "What measures were reported in the Senate and what are their report numbers?"

❌ **Still Improving:**
- Complex multi-part questions requiring multiple record searches
- Questions about specific bill votes (sometimes not found in records)

## Key Features

- ✅ Automatic text chunking for long documents
- ✅ Semantic search with deduplication
- ✅ Date extraction from records
- ✅ Question enhancement with temporal context
- ✅ Clean evaluation output with accuracy metrics
- ✅ JSON export of detailed results

## Next Steps / TODO

- [ ] Expand to full dataset evaluation (all Q&A pairs)
- [ ] Test additional models (GPT-4o, Claude, etc.)
- [ ] Improve search relevance for edge cases
- [ ] Add support for multi-hop reasoning questions
- [ ] Optimize system prompt for better answer formatting
- [ ] Add more evaluation metrics (precision, recall, F1)

## Results Files

After running evaluation, check:
- `evaluation_results_gpt-5-mini.json` - Detailed results with all questions, answers, and scores
- Individual question analysis with ✓/✗ status

## Technical Notes

### Chunking Strategy
- **Chunk Size**: 6000 characters (~1500 tokens)
- **Overlap**: 200 characters to maintain context
- **Break Points**: Prefers newlines or periods for clean splits

### Embedding Limits
- OpenAI embedding models have 8,191 token limit
- Chunking ensures all text fits within limits
- ChromaDB handles vector storage and retrieval

### Judge Prompt
Uses default verifiers JudgeRubric prompt:
```
Given a ground truth answer and a response, determine if the response is correct.
Respond either "yes" or "no" only.
```

## Dependencies

```
chromadb
verifiers
datasets
openai
python-dotenv
tqdm
```

## License

[Your License Here]

## Development Status

### Type of Change
- [x] New environment implementation
- [ ] Update to existing environment
- [ ] Other repo maintenance (docs, tests)

### Evaluation
- [x] Evaluation results included with at least 5 examples (`evaluation_results_gpt-5-mini.json`)
- [x] Results show rewards > 0 (90% accuracy, 9/10 correct)
- [x] Rollout logic and reward logic behaving as expected
- [ ] Pre-commit hooks installed
- [ ] Code passes style rules (`ruff check --fix .`)
- [ ] Tests implemented and passing (`pytest`)

### Checklist
- [x] Code follows best practices for environment development
- [x] Implementation uses verifiers framework properly
- [x] Data preparation logic encapsulated in `load_environment()`
- [x] Loads data from original sources (local congressional records)
- [x] Self-review of code completed
- [x] Manual cleanup pass performed (removed LLM "slop")
- [x] Code commented appropriately (not excessively)
- [x] Environment documented with README

### Known Issues / TODO
- [ ] Pre-commit hooks not yet configured
- [ ] Style checking with ruff not yet implemented
- [ ] Unit tests not yet written
- [ ] One edge case failing (H.R. 3633 vote question)
- [ ] Full dataset evaluation pending (currently 10 examples)

## Contributing

This is a work in progress. Contributions and suggestions welcome!

---

**Current Status**: 90% accuracy on 10 congressional Q&A evaluation. System successfully retrieves and answers questions about bills, votes, reports, and proceedings from Congressional Records.
