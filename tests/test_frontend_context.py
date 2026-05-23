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


def test_virtual_shell_keeps_linux_root_directory_semantics():
    change_directory = js_function_body("changeDirectory")
    list_directory = js_function_body("listDirectory")
    resolve_path = js_function_body("resolvePath")

    assert '"/": ["home", "var", "etc", "sys", "srv", "dev"]' in HTML
    assert "isVirtualDirectory(next)" in change_directory
    assert "virtualDirectories[path]" in list_directory
    assert 'rawTarget.startsWith("/")' in resolve_path
    assert "normalizePath(rawTarget)" in resolve_path


def test_virtual_shell_normalizes_common_linux_path_segments():
    resolve_path = js_function_body("resolvePath")
    normalize_path = js_function_body("normalizePath")

    assert 'target || "~"' in resolve_path
    assert 'rawTarget === "~" || rawTarget.startsWith("~/")' in resolve_path
    assert 'part === "."' in normalize_path
    assert 'part === ".."' in normalize_path
    assert 'return parts.length ? `/${parts.join("/")}` : "/"' in normalize_path


def test_ending_modal_can_close_without_restart():
    assert 'id="endingCloseButton"' in HTML
    bind_events = js_function_body("bindEvents")
    close_ending = js_function_body("closeEnding")

    assert 'elements.endingCloseButton.addEventListener("click", closeEnding)' in bind_events
    assert 'hideScreen("endingScreen")' in close_ending
    assert "restartGame" not in close_ending


def test_terminal_tab_completion_is_bound_to_command_input():
    bind_events = js_function_body("bindEvents")
    complete_command_input = js_function_body("completeCommandInput")

    assert 'event.key === "Tab"' in bind_events
    assert "event.preventDefault()" in bind_events
    assert "completeCommandInput()" in bind_events
    assert "getInputCompletion(input)" in complete_command_input


def test_terminal_tab_completion_uses_virtual_filesystem():
    assert "const shellCommands = [" in HTML
    assert "const virtualDirectories = {" in HTML
    get_input_completion = js_function_body("getInputCompletion")
    complete_path_token = js_function_body("completePathToken")
    list_directory = js_function_body("listDirectory")
    change_directory = js_function_body("changeDirectory")

    assert "completeFromOptions(input" in get_input_completion
    assert "usesPathCompletion(command)" in get_input_completion
    assert "virtualDirectoryEntries(parent)" in complete_path_token
    assert "directoriesOnly" in complete_path_token
    assert "virtualDirectories[path]" in list_directory
    assert "isVirtualDirectory(next)" in change_directory
