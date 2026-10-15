---
name: langchain
title: LangChain and LangGraph
area: ml
tags: [python, llm, chains, agents, langgraph, runnables]
detect: [dep:langchain, dep:langchain-core, dep:langchain-anthropic, dep:langgraph, dep:langchain-community]
related: [llamaindex, rag, tool-use, llm-evals, anthropic-sdk]
---
LangChain apps: runnables composed with LCEL, chat model wrappers, structured output and LangGraph state graphs for agents.

## Verify
- `python -c "import langchain_core; print(langchain_core.__version__)"`: the core package version.
- `pytest -q`: chain and graph tests pass against fake models.
- `pip check`: provider packages and core versions are compatible.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Use a fake chat model from `langchain_core` so the chain runs offline and deterministically.
```python
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def test_chain_formats_prompt_and_parses():
    llm = GenericFakeChatModel(messages=iter([AIMessage(content="hello")]))
    chain = ChatPromptTemplate.from_template("Say {x}") | llm | StrOutputParser()
    assert chain.invoke({"x": "hi"}) == "hello"
```

## Do
- Compose with the `|` operator and call `invoke`, `batch` or `stream`. Use `ainvoke` in async code.
- Import from `langchain_core` and the provider package (for example `langchain_anthropic`), not from `langchain_community` for models that have their own package.
- Get typed output with `llm.with_structured_output(PydanticModel)` instead of parsing text.
- Bind tools with `llm.bind_tools([...])` and define them with the `@tool` decorator and type hints.
- For agents, use LangGraph: a `StateGraph` with typed state, explicit nodes and edges, and a checkpointer for memory and resume.
- Set `max_retries` and timeouts on the model, and cap graph steps with the `recursion_limit` config.
- Trace with LangSmith or callbacks in dev, and keep secrets out of traces.
- Pin versions: the API moves quickly between releases.

## Avoid
- `LLMChain`, `ConversationChain`, `initialize_agent` and `AgentExecutor` in new code: legacy. Use runnables and LangGraph.
- `from langchain.llms import ...` style imports: moved to partner packages. Import from `langchain_<provider>`.
- Passing `chain.run(...)`: removed in newer releases. Use `invoke`.
- Regex-parsing model output when structured output exists: fragile. Use `with_structured_output`.
- Unbounded agent loops: cost and hangs. Set `recursion_limit` and tool-call caps.
- Hiding simple API calls behind several abstractions: harder to debug. Use the provider SDK when a chain adds nothing.
- Tests that hit a real model: flaky. Use fake models.

## Review
- [ ] No legacy chain or agent classes remain.
- [ ] Imports come from `langchain_core` and provider packages.
- [ ] Structured output and tools are typed.
- [ ] Graph has a step limit and, if stateful, a checkpointer.
- [ ] Tests run offline with fake models.
