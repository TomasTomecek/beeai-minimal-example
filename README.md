# Simple BeeAI Agent

A minimal agentic example demonstrating the [BeeAI framework](https://github.com/i-am-bee/beeai-framework) for looking for compiler warnings in a build log.

## Requirements

- Python 3.13
- BeeAI Framework
- Pydantic

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TomasTomecek/beeai-minimal-example.git
cd beeai-minimal-example
```

2. Install dependencies:
```bash
pip install -e .
```

Or install dependencies directly:
```bash
pip install beeai-framework pydantic
```

3. Set up your model of choice with proper authentication. For GCP Gemini Language API it is:
```bash
export CHAT_MODEL="gemini:gemini-2.5-pro"
export GEMINI_API_KEY="..."
```

## Usage

Run the agent with a build log file:

```bash
python3 agent.py <path-to-build-log>
```

Example with the included sample log:
```bash
python agent.py libtiff-c8s-build.log

...


```

