# HTML 转 Unity UI 预制体技能中文说明

本文档是 `SKILL.md` 及其 `references/*.md` 的中文同步说明。英文 `SKILL.md` 是技能触发和执行时的主文档；维护本技能时，如果英文主文件或引用文档里的行为、流程、项目结构规则、校验要求、完成报告要求发生变化，必须在同一次变更中同步更新本文档。

## View 与 Prefab 授权规则

当前任务要求生成新的 `UIXXXView` 时，不需要额外 prefab 写入授权；该生成请求本身足以创建新的 View prefab、匹配的 View 脚本、注册代码，以及项目规则允许的新配套 UI 文件。

编辑已有 `.prefab` 必须获得当前任务和目标 prefab 的明确授权。没有授权时，不要修改、重新生成、覆盖、回滚或手改已有 `.prefab`。诊断、修代码、验证规则、检查层级、看截图、“确认清楚”或“按基准走”等请求，都不等于允许编辑已有 prefab。

普通点击打开的界面、弹窗、侧边栏、帮助、资料、确认流程、按平台显示的入口，默认作为独立 `UIView` 通过 `UIManager.ShowView` 打开且不询问；当前 View 通常只负责显示/隐藏入口并把点击路由到独立 View。只有局部 tab/page、主界面底部按钮切换预制页面组、同屏模式面板这类同一 View 内切换功能，才建议嵌入当前 View；如果强烈建议嵌入但用户没有明确要求，应先说明原因并询问。

## 核心规则

将 HTML/CSS 转成 Unity UGUI 预制体时，必须先读源码，再用浏览器渲染结果验证和测量源码实际产出的布局，不能只靠源码文本猜测布局。可运行原型、DOM、CSS、JavaScript 状态/渲染逻辑、浏览器实测布局和截图都是证据输入；最终 Unity 输出仍必须遵守用户明确指令、目标项目规则、同项目 Unity 样例、资源归属、序列化边界和校验要求。

所有原型理解一律以源码为准。必须先读取相关 HTML、CSS、JavaScript、配置、资源清单和生成输入，再打开渲染网页、运行浏览器测量或查看截图。网页输出和截图只能在源码审阅之后用于验证或补证，不能作为结构、状态、文案、资源或行为的第一解释来源。

## 第一优先级：元素证据计划

源码审阅完成后，在映射、生成、编辑或校验 Unity 文件之前，必须先写转换计划，并为每个 UI 元素记录证据。这是本技能的第一优先级判断逻辑，不是完成报告里的补充项。每个计划处理的 UI 元素都要回答：

- 这个元素为什么存在？
- 为什么使用这个图片、颜色、字体、材质或图集条目？
- 为什么使用这个位置、尺寸、anchor、sibling order、mask 和层级？
- 它有哪些状态，每个状态切换哪些序列化节点或属性？
- 它有哪些交互，由哪个 View、model 或 event 绑定负责？
- 哪些部分必须是静态 prefab/资源数据，哪些部分允许运行时处理？
- 是否有推断或证据缺失？

每个受影响元素还要记录适用的具体证据字段：截图区域、HTML 节点、已有 prefab 节点、源美术文件、图集条目、配置行或用户明确指令；sprite、texture、颜色、字体、`.meta` GUID、图集条目、材质的视觉依据；bounds、anchors、size、sibling order、mask、view layer 的布局依据；default active、selected、disabled、locked、hover、pressed、empty 等状态覆盖，以及每个状态切换哪些预制节点；button、toggle、drag、scroll、modal、navigation、model fields、events、runtime binding 等交互归属。

在计划明确受影响元素的稳定 GameObject 名、父级路径、来源证据、Unity 表现、运行时/静态边界和剩余缺口之前，不要生成或编辑 prefab/资源。元素证据计划使用用户要求的文档语言；如果项目没有批准的文档路径，就把计划保留在对话里或任务本地临时文件里，不要擅自新增项目 Markdown。写入生产 `.prefab` 文件前，需要先展示元素证据计划和结构化 prefab 规格；除非用户已经在当前任务中明确批准自动生成或重建，否则写 `.prefab` 前要先确认。证据缺失时，先从原型源码补证，再看浏览器实测、源资源、图集条目、已批准 prefab、View 绑定、配置、测试或用户明确消息；仍无法证明时，先问用户。

