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
    assert 'normalized === "进行入职宣誓"' in handle_onboarding
    assert "onboardingStep: 8" in handle_onboarding
    assert 'onboardingOath: {' in HTML
    assert 'patch: { screen: "oath", ticket: "onboardingOath" }' in handle_onboarding
    assert "准备好后，在 CLI 输入：进行入职宣誓" in HTML
    assert "showOath: true" in handle_onboarding
    assert "eventConfirmButton.disabled = true" in show_oath
    assert "updateOathConfirmState()" in show_oath
    assert 'const showEncyclopedia = Boolean(state.encyclopediaVisible)' in render_state
    assert 'classList.toggle("visible", showEncyclopedia)' in render_state
    assert "训练时用 ai_chat <问题> 问 Brasch" in HTML
    assert "建议经常输入 ai_chat <内容> 和 Kernel-Mind 对话" in HTML
    assert "就算你会终端，也要多用 ai_chat <内容> 和 Kernel-Mind 对话" in HTML
    assert "queueLines(lines).then(showOathEvent)" not in choose_foundation


def test_encyclopedia_control_opens_dedicated_modal():
    bind_events = js_function_body("bindEvents")
    open_encyclopedia = js_function_body("openEncyclopedia")
    close_encyclopedia = js_function_body("closeEncyclopedia")

    assert 'elements.encyclopediaButton.addEventListener("click", openEncyclopedia)' in bind_events
    assert 'showScreen("encyclopediaScreen")' in open_encyclopedia
    assert 'hideScreen("encyclopediaScreen")' in close_encyclopedia
    assert "scrollIntoView" not in open_encyclopedia


def test_long_modal_content_scrolls_inside_viewport():
    assert ".event-panel {" in HTML
    assert "max-height: calc(100dvh - 36px);" in HTML
    assert "display: flex;" in HTML
    assert "flex-direction: column;" in HTML
    assert ".encyclopedia {" in HTML
    assert ".guide-content {" in HTML
    assert ".plot-map {" in HTML
    assert "flex: 1 1 auto;" in HTML
    assert "min-height: 0;" in HTML
    assert "max-height: none;" in HTML


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


def test_llm_status_uses_kernel_mind_player_facing_copy():
    check_status = js_function_body("checkLlmStatus")

    assert "Kernel-Mind 状态" in HTML
    assert "LLM Link" not in HTML
    assert 'message: payload.enabled ? "可对话" : "本地回退"' in check_status
    assert "在线：" not in check_status
    assert "deepseek" not in HTML


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


def test_help_is_stage_scoped_and_not_full_walkthrough():
    help_result = js_function_body("helpResult")
    help_lines = js_function_body("helpLines")
    active_help = js_function_body("activeHelpLine")

    assert "helpLines()" in help_result
    assert "阶段三：cat /srv/care/incident.log" not in help_lines
    assert "阶段六工具：strings architecture.png" not in help_lines
    assert "decrypt distilled_metadata.encrypted --key <key>" not in help_lines
    assert "state.stage === 1" in active_help
    assert "state.stage === 6" in active_help
    assert "verify_evidence / derive_key" in active_help


def test_collection_masks_undiscovered_items_and_opens_found_archives():
    render_discoveries = js_function_body("renderDiscoveries")
    collection_title = js_function_body("collectionTitle")
    collection_hint = js_function_body("collectionHint")
    collection_status = js_function_body("collectionStatus")
    show_archive = js_function_body("showCollectionArchive")
    archive_record = js_function_body("collectionArchiveRecord")

    assert "collectionTitle(item, found)" in render_discoveries
    assert "showCollectionArchive(item.id)" in render_discoveries
    assert 'return "???"' in collection_title
    assert "item.group === \"Intermissions\"" in collection_title
    assert "当前尚不存在。" in collection_hint
    assert "已存在，尚未发现。" in collection_hint
    assert 'if (found) return `已回收 / Recovered · ${stageName(item.minStage)}`' in collection_status
    assert 'if (state.stage < item.minStage) return "尚不存在 / Not yet generated";' in collection_status
    assert 'return "已存在 / Undiscovered";' in collection_status
    assert "metaCollection.unlocked.includes(id)" in show_archive
    assert "relicCatalog.find" in archive_record
    assert "collectibleArchiveCatalog[id]" in archive_record


def test_plot_flowchart_control_opens_dedicated_modal():
    bind_events = js_function_body("bindEvents")
    open_plot = js_function_body("openPlotMap")
    close_plot = js_function_body("closePlotMap")

    assert 'id="plotButton"' in HTML
    assert 'id="plotScreen"' in HTML
    assert 'id="plotMap"' in HTML
    assert 'elements.plotButton.addEventListener("click", openPlotMap)' in bind_events
    assert 'elements.plotCloseButton.addEventListener("click", closePlotMap)' in bind_events
    assert 'renderPlotMap()' in open_plot
    assert 'showScreen("plotScreen")' in open_plot
    assert 'hideScreen("plotScreen")' in close_plot


def test_plot_flowchart_masks_hidden_routes_and_derives_current_position():
    render_plot_node = js_function_body("renderPlotNode")
    is_known = js_function_body("isPlotNodeKnown")
    current_node = js_function_body("currentPlotNodeId")
    hint_text = js_function_body("plotHintText")

    assert "const plotRouteCatalog = [" in HTML
    assert 'route: "echo"' in HTML
    assert 'route: "wildfire"' in HTML
    assert 'title.textContent = known ? node.title : "???"' in render_plot_node
    assert 'description.textContent = known ? node.description : "???"' in render_plot_node
    assert 'node.group === "main"' in is_known
    assert 'plotArchive.routes.includes(node.route)' in is_known
    assert 'plotArchive.endings.includes(node.ending)' in is_known
    assert 'if (state.ending) return `ending-${state.ending}`' in current_node
    assert 'return `stage${state.stage}`' in current_node
    assert "隐藏线路仍需要旧提交和身份证据" in hint_text


def test_plot_flowchart_persists_cross_run_and_clears_on_hard_reset():
    load_archive = js_function_body("loadPlotArchive")
    save_archive = js_function_body("savePlotArchive")
    update_archive = js_function_body("updatePlotArchiveFromState")
    known_routes = js_function_body("knownPlotRoutesFromState")
    reset_session = js_function_body("resetGameSession")

    assert 'let plotArchive = { routes: [], endings: [] }' in HTML
    assert 'window.localStorage.getItem(`${storagePrefix}plotArchive`)' in load_archive
    assert "uniqueKnownPlotIds(parsed.routes, plotRouteIds)" in load_archive
    assert 'window.localStorage.setItem(`${storagePrefix}plotArchive`' in save_archive
    assert "savePlotArchive()" in update_archive
    assert 'routes.push("stage6", "company", "escape")' in known_routes
    assert 'state.askedLin && state.hiddenDiscoveries.includes("git-log")' in known_routes
    assert 'state.hiddenDiscoveries.includes("distilled-index")' in known_routes
    assert 'plotArchive = { routes: [], endings: [] }' in reset_session
    assert 'window.localStorage.removeItem(`${storagePrefix}plotArchive`)' in reset_session
    assert 'hideScreen("plotScreen")' in reset_session
