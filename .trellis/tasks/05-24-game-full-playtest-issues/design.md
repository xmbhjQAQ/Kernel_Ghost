# Design: 游戏引导、百科与攻略入口完善

## 架构与边界
- 主要变更集中在 `index.html`，继续保持单文件静态游戏结构。
- 不引入外部依赖，不增加构建流程。
- 新手教程仍走现有 `screen: "onboarding"`、`onboardingStep`、`handleOnboardingCommand()` 状态机。
- 百科继续复用现有 `encyclopediaScreen` 弹窗，但内容改为“当前游戏实际使用知识”。
- 新增书本入口使用独立弹窗，避免和百科、工单间事件、结局弹窗状态互相污染。
- 收藏 Hint 作为收藏项内部的独立按钮，不改变已发现收藏项点击回看行为。

## 新手教程设计
- 目标不是提前教完整攻略，而是教会玩家读工单、定位目录、读取文件、过滤文本、提交 Flag。
- 建议教程步骤扩展为：
  - `help`：知道可以查看当前阶段提示。
  - `pwd`：查看当前目录。
  - `ls`：列出文件。
  - `ls -a`：理解隐藏文件存在。
  - `cd tickets`：切换目录。
  - `cat intro.txt`：读取文件。
  - `cat intro.txt | grep "FLAG"` 或等价训练文件：理解管道和 `grep`。
  - `submit_flag FLAG{TRAINING_OK}`：理解提交格式，使用训练 Flag，不影响正式 `completedFlags`。
- 阶段专用命令如 `ps`、`kill`、`sandbox`、`weights`、`override_validator`、`verify_evidence`、`derive_key`、`decrypt` 不建议全部在入职教程中强制实操，否则教程过长；应在百科提供速查，在正式阶段由工单和错误反馈引导。

## 百科设计
- 删除未使用泛知识：
  - 哈希
  - 古典密码
  - RSA
- 保留并完善实际使用知识：
  - 终端基础：`help`、`pwd`、`ls`、`ls -a`、`cd`、`cat`
  - 管道与过滤：`cat file | grep "TEXT"`
  - Flag 提交：`submit_flag FLAG{...}`
  - 隐藏文件和路径：相对路径、绝对路径、点文件
  - Base64：识别与解码终局残留
  - 证据链：`verify_evidence --lin`、`verify_evidence --echo-wall`
  - 黑档案 key：`derive_key --from evidence` 与 `decrypt distilled_metadata.encrypted --key ...`
  - 阶段专用命令速查：`ps`、`kill`、`sandbox`、`weights`、`override_validator`、`format`

## 收藏 Hint 设计
- 每个 `collectibleCatalog` 项增加 hint 文案或从独立 `collectionHintCatalog` 查表。
- 未发现时：
  - 标题仍保持 `???`，不在列表主文案中直接暴露名称。
  - `Hint` 按钮弹出轻提示：阶段、目录或前置条件。
- 已发现时：
  - `Hint` 可隐藏，或显示“已回收，可点击回看”；推荐隐藏，减少界面噪声。
- 工单间事件：
  - Hint 显示“完成对应阶段工单后随机归档；可重开或继续流程收集不同事件”。
- 可访问性：
  - Hint 按钮必须 `type="button"`。
  - 防止点击 Hint 触发父级收藏回看，需要 `event.stopPropagation()`。

## 书本弹窗设计
- 页面右上角新增书本图标按钮，可命名为“导览 / Guide”。
- 默认弹窗内容：
  - 宣传介绍
  - 玩法介绍
  - 常用命令速查
- 攻略区域默认折叠或隐藏。
- 点击“查看攻略”触发确认：
  - 确认文案明确提示“包含主线、结局、全收藏剧透”。
  - 用户取消则保持隐藏。
  - 用户确认后展示主线攻略和全收藏攻略。
- 内容来源优先复用《剧情文章与详细攻略.md》，页面内可摘取为常量或直接静态 HTML。

## 数据流与状态
- 新手教程新增步骤需要扩展 `onboardingStep` 的合法范围和 `onboardingExpectedCommand()`。
- 训练 Flag 只用于 onboarding，不写入正式 `completedFlags`。
- Hint 根据 `state.foundation` 显示：`beginner` 和 `terminal` 显示，`ready` 不显示。
- 书本攻略确认只需会话内状态即可；不要求持久化。
- 百科可见性仍由 `state.encyclopediaVisible` 控制，但“可直接参与案件”是否显示百科需要根据产品决策确认。

## 兼容与迁移
- 旧存档的 `onboardingStep` 归一化上限需要同步更新。
- 老玩家已在 `playing` 状态时不应被强制拉回教程。
- 收藏项新增字段必须兼容旧 `collection` localStorage。

## 风险
- 教程过长会拖慢进入游戏的节奏，需要把“必须实操”和“速查知识”分开。
- Hint 太强会直接破坏探索感，因此只给 `beginner` 和 `terminal` 路径，`ready` 路径保持无 Hint。
- 攻略弹窗内容较长，移动端需要滚动体验和关闭按钮稳定。