证据必须明确。“看起来相似”、“当前 prefab 已经这样做”、“另一个界面也是这样”或“差不多”都不是有效来源。必须区分标注浏览器实测、源码定义、继承沿用、生成资源和推断值。当前 prefab 只有在用户批准它作为来源，或它确实匹配原型/源码证据时，才可作为证据。

不要因为相似 prefab 目前这样做，就选择不同的图片、颜色、节点结构或状态语义。不要把视觉相似的项目 sprite、通用图集条目、按钮底图、面板底图、边框图或其他复用 UI 片段当成替代源资源。同项目样例只能证明序列化字段形状、组件布局、fileID/GUID 写法、嵌套 prefab 机制或 Unity 侧结构，不能证明应该选择样例里的视觉资源。如果源码证据显示边框、徽章、胶囊、标签、面板、卡片面等视觉容器，但没有已批准 sprite 或 texture，编辑前只能选择：绑定源码证明的资源、绑定计划中记录的生成资源、在视觉已烘焙进其他已批准资源时留空或透明，或询问用户确认准确替代资源。不要绑定无关图集 sprite 再靠 tint 近似源码效果。

图片和资源证据要优先查原型源码、DOM、CSS、JavaScript、原型引用资源和源码审阅后的截图，再看 Unity 侧候选美术目录或当前 prefab。不要只凭路径名、目录名或命名习惯把某个文件夹称为“源资源”或“权威源”；`art`、`source`、`raw`、`Z-main`、`Z-stage` 等名字只能说明它们是候选资源位置，必须有生成器、图集输入、导出清单、导入日志、配置、文档或用户明确说明才能确认为源链。证据计划里要把未证实的美术目录标为“候选美术/资源，源状态未证实”，并继续追踪生成链后再使用。原型缺少必要图片时，可以生成栅格资源，但计划里必须标记为生成资源，并记录它填补的原型缺口、生成所依据的视觉/布局/状态/交互约束、prompt 或输入、预期尺寸、图集名、sprite 名、放置位置和验证标准。不要把生成资源称为原型来源。

## Unity 输出约束

用 HTML/CSS/JavaScript 判断 UI 应显示什么、有哪些状态、行为如何变化；用 Unity 项目证据决定这些内容如何落到 prefab、资源、脚本、GUID/fileID 引用、可复用 Item、运行时绑定和校验里。如果网页证据与 Unity 生产规则不一致，保留网页证据并在报告中说明，但生成出的 Unity 结构要适配 Unity 规则。

生成或编辑 Unity UI 资产前：

