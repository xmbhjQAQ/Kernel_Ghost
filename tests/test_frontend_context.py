from pathlib import Path


HTML = Path("index.html").read_text(encoding="utf-8")


def js_function_body(name: str) -> str:
    marker = f"function {name}"
    start = HTML.index(marker)
    brace_start = HTML.index("{", start)
    depth = 0
    for index in range(brace_start, len(HTML)):
        char = HTML[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return HTML[brace_start : index + 1]
    raise AssertionError(f"Could not find complete JavaScript function {name}")


def test_last_command_output_preserves_full_command_output():
    body = js_function_body("buildOrderedTerminalContext")

    assert "group.output.slice()" in body
    assert "group.output.slice(-" not in body


def test_terminal_entries_do_not_truncate_command_context_before_grouping():
    body = js_function_body("terminalEntries")

    assert "text: node.textContent" in body
    assert "node.textContent.slice(" not in body
