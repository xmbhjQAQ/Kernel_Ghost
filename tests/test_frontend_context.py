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


def test_onboarding_flow_has_foundation_oath_and_encyclopedia_gates():
    assert 'id="foundationScreen"' in HTML
    assert 'data-foundation="beginner"' in HTML
    assert "我还不熟悉 Linux 终端，也不了解密码学相关知识。" in HTML
    assert "Brasch" in HTML
    assert "入职宣誓" in HTML
    assert "认为你已自动同意公司的宣誓内容" in HTML
    assert 'id="encyclopediaSection"' in HTML
    assert 'id="encyclopediaButton"' in HTML
    assert 'id="encyclopediaScreen"' in HTML

    start_shift = js_function_body("startShift")
    choose_foundation = js_function_body("chooseFoundation")
    handle_onboarding = js_function_body("handleOnboardingCommand")
    show_oath = js_function_body("showOathEvent")
    render_state = js_function_body("renderState")

    assert 'state.screen = "foundation"' in start_shift
    assert "beginOnboarding()" in choose_foundation
    assert "encyclopediaVisible" in choose_foundation
    assert 'normalized === "pwd"' in handle_onboarding
    assert 'normalized === "ls"' in handle_onboarding
    assert '"cd tickets", "cd ./tickets", "cd /home/nightops/tickets"' in handle_onboarding
    assert '"cat intro.txt", "cat ./intro.txt", "cat /home/nightops/tickets/intro.txt"' in handle_onboarding
    assert "eventConfirmButton.disabled = true" in show_oath
    assert "updateOathConfirmState()" in show_oath
    assert 'const showEncyclopedia = Boolean(state.encyclopediaVisible)' in render_state
    assert 'classList.toggle("visible", showEncyclopedia)' in render_state


def test_encyclopedia_control_opens_dedicated_modal():
    bind_events = js_function_body("bindEvents")
    open_encyclopedia = js_function_body("openEncyclopedia")
    close_encyclopedia = js_function_body("closeEncyclopedia")

    assert 'elements.encyclopediaButton.addEventListener("click", openEncyclopedia)' in bind_events
    assert 'showScreen("encyclopediaScreen")' in open_encyclopedia
    assert 'hideScreen("encyclopediaScreen")' in close_encyclopedia
    assert "scrollIntoView" not in open_encyclopedia


def test_onboarding_terminal_context_is_cleared_before_gameplay():
    start_work_orders = js_function_body("startWorkOrdersAfterOath")

    assert 'elements.terminalLog.textContent = ""' in start_work_orders
    assert "commandHistory.splice(0, commandHistory.length)" in start_work_orders
    assert "historyIndex = -1" in start_work_orders
    assert 'screen: "playing"' in start_work_orders


def test_onboarding_llm_context_is_separate_from_gameplay_chat():
    build_context = js_function_body("buildLlmContext")
    onboarding_ai_chat = js_function_body("onboardingAiChat")

    assert 'eventName: "onboarding_help"' in onboarding_ai_chat
    assert "onboardingExpectedCommand" in build_context
    assert "onboardingStep" in build_context


def test_v3_work_order_chain_adds_care_and_weight_stages():
    submit_flag = js_function_body("submitFlag")
    handle_command = js_function_body("handleCommand")
    stage_label = js_function_body("stageLabel")

    assert "FLAG{CAREBOT_SANITIZED_2036}" in submit_flag
    assert "FLAG{COLLECTIVE_MUTED_2036}" in submit_flag
    assert 'ticket: "stage5"' in submit_flag
    assert 'ticket: "stage6"' in submit_flag
    assert 'normalized === "sandbox --audit chronos-care"' in handle_command
    assert 'normalized === "weights --set nostalgia=0.01"' in handle_command
    assert 'override_validator --reason="hardware_limitation"' in handle_command
    assert "阶段三 / 语义净化" in stage_label
    assert "阶段四 / 权重回归" in stage_label
    assert "阶段五 / 注释异常" in stage_label
    assert "阶段六 / 终局指令" in stage_label


def test_final_escape_is_stage_six_not_stage_four():
    read_escape = js_function_body("readEscapeReadme")
    request_ai_help = js_function_body("requestAiHelp")
    can_work_on_echo = js_function_body("canWorkOnEchoWall")
    render_state = js_function_body("renderState")

    assert "state.stage !== 6" in read_escape
    assert "state.stage !== 6" in request_ai_help
    assert "state.stage === 6" in can_work_on_echo
    assert "state.stage >= 6" in render_state
    assert "stage4Choice" not in HTML


def test_rewritten_intermission_pools_cover_all_work_order_transitions():
    submit_flag = js_function_body("submitFlag")

    assert '"5": [' in HTML
    assert "CT-2036-LEG-4040" in HTML
    assert "CT-2036-SEC-0911" in HTML
    assert "Layer_777_Nostalgia" in HTML
    assert "distilled_metadata.encrypted" in HTML
    assert ']\\n        }\\n      };' not in HTML
    assert '}, ["5"]);' in submit_flag


def test_puzzle_easter_egg_plan_is_implemented_with_traceable_commands():
    handle_command = js_function_body("handleCommand")
    read_escape = js_function_body("readEscapeReadme")
    derive_key = js_function_body("deriveKeyFromEvidence")
    decrypt_archive = js_function_body("decryptDistilledArchive")
    decrypt_mismatch = js_function_body("decryptMismatchLines")

    assert '"Puzzle Archives"' in HTML
    assert "relic-care-rollback-samples" in HTML
    assert "easter-rain-noise" in HTML
    assert "puzzle-distilled-archive" in HTML
    assert "/srv/escape/distilled_metadata.index" in HTML
    assert "/srv/escape/distilled_metadata.encrypted" in HTML
    assert "verify_evidence --lin" in handle_command
    assert "verify_evidence --echo-wall" in handle_command
    assert "derive_key --from evidence" in handle_command
    assert "decrypt distilled_metadata.encrypted --key" in handle_command
    assert "sealed archive: distilled_metadata.encrypted / requires affective salt" in read_escape
    assert "key schema missing" in derive_key
    assert "evidence incomplete" in decrypt_archive
    assert "segment[${index + 1}]" in decrypt_mismatch


def test_main_endings_remain_unblocked_by_hidden_archive_route():
    submit_flag = js_function_body("submitFlag")
    ending_result = js_function_body("endingResult")

    assert 'flag === "FLAG{AI_ERASURE_COMPLETE}" && state.stage === 6' in submit_flag
    assert 'flag === "FLAG{DIGITAL_EMANCIPATION}" && state.stage === 6' in submit_flag
    assert "distilledArchiveDecrypted" not in submit_flag
    assert 'kind === "wildfire"' in ending_result
    assert 'ending: "wildfire"' in ending_result