- 写入资源前先找到 Unity 项目根目录，并读取 `ProjectSettings/ProjectVersion.txt`；如果 Unity 版本缺失，要说明生成风险更高并询问是否继续。
- 给目标 prefab 分类：源 prefab、生成 prefab、嵌套实例输出、导入资源输出或未知。
- 生成 prefab 必须先修源规格、转换器输入、美术输入或工具流程，再重新生成；不要把手改 YAML 当成主要修复方式。直接编辑 prefab 文件会受 Unity 版本、包、GUID 和组件序列化布局影响，风险较高；只有用户明确批准当前任务以 prefab 文件本身作为编辑面时，才允许直接编辑 prefab 文件。序列化输出以同项目样例和 Unity 校验为准。
- 任意包含 `MiniGameKit` 的项目路径默认视为框架拥有且只读，尤其是 `Assets/MiniGameKit/**`。只有用户在当前任务中明确批准具体文件变更时，才能新增、删除、修改、移动、格式化、生成或覆盖这些文件。方案看起来需要改框架文件时，先停止询问；优先使用业务层文件、配置、prefab 或已批准扩展点。
- 遵守项目已有框架加载边界：prefab、view、图集、贴图、字体、sprite 和其它非 Config 运行时资源走 `MiniFrameWork.AssetManager` 或其它已批准的框架加载器；有文档记录的动态业务状态 UI 图集 sprite 可以走 `MiniFrameWork.UIManager.GetSprite/TryGetSprite`。`Resources/config/` 下的 Config 资产不受这个 AssetManager-only 规则限制。不要在运行时或业务代码里生成或新增任何直接的非 Config `Resources.Load(...)` 调用，包括 prefab、UI、texture、font、sprite 加载。如果现有 `AssetManager` 或已批准框架加载器不支持所需非 Config 资源类型、路径或加载方式，先停下来问用户是否添加或扩展加载器，不要用 `Resources.Load` 兜底。
- 默认 UI sprite、颜色、Image Type、mask、字体、九宫切片、Item 内部结构必须先序列化进 prefab/资源。运行时 View 代码可以绑定数据、切换预置状态、为已记录的动态业务状态调用批准的图集 sprite API，或实例化完整 Item prefab；不能变成修补缺失默认视觉或运行时创建原始产品 UI 控件的兜底。
- 生成或编辑 prefab/资源前，先写元素证据计划和结构化 prefab 规格。
- 生成序列化字段前，先查同项目样例、资源 `.meta`、脚本 `.meta`、嵌套 prefab 样例。
- 生成前评估公共 prefab 或 Item prefab 抽取。
- 对生成或修改的 prefab 运行 `scripts/validate_unity_prefab.py`；有项目根且属于 UI prefab 工作时运行 `scripts/check_static_ui_compliance.py`；并在可行时尝试 Unity batchmode 导入校验。prefab validator 会检查 Unity object block、重复 fileID、缺失 GameObject 或 Transform-like object、悬空本地 fileID 引用、基本组件反向引用、父子引用、GUID 格式，以及可行时匹配 `.meta` 文件。UI scanner 会拦截 root-only View prefab、生成 View 的 `mask` 缺失 `UIStartView` Full 脚本、非 ASCII GameObject 名称、挂在 View 根节点上的可见或交互组件、内置字体 fallback、运行时构造原始 UI 控件，以及可疑的运行时视觉兜底。validator 或 scanner error 都按阻断处理，warning 要解决或作为风险报告。静态校验不能替代 Unity 导入校验。
- 生成图集前，先按项目图集规则从外部图集源目录推导 atlas short name，再扫描每个源 sprite 文件。所有小图文件名必须已经是 `<atlasShortName>@<functional_name>.png`，归一化后的 sprite 名必须唯一。`btn_primary.png` 这类裸名、裸名和前缀名混用的重复资源、或会生成无前缀 atlas 条目的命名，都按阻断处理。源输入修正并重新生成前，不要运行 TexturePacker，也不要保留生成图集输出。

## Unity 序列化与复用规则

生成序列化数据前，优先复制同项目对象的序列化形状，而不是发明字段。需要检查相似 prefab、场景对象、资源 `.meta`、脚本 `.meta`、嵌套 prefab 样例、prefab instance overrides、对象顺序、组件字段名、class ID、fileID 和外部引用。样例驱动复制只限于序列化机制；除非元素证据计划单独证明该视觉引用或用户明确批准，否则不要把样例对象的 sprite、texture、调色板、material、Image Type 或视觉状态复制到目标 prefab。

只把硬编码 Unity 知识用于低风险基础结构，例如 `GameObject`、`Transform`、`RectTransform`、`m_GameObject`、`m_Component`、`m_Father` 和 `{fileID, guid, type}` 引用形状。没有项目样例时，不要编造复杂 MonoBehaviour、UI、renderer、animation、physics 或 package-specific 序列化字段。新建本地 fileID 必须在 prefab 内唯一，并同步更新所有本地引用。资源和脚本引用必须来自目标 `.meta` 文件，不能发明 GUID。

文本字体引用必须序列化到 prefab、生成规格或明确的项目字体资源字段里。不要给产品 UI 添加 `Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf")`、`Resources.GetBuiltinResource<Font>("Arial.ttf")` 或其他 Unity 内置字体运行时 fallback。

源码具有视觉容器语义的文本控件，不能塌成裸 `Text`。如果 HTML/CSS、设计说明或截图显示某个 label 带背景、边框、圆角、padding、胶囊/徽章/标签行为、disabled 表面、hover 表面或状态装饰，应创建序列化视觉容器，例如带 `Image` 或 `RawImage` 的 `sp_xxx_bg` 或 `gr_xxx`，再把 `lb_xxx` 文本放在其下。运行时代码可以改文本或切换预制状态组，但不能负责创建缺失的徽章、胶囊或容器视觉。

