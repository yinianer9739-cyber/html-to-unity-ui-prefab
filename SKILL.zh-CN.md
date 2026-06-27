# HTML 转 Unity UI 预制体技能中文说明

本文档是 `SKILL.md` 及其 `references/*.md` 的中文同步说明。英文 `SKILL.md` 是技能触发和执行时的主文档；维护本技能时，如果英文主文件或引用文档里的行为、流程、项目结构规则、校验要求、完成报告要求发生变化，必须在同一次变更中同步更新本文档。

## 核心规则

将 HTML/CSS 转成 Unity UGUI 预制体时，必须先通过浏览器渲染拿到真实布局数据，不能只靠源码文本猜测布局。生成或编辑 Unity 文件前，必须遵守目标项目的 `AGENTS.md` 和适用的子规则。

## 必读文档

- 执行流程见 `references/conversion-workflow.md`。
- 完成前检查见 `references/output-checklist.md`。

## 默认流程

1. 读取项目规则，包括 `AGENTS.md`、详细文档，以及存在时的 `SubDoc/*.md`。
2. 涉及资源或图集工作前，先确认 TexturePacker 已安装；缺失则停止。
3. 在浏览器中渲染 HTML，并收集 `getBoundingClientRect()` 和 computed styles。
4. 将渲染结果转换为结构化 UI 描述。
5. 将图片拆分为大图和小图，小图走图集流程。
6. 生成 `UIXXXView` 前，检查 `Assets/Resources/ui/UIStartView.prefab`，并把它作为标准 View 预制体结构。
7. 在 `Assets/Resources/ui/` 下生成或重建 `UIXXXView` 和需要的 `UIXXXItem`。
8. 如果存在匹配的 `UIXXXView.cs`，挂载到根节点；使用 UGUI 组件，并保留项目命名规则。
9. 输出生成报告，列出创建文件、不支持的 CSS、推断节点、缺失资源和需要人工检查的内容。

## 强制默认规则

- UI 预制体和 Item 默认放在 `Assets/Resources/ui/`；除非用户明确改规则，不创建按模块拆分的 UI 预制体目录。
- `UIStartView.prefab` 是生成 View 的标准基准：根对象命名为 `UIXXXView`，根节点挂匹配的 `UIView` 脚本，包含全屏拉伸的 `mask` 背景/遮罩层，以及全屏拉伸的 `view` 内容容器。
- 使用统一宽度缩放：`scale = 720 / htmlViewportWidth`。节点尺寸、居中坐标和字号都使用同一个缩放值。
- 高度视为自适应视口空间，不使用第二套独立高度缩放。
- flex、文本、margin、padding、transform、定位节点等必须以浏览器 computed layout 为准。
- 视觉堆叠先按 computed `z-index` 排序；`z-index` 相同时保留 DOM 顺序。
- 不静默发明业务行为。按钮回调、静态 Item 引用、脚本暴露关系不清楚时，要询问或在报告中说明。
- 给其他 AI 工具使用的 HTML 编写规则是单独交接文档，不属于本技能必需流程。

## UIStartView 标准结构

生成或重建 View 预制体前，需要检查：

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
- 可复用列表行、格子等应保持为独立 Item prefab，不要折进 View 根结构。

如果创建匹配的 `UIXXXView.cs`，要遵循 `UIStartView.cs` 的注册模式：继承 `UIView`，提供静态 `RegisterView()`，创建 `UIViewInfo`，设置 `viewName`、`canvasType`、`viewType`，并调用 `UIManager.Instance.RegisterView(info)`。

## 完成前检查

完成前至少确认：

- `UIXXXView.prefab` 已在 `Assets/Resources/ui/` 下创建或重建。
- 需要的 `UIXXXItem.prefab` 已创建。
- 新 Unity 文件有 `.meta`。
- 存在匹配 `UIXXXView.cs` 时已挂到根节点。
- TexturePacker 已在图集工作前确认。
- 大图放在 `Assets/Resources/tex/`。
- 小图已按项目图集流程分组并打包。
- Image、RawImage、Text 字体引用可解析。
- 使用了浏览器 computed layout 和统一宽度缩放。
- 生成的 View 结构匹配 `UIStartView.prefab`：全屏拉伸根节点，`mask` 作为背景/遮罩层并保留 FULL 刘海屏反向填充脚本，`view` 作为内容容器。
- 文本 RectTransform 足够，避免裁剪。
- ScrollView 的 Content、Viewport、Item 模板结构合理。
- 兄弟节点顺序遵循 z-index 和 DOM 顺序。

## 必须报告

完成报告需要列出：

- 生成的 prefab。
- 生成或移动的资源。
- 不支持的 CSS。
- 被栅格化为 PNG 的 CSS 视觉效果。
- 自动生成或重命名的节点。
- 缺失源图片。
- 推断组件类型的节点。
- 疑似九宫切片但未确认 slice 数据的资源。
- 被提升为 Item prefab 的重复组。
- 因属于 ScrollView 而未静态引用的 Item prefab。
- 仍需人工确认的问题。

## 停止条件

遇到以下情况要先停止并询问用户：

- 项目规则冲突。
- TexturePacker 缺失。
- HTML 设计尺寸缺失且无法安全推断。
- 目标 prefab 已存在，但用户没有要求重建。
- 命名或 Item 抽取会造成不稳定的业务引用。
- 必需美术资源缺失。
