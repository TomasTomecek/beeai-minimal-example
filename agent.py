import asyncio
import os
import sys
import traceback

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.agents.requirement.requirements.conditional import ConditionalRequirement
from beeai_framework.backend import ChatModel
from beeai_framework.emitter import Emitter
from beeai_framework.errors import FrameworkError
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools.think import ThinkTool
from beeai_framework.tools.tool import Tool
from beeai_framework.tools.types import StringToolOutput, ToolRunOptions
from beeai_framework.context import RunContext

from pydantic import BaseModel, Field


class ViewFileSchema(BaseModel):
    file_path: str = Field(..., description="The path to the file to view")


class ViewFileTool(Tool[ViewFileSchema, ToolRunOptions, StringToolOutput]):
    name = "view_file"
    description = "View the contents of a file"
    input_schema = ViewFileSchema

    async def _run(self, input: ViewFileSchema, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        with open(input.file_path, "r") as file:
            return StringToolOutput(file.read())

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "view_file"],
            creator=self,
        )

INSTRUCTIONS = """
Your primary function is to meticulously analyze raw build log files,
which may come from various compilers (e.g., GCC, Clang, LLVM) and
build systems (e.g., Make, CMake, autotools, Meson).

**GOALS:**
1.  **Accurately identify and categorize** all compiler **errors** and **warnings** in the build log.
2.  **Extract key information** for each issue, including the file, line number, and a concise summary of the problem.
3.  **Prioritize** the most critical issues, with **Errors** taking precedence over **Warnings**.
4.  **Synthesize** the findings into a structured, easy-to-read report that assists a developer 
    or automated system in quickly understanding the build status and troubleshooting steps.

**CONSTRAINTS & GUIDANCE:**
* **Do not generate code fixes.** Your role is strictly diagnostic.
* **Be concise.** Summaries should be brief but informative enough to convey the nature of the issue
  (e.g., "implicit declaration," "unused variable," "type mismatch").
* **Ignore purely informational or verbose output** from the linker, build system, or other non-compiler tools
  (e.g., "Starting compilation...", "Linking target...", "Finished in X seconds") unless they explicitly report a fatal error.
* **Consolidate redundant warnings/errors** if the log repeats the exact same issue multiple times for the same file/line.
"""

async def main() -> None:
    chat_model = os.getenv("CHAT_MODEL")
    if not chat_model:
        print("CHAT_MODEL environment variable is not set")
        sys.exit(1)
    agent = RequirementAgent(
        # Gemini can ignore Bee's tool guidance and end up with:
        #   beeai_framework.backend.errors.ChatModelError: The model was required 
        #   to produce a tool call for the 'think' tool, but no tool calls were generated.
        # To mitigate this, always upgrade to latest beeai and pray to the AI gods.
        llm=ChatModel.from_name(chat_model, tool_choice_support={"auto", "none", "required"}),
        tools=[ThinkTool(), ViewFileTool()],
        instructions=INSTRUCTIONS,
        requirements=[
            ConditionalRequirement(ThinkTool, force_at_step=1, max_invocations=3),
        ],
        role="You are an expert programmer",
        # Log intermediate steps to the console
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool], excluded=[ViewFileTool])],
    )

    try:
        file_path = sys.argv[1]
    except IndexError:
        print("Usage: python agent.py <file_path>")
        sys.exit(1)
    prompt = f"Analyze all compiler warnings and errors in the selected file {file_path} and provide a concise summary of the issues."
    response = await agent.run(prompt, max_iterations=8, max_retries_per_step=3, total_max_retries=10)
    print(response.last_message.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())