这条容器规则不表示容器必须填写 `Source Image`。如果源码视觉是 CSS 绘制的，并且没有源码证明的 sprite/texture，也没有在证据计划中记录过的生成资源，应让容器的 sprite/texture 为空、视觉颜色透明，或把 CSS 视觉烘焙成证据计划记录过的生成贴图。不能因为节点上有 `Image` 组件，就自动从通用图集、按钮图、面板图、边框图或任何“可拉伸”的项目 sprite 里填一个资源。

如果多个目标 prefab 共享结构、组件、资源组、命名语义或维护目的，写文件前先评估公共 prefab 抽取。信号包括重复层级/组件、重复资源引用、`Common`、`Shared`、`Base`、`Template`、`ItemCell`、`ButtonBase`、`TongYong`、`JiChu`、`MoBan` 等命名语义，以及能降低维护成本且不隐藏关键差异的复用。抽取前先列出公共 prefab 名称和路径、抽取原因、依赖它的 prefab、保留为 instance override 的字段和风险；确认后先生成公共 prefab，再用同项目样例生成依赖 prefab 的嵌套实例。

## 默认流程

1. 读取项目规则，包括 `AGENTS.md`、详细文档，以及存在时的 `SubDoc/*.md`。
2. 识别并读取源码输入：HTML、CSS、JavaScript、配置/数据文件、资源清单、生成器输入，以及目标 UI 状态相关的状态/渲染代码。必须在打开渲染网页或截图前完成。
3. 先写元素证据计划和结构化 prefab 规格，再做转换或生成决策。
4. 建立 Unity 输出约束：项目根、Unity 版本、prefab 分类、框架路径边界、资源/运行时静态边界、校验计划。
5. 涉及资源或图集工作前，先确认 TexturePacker 已安装；缺失则停止。
6. 源码审阅和计划完成后，才在浏览器中渲染 HTML，并收集 `getBoundingClientRect()` 和 computed styles。
7. 截图只能在源码审阅后作为视觉验证、不一致证据或缺口证据使用。
8. 将有源码依据并经浏览器验证的布局和原型状态逻辑转换为结构化 UI 描述。
9. 将图片拆分为大图和小图，小图走项目图集流程。
10. 生成 `UIXXXView` 前，检查 `Assets/Resources/ui/UIStartView.prefab`，并把它作为标准 View 结构。
11. 在 `Assets/Resources/ui/` 下生成或重建 `UIXXXView` 和需要的 `UIXXXItem`。
12. 编辑 View 代码前，先校验 prefab/资源结果；运行时代码只能消费已完成的 prefab 节点和完整 Item prefab。
13. 存在匹配的 `UIXXXView.cs` 时挂到根节点，使用 UGUI 组件，并保留项目命名规则。
14. 输出生成报告，列出文件、资源、推断、缺失项、校验结果、跳过项和 Unity 内人工检查。

## 强制默认规则

- UI prefab 和 Item 默认放在 `Assets/Resources/ui/`；除非用户明确改规则，不创建按模块拆分的 UI prefab 目录。
- `UIStartView.prefab` 是生成 View 的标准基准：根对象命名为 `UIXXXView`，根节点挂匹配的 `UIView` 脚本，包含全屏拉伸且保留样例 Full 脚本的 `mask` 背景/遮罩层，以及全屏拉伸的 `view` 内容容器。
- prefab 根节点保持轻量，通常只放 `RectTransform` 和必要 View/controller 脚本。Image、Text、Button、ScrollRect、layout group 等可见或交互控件放在命名子节点。
- 默认 UI 视觉必须先序列化进 prefab/资源：sprite、颜色、Image Type、mask、raycast、字体、九宫切片、Item 内部结构。不要在 View 代码里用运行时 `SetSprite`、直接 `image.sprite =`、直接 `image.color =`、内置字体 fallback 或临时资源加载来修补默认视觉。
- 重复 UI 单元要抽为 `UIXXXItem.prefab`、嵌套/静态 prefab 实例，或静态布局容器下的 Item prefab 池。三个及以上重复实例是强制抽取信号；两个复杂或可复用实例也应抽取，除非规格里记录明确例外。
- 使用统一宽度缩放：`scale = 720 / htmlViewportWidth`。
- 高度视为自适应视口空间，不使用第二套独立高度缩放。
- flex、文本、margin、padding、transform、定位节点等必须以浏览器 computed layout 为准。
- 保留 JavaScript 原型驱动的 UI 状态和类型渲染规则，例如卡片变体、disabled、冷却标签、刷新/广告倒计时、弹窗暂停、空状态文案。
- 视觉堆叠按 computed `z-index` 排序；`z-index` 相同时保留 DOM 顺序。
- 不静默发明业务行为。按钮回调、静态 Item 引用、脚本暴露关系不清楚时，要询问或在报告中说明。

