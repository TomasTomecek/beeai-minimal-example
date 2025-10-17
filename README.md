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

Here is a summary of the warnings:

**-Warray-parameter= (7 warnings):**
- These warnings indicate a mismatch between function definitions and declarations for array parameters. For example, a function defined with `float xyz[3]` is declared elsewhere as `float*`. This can lead to confusion but is often not a critical issue.

**-Wmisleading-indentation (3 warnings):**
- The compiler found instances where the code's indentation suggests a different logic than what is actually executed. This can make the code harder to read and maintain.

**-Wimplicit-fallthrough= (10 warnings):**
- These warnings occur in `switch` statements where a `case` block falls through to the next one without an explicit `break` or `/* fallthrough */` comment. This can be a source of bugs if the fallthrough is unintentional.

**-Wshift-negative-value (1 warning):**
- A left shift of a negative value was detected, which can lead to undefined behavior in C.

**-Wformat= (1 warning):**
- This warning points to a type mismatch between a format specifier in a `printf`-like function and the actual argument passed. For example, using `%u` for a `long int`.

**-Wstringop-overflow= (2 warnings):**
- The compiler detected a potential buffer overflow when writing to a string, which could lead to security vulnerabilities.

**-Wformat-truncation= (1 warning):**
- This warning indicates that the output of a formatted string function might be truncated, leading to loss of data.

**libtool warnings (9 warnings):**
- These warnings from `libtool` indicate that certain libraries were not installed in the expected directory, which could cause issues during linking.
```

