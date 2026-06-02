# 🛡️ Claude Code 技能合集 (Skills Library)

欢迎来到我的 Claude Code 技能库！本项目收录了一系列针对 **Claude CLI (如小龙虾、Claude Code)** 优化的结构化 AI 技能。

这些技能通过增强 AI 的思维链（CoT）和多 Agent 协作能力，显著提升复杂任务的处理质量。

---

**[📖 English Version / 英文版](README.md)**

---

## 🛠️ 技能列表 (Skills List)

### 1️⃣ 深度提示词创作助手 (Prompt Deep Creator)
<details>
<summary><b>点击展开：将模糊想法转化为专业 Prompt 🚀</b></summary>

#### 🔹 功能核心
将零散、口语化、甚至模糊的创作想法，转化为高质量、结构清晰、可直接使用的正式提示词。
- **提取要素**：自动识别核心目标、受众、风格及约束条件。
- **结构化输出**：生成包含角色设定、任务背景、核心任务及禁止事项的标准模板。
- **智能追问**：当输入信息不足时，主动引导补充关键要素。

#### 🔹 适用场景
- **写作创作**：技术博客、深度长文、科普文章。
- **方案设计**：商业方案、产品需求文档 (PRD)。

#### 🔹 安装方法
1. 下载 `prompt-deep-creator.zip` 并解压。
2. 将 `skill.md` 内容复制到你的 Claude 预设指令中，或将解压后的文件夹放入软件的 `skills` 目录。
3. 如果使用 `skills.json` 管理，请添加对应路径。
</details>

---

### 2️⃣ 三省六部 · 多 Agent 思维框架 (Sansheng)
<details>
<summary><b>点击展开：通用任务处理行政体系 ⚔️</b></summary>

#### 🔹 功能核心
将任何复杂任务按照"分拣→规划→审议→派发→执行→汇总"的严格流程进行结构化处理。
- **太子 · 接旨分拣**：判断任务类型并提取核心需求。
- **中书省 · 起草方案**：制定具体、可执行的方案（拒绝空话）。
- **门下省 · 审议把关**：**核心特色**，不合格的方案会被直接"封驳"。
- **六部 · 实际执行**：兵部(技术)、礼部(文档)、户部(数据)等部门实际产出成果。

#### 🔹 安装方法
1. 下载 `The Three Provinces and Six Ministries System AI Agent (win)_skill_v1.0.zip` 并解压。
2. **CLI 模式**：
   - 确保安装了 Python 3。
   - 在终端运行 `python3 edict.py '{"task":"任务内容"}'` 即可触发流转。
3. **Web 看板模式**：
   - 运行 `python3 scripts/serve.py` 启动可视化界面（访问 127.0.0.1:7891）。
</details>

---

## 📥 通用安装与配置 (Installation)

针对主流 Claude 终端工具，你可以按照以下方式集成：

### 方法 A：目录集成（推荐）
1. 找到你的软件安装目录（例如 `~/.gemini/antigravity/scratch/`）。
2. 将对应的技能文件夹拷贝至 `skills/` 目录下。
3. 重启 Claude CLI，尝试输入"使用三省六部处理..."或"帮我深度创作一个提示词"。

### 方法 B：配置文件关联
在你的 `skills.json` 中添加如下配置：
```json
{
  "skills": [
    {
      "name": "sansheng",
      "path": "./skills/sansheng/SKILL.md"
    },
    {
      "name": "prompt-deep-creator",
      "path": "./skills/prompt-deep-creator/skill.md"
    }
  ]
}
```

---

## 📄 文档

- **[English Documentation / 英文文档](README.md)**
- **[中文文档](README_CN.md)** (当前)

---

*由 Claude Code Skills Hub v1.0.0 生成*