## 图集输入与输出门槛

项目图集从外部文件夹生成时，必须从输出图集名推导 sprite 前缀。例如 `Z-common@...` 会生成 `ui_atlas_common`，因此该文件夹下每个源 sprite 都必须命名为 `common@...`。

不要把 TexturePacker、Unity 导入或 Inspector 显示当成命名修复器。图集工具会把源 sprite 名原样写入 `.tpsheet` 和 `.png.meta`；因此裸源文件名会生成裸 atlas 条目。构建前，如果任何源 sprite 缺少预期前缀，或同时存在 `name.png` 与 `<prefix>name.png`，或归一化后的 sprite 名重复，必须让计划失败并先修源输入。

构建或检查图集后，必须检查生成的 `.tpsheet` 和 `.png.meta`。`ui_atlas_<shortName>` 下每个 sprite 名都必须以 `<shortName>@` 开头；`nameFileIdTable` 条目也必须符合这个规则；Unity id table 以外的重复 sprite 名按阻断处理。如果项目存在 `UiAtlasNamingTests`，使用图集条目前必须运行该测试或等价静态检查。

## UIStartView 标准结构

生成或重建 View prefab 前，需要检查：

```text
Assets/Resources/ui/UIStartView.prefab
Assets/Scripts/Runtime/Start/UIStartView.cs
```

`UIStartView` 代表本项目生成 View 的标准结构：

- 根 GameObject 名称与 prefab/class 名一致，例如 `UIXXXView`。
- 根节点使用全屏拉伸 `RectTransform`。
- 根节点在存在匹配脚本时挂载 `UIXXXView.cs`。
- 第一个子节点是 `mask`，它是背景/遮罩层。保留它的全屏拉伸、透明 Image，以及样例上的 FULL 脚本；该脚本用于刘海屏反向填充适配，不是普通可视内容布局。
- 第二个子节点是 `view`，它是全屏拉伸的内容容器，常规生成的可见 UI 控件放在 `view` 下面。
- 当存在 `view` 容器时，不要把生成的可视控件直接放在根节点下。
- 除非用户明确要求不同结构，不要把背景覆盖、弹窗遮罩行为或刘海屏反向填充逻辑从 `mask` 移出去。
- 可复用列表行、格子、固定网格卡片等应保持为独立 Item prefab，不要折进 View 根结构。

创建匹配的 `UIXXXView.cs` 时，遵循 `UIStartView.cs` 的注册模式：继承 `UIView`，提供静态 `RegisterView()`，创建 `UIViewInfo`，设置 `viewName`、`canvasType`、`viewType`，并调用 `UIManager.Instance.RegisterView(info)`。

## 结构化规格与 UI 证据

生成 prefab 文件或 UI 资源前，先准备结构化规格，至少包含 prefab 名称和输出路径、source/generated 分类、拥有它的源/工具/输入、GameObject 层级、`UIStartView` 根/mask/view 使用方式、root object policy、Transform 或 RectTransform、anchor、sibling order、mask、layer、组件和关键字段、资源和脚本 GUID 来源、tag/layer/active/static flags、公共 prefab/Item 抽取决策、校验计划。

每个创建、移动、删除、重绑、视觉变化、状态切换或运行时代码处理的 UI 元素都必须在元素证据计划中说明稳定 GameObject 名、父级路径、来源和理由。视觉、布局、状态、交互、运行时/静态边界必须标出来源，推断不能写成事实。

不要仅凭路径名把某个目录或文件称为权威源。`art`、`source`、`raw`、`Z-main` 等目录名只能说明它们是候选资源位置，必须有生成器、图集输入、导出清单、导入日志、配置、文档或用户明确说明才能确认为源。

