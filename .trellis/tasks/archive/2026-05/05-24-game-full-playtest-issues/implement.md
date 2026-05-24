# Implement: 游戏引导、百科与攻略入口完善

## 实施顺序
1. 扩展状态字段与 DOM 缓存
   - 增加书本按钮、书本弹窗、攻略确认按钮、关闭按钮。
   - 如需要，增加 `guideSpoilersVisible` 这类会话内变量。
   - 更新 `normalizeRestoredState()` 的 `onboardingStep` 上限。

2. 扩展新手教程
   - 更新 `tickets` 中 onboarding 相关工单。
   - 扩展 `beginOnboarding()` 起始说明。
   - 扩展 `handleOnboardingCommand()` 步骤，覆盖 `help`、`pwd`、`ls`、`ls -a`、`cd`、`cat`、`grep`/管道、训练 Flag 提交。
   - 确认训练 Flag 不进入主线 `completedFlags`。

3. 精简并重写百科
   - 删除哈希、古典密码、RSA。
   - 增加实际玩法知识：终端命令、管道、隐藏文件、Base64、证据验证、key 派生与解密。
   - 确认“终端基础已具备”和“基础待建立完成教程”用户都能打开百科。

4. 增加收藏 Hint
   - 为每个收藏项配置 hint 文案。
   - 在 `renderDiscoveries()` 中插入 Hint 按钮。
   - 确保按钮点击不触发收藏回看。
   - 根据 `state.foundation` 控制显示策略：`beginner` 和 `terminal` 显示，`ready` 不显示。

5. 增加书本导览弹窗
   - 添加右上角书本按钮样式和 HTML。
   - 默认展示宣传介绍、玩法介绍、命令速查。
   - 点击攻略按钮时 `window.confirm()` 二次确认，确认后展示主线攻略和全收藏攻略。
   - 确保移动端可滚动、可关闭。

6. 验证与回归
   - 静态脚本语法检查。
   - 本地页面 smoke test：新手路径、轻基础路径、可直接参与案件路径。
   - 检查收藏 Hint 点击、已发现收藏回看、百科打开关闭、书本攻略确认。

## 验证命令
- `node -e "const fs=require('fs'); const html=fs.readFileSync('index.html','utf8'); const script=html.match(/<script>([\\s\\S]*)<\\/script>/)[1]; new Function(script); console.log('index.html script syntax ok');"`
- 如 Python 测试仍适配：`python -m pytest`

## 风险文件
- `index.html`
- `剧情文章与详细攻略.md`，仅在需要同步站内导览文案时修改。

## 回滚点
- 新手教程状态机最容易引入流程阻断；每新增一步都要验证错误命令提示和正确命令推进。
- 收藏 Hint DOM 嵌套在可点击收藏项中，必须防止事件冒泡。
- 攻略确认不能只靠 `<details>`，否则用户可能误展开剧透。