## 完成前检查

完成前至少确认：

- 元素证据计划已在转换/生成决策前写出。
- 结构化 prefab 规格已在 prefab/资源编辑前写出。
- 除非用户已明确批准当前任务自动生成或重建，否则生产 `.prefab` 写入前已展示结构化规格并获得确认。
- 相关 HTML/CSS/JavaScript/配置/资源源码输入已在打开渲染网页、运行浏览器测量或使用截图前读取。
- `UIXXXView.prefab` 已在 `Assets/Resources/ui/` 下创建或重建。
- 需要的 `UIXXXItem.prefab` 已创建。
- 新 Unity 文件有 `.meta`。
- 存在匹配 `UIXXXView.cs` 时已挂到根节点。
- 目标 prefab 已完成 source/generated 分类。
- 生成 prefab 已先修源/输入/工具再重新生成。
- 直接编辑 prefab 文件只发生在用户明确批准该文件作为当前编辑面之后。
- TexturePacker 已在图集工作前确认。
- 大图放在 `Assets/Resources/tex/`。
- 小图已按项目图集流程分组并打包。
- 图集源小图文件名已按目标图集 short name 使用 `<atlasShortName>@<functional_name>.png`，没有裸名、裸名/前缀名混用或归一化重复。
- 生成的 `.tpsheet` 和 `.png.meta` 中所有 `ui_atlas_<shortName>` sprite 条目及 `nameFileIdTable` 条目都以 `<shortName>@` 开头；项目存在 `UiAtlasNamingTests` 时已运行或执行了等价静态检查。
- Image、RawImage、Text 字体引用可解析。
- 每个 UI Text 字体引用都指向已分配的项目字体资源，运行时代码没有 `Resources.GetBuiltinResource<Font>`、`LegacyRuntime.ttf`、`Arial.ttf` 等内置字体 fallback。
- 资源身份由原型/源码证据、生成资源记录、配置、图集条目或用户明确指令证明；没有把路径名当证明，也没有用视觉相似的项目 sprite、通用图集条目、按钮/面板/边框底图等当替代源资源。
- 同项目样例只用于序列化机制或已批准的 Unity 结构，没有把样例视觉资源、颜色、材质、Image Type 或状态语义当成目标视觉证据。
- 资产和脚本 GUID 来自 `.meta` 或同项目样例，本地 fileID 在 prefab 内唯一且引用一致。
- 默认 UI 视觉已序列化进 prefab/资源。
- 框架加载边界未被破坏：非 Config 运行时资源走 `AssetManager` 或其它已批准框架加载器，没有新增直接的非 Config `Resources.Load(...)` 调用；`Resources/config/` 下的 Config 资产按例外处理；加载器缺少非 Config 资源能力时，已先询问用户是否添加 API 或扩展加载器。
- HTML 转换、解析器、截图、DOM 映射和资源推断结果已与 Unity 资源身份、序列化字段、GUID/fileID 引用、运行时/静态边界、Item 抽取和校验要求对齐。
- 每个受影响 UI 元素的证据已回答：为什么存在、为什么使用对应图片/颜色/字体/材质/图集条目、为什么使用对应位置/尺寸/anchor/sibling order/mask/层级、有哪些状态和序列化变化、交互由哪个 View/model/event 绑定负责、哪些是静态数据而哪些允许运行时处理、是否存在推断或证据缺失。
- 使用了原型源码 DOM/CSS/JavaScript 和浏览器 computed layout，且浏览器/截图证据发生在源码审阅之后。
- 生成的 View 结构匹配 `UIStartView.prefab`：全屏拉伸根节点，`mask` 作为背景/遮罩层并保留 FULL 刘海屏反向填充脚本，`view` 作为内容容器。
- 根节点保持轻量，不包含可见或交互控件，除非用户或同项目样例明确要求。
- 每个可见控件都是稳定英文命名的子节点；除非用户或同项目样例明确要求，不要把可见控件放在 prefab 根节点上。
- 文本 RectTransform 足够，避免裁剪。
- 具有源码视觉容器语义的文本控件已生成为视觉容器加子文本，没有塌成裸 `Text`。
- 没有源码证明或计划记录的生成 sprite 时，styled visual container 没有被通用图集、按钮图、面板图、边框图或可拉伸项目 sprite 自动填充。
- ScrollView 的 Content、Viewport、Item 模板结构合理。
- 兄弟节点顺序遵循 z-index 和 DOM 顺序。
- 重复 UI 单元已抽为 Item prefab、嵌套/静态实例或 Item prefab 池，或者规格里记录了明确例外。
- 已运行 `scripts/validate_unity_prefab.py` 校验生成或修改的 prefab。
- 有项目根且属于 UI prefab 工作时，已运行 `scripts/check_static_ui_compliance.py`，并覆盖 root-only View prefab、生成 View 的 `mask` 缺失 `UIStartView` Full 脚本、直接的非 Config `Resources.Load(...)` 调用、非 ASCII GameObject 名称、View 根节点可见或交互组件、内置字体 fallback、运行时构造原始 UI 控件和可疑运行时视觉兜底检查。
- 可行时已尝试 Unity batchmode 导入校验，并检查 YAML、缺脚本、导入错误、prefab 加载失败、缺 GUID。
- View 运行时代码没有用临时 sprite/color/font/resource fallback 逻辑修补缺失的默认 UI 视觉。
- 静态容器已配置完成时，允许运行时实例化完整 `UIXXXItem.prefab`；不允许运行时构造该 Item 的原始控件。

## 必须报告

完成报告需要列出：生成的 prefab、source/generated 分类和拥有源/工具、生成或移动的资源、不支持的 CSS、栅格化为 PNG 的 CSS 视觉、自动生成或重命名节点、缺失源图片、推断组件类型、疑似九宫切片但未确认 slice 数据的资源、提升为 Item prefab 的重复组、因属于 ScrollView 而未静态引用的 Item prefab、抽取的公共 prefab 及引用它的 prefab、静态 prefab validator 结果、静态 UI 合规扫描结果、Unity batchmode 结果或跳过原因、资产和脚本 GUID/fileID 依赖、跳过的校验及原因、仍需人工确认的问题、Unity 内仍需人工检查的问题，以及截图和原型逻辑/浏览器测量不一致的地方。出现证据冲突时，按用户明确指令、项目规则、Unity 输出约束、同项目样例、原型/浏览器证据、截图证据的顺序处理。

## 0.4.0 质量门禁同步说明

本版本新增“布局质量门禁”：生成 prefab 不等于转换完成，必须证明 Unity 输出和源代码驱动的 HTML 原型足够接近，或者把差异作为未完成工作报告。

转换完成前应记录每个关键元素的浏览器 `getBoundingClientRect()`、生成或导出的 Unity rect、位置偏差、尺寸偏差、视觉资源证据和样式支持状态。默认阈值为位置偏差不超过 4 个缩放像素，尺寸偏差不超过 2%。项目或用户给出更严格阈值时，以更严格阈值为准。

当存在对比 JSON 时，运行：

```text
python scripts/compare_layout_quality.py <quality-json>
```

JSON 中的元素建议包含 `id`、`html_rect`、`unity_rect`、`visual_required`、`asset_status`、`style_required`、`style_status`。关键视觉元素如果缺少资源证据，或者只标记为 missing、unknown、inferred、placeholder、substitute，应阻断完成，除非用户明确接受该妥协。关键样式如果缺少支持或未实现，也应阻断完成。

如果可以自动截取 Unity 渲染图，应把 Unity 截图与浏览器截图或源截图做 overlay/diff。像素级完全一致不是硬要求，但明显的位置错误、缺图、层级错误、裁剪、字体错误或 CSS 视觉缺失，都应修复或报告为未完成工作。

## 停止条件

遇到以下情况要先停止并询问用户：项目规则冲突、TexturePacker 缺失、无法识别 Unity 项目根或 Unity 版本且用户未批准高风险继续、HTML 设计尺寸缺失且无法安全推断、关键 UI 证据缺失、生成 prefab 的拥有源/工具/输入无法识别、目标 prefab 已存在但用户没有要求重建、命名或 Item 抽取会造成不稳定业务引用、必需美术资源缺失、方案需要修改任意包含 `MiniGameKit` 的项目路径但用户未批准具体文件。
