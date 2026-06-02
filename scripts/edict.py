#!/usr/bin/env python3
"""
三省六部 · CLI 技能脚本 (支持双语)
用法: python3 edict.py '{"task":"...", "priority":"normal", "lang":"zh"}'

两种运行模式：
1. 有 Claude CLI → 调用真实 LLM，各Agent独立思考
2. 无 Claude CLI → 输出三省六部思维框架模板，供宿主AI参考执行

参数:
  task      - 任务描述 (必填)
  priority  - 优先级: high/normal/low (默认 normal)
  lang      - 语言: zh/en (默认 zh)
"""
import sys
import json
import os
import io
import pathlib
import subprocess
import shutil

# Windows UTF-8 输出兼容
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

# 查找 sansheng 项目目录（含 SOUL.md 人格文件）
_POSSIBLE = [
    pathlib.Path.home() / '.gemini' / 'antigravity' / 'scratch' / 'sansheng',
    pathlib.Path(os.getenv('SANSHENG_HOME', '')) if os.getenv('SANSHENG_HOME') else None,
]
SANSHENG_DIR = next((p for p in _POSSIBLE if p and p.exists()), None)

# 检测 Claude CLI 是否可用
HAS_CLAUDE = shutil.which('claude') is not None

# Agent 流程定义
FLOW = [
    ('taizi',    '太子',   '接旨分拣'),
    ('zhongshu', '中书省', '方案起草'),
    ('menxia',   '门下省', '审议把关'),
    ('shangshu', '尚书省', '调度派发'),
]

DEPARTMENTS = {
    'hubu':    ('户部', '数据分析、资源管理、预算统计'),
    'libu':    ('礼部', '文档撰写、规范制定、沟通协调'),
    'bingbu':  ('兵部', '工程开发、代码实现、技术方案'),
    'xingbu':  ('刑部', '安全审计、合规检查、风险评估'),
    'gongbu':  ('工部', '基础设施、部署运维、工具搭建'),
    'libu_hr': ('吏部', '人事协调、团队管理、资源调配'),
}


def section(title):
    """输出分隔线"""
    print(f"\n{'='*56}")
    print(f"  {title}")
    print(f"{'='*56}\n")


def load_soul(agent_id):
    """加载 Agent 的 SOUL.md"""
    if SANSHENG_DIR:
        soul_path = SANSHENG_DIR / 'agents' / agent_id / 'SOUL.md'
        if soul_path.exists():
            return soul_path.read_text(encoding='utf-8')
    return None


def probe_claude():
    """探测 Claude CLI 是否可正常调用（模型可用）"""
    try:
        result = subprocess.run(
            ['claude', '-p', 'reply OK', '--output-format', 'text', '--bare'],
            capture_output=True, text=True, timeout=15, encoding='utf-8'
        )
        if result.returncode == 0 and result.stdout.strip():
            return True
        # 检测常见错误
        output = (result.stdout or '') + (result.stderr or '')
        if 'model' in output.lower() and ('not exist' in output.lower() or 'issue' in output.lower()):
            sys.stderr.write(f"[探测] 当前模型不可用: {output.strip()[:150]}\n")
            return False
    except Exception:
        pass
    return False


def call_claude(system_prompt, user_message):
    """通过 Claude CLI 调用 LLM"""
    try:
        cmd = ['claude', '-p', user_message, '--system-prompt', system_prompt,
               '--output-format', 'text', '--bare']
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120, encoding='utf-8'
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        # 调试信息
        output = (result.stdout or '') + (result.stderr or '')
        if output.strip():
            sys.stderr.write(f"[Claude CLI] {output.strip()[:200]}\n")
    except subprocess.TimeoutExpired:
        sys.stderr.write("[Claude CLI] 调用超时\n")
    except Exception as e:
        sys.stderr.write(f"[Claude CLI] 异常: {e}\n")
    return None


def run_with_llm(task, priority):
    """使用真实 LLM 执行三省六部流转"""
    context = f"旨意: {task}\n优先级: {priority}"
    accumulated = ""

    for agent_id, name, role in FLOW:
        section(f'{name} . {role}')
        soul = load_soul(agent_id) or f"你是{name}，负责{role}。"
        message = f"{context}\n\n前序处理记录:\n{accumulated}" if accumulated else context
        reply = call_claude(soul, message)
        if reply:
            print(reply)
            accumulated += f"\n[{name}]: {reply[:500]}\n"
        else:
            print(f"(LLM 调用失败，跳过 {name})")

    # 尚书省派发后，判断需要哪些部门执行
    section('六部 . 执行')
    for dept_id, (dept_name, dept_desc) in DEPARTMENTS.items():
        soul = load_soul(dept_id) or f"你是{dept_name}尚书，负责{dept_desc}。"
        message = f"{context}\n\n执行方案:\n{accumulated}\n\n请根据你的职责，输出你负责部分的实际成果。如果此任务与你的职责无关，简短说明即可。"
        reply = call_claude(soul, message)
        if reply and '与本部无关' not in reply and '不涉及' not in reply and len(reply) > 20:
            section(f'{dept_name} . 执行')
            print(reply)
            accumulated += f"\n[{dept_name}]: {reply[:300]}\n"

    section('最终成果 . 汇总')
    soul = "你是太子，负责将各部门成果汇总为最终报告，呈给皇上。要求：精炼、完整、可直接使用。"
    reply = call_claude(soul, f"旨意: {task}\n\n各部门执行记录:\n{accumulated}\n\n请汇总为最终成果报告。")
    if reply:
        print(reply)
    else:
        print(f"旨意「{task}」已完成全流程处理。")


def run_framework_mode(task, priority):
    """无 LLM 时，输出思维框架指引，供宿主AI参照执行"""
    section('三省六部 . 任务处理框架')
    print(f"""请按以下流程处理此任务：

旨意: {task}
优先级: {priority}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第一步: 太子 - 接旨分拣】
- 判断任务类型和复杂度
- 提取核心需求、约束条件、交付物
- 识别涉及的部门

【第二步: 中书省 - 起草方案】
- 拆解为具体的子任务（每个要有明确输入/输出）
- 标注负责部门
- 预估资源和风险
  注意: 方案必须具体，不能是"需求分析与规划"这种空话

【第三步: 门下省 - 审议】
- 检查方案覆盖度、可行性、分工合理性
- 不合格就封驳修改

【第四步: 尚书省 - 派发】
- 确定执行顺序和依赖关系
- 明确各部门的输入/输出

【第五步: 六部执行】
各部门按分工实际完成任务，输出具体成果:
  - 户部: 数据分析、资源清单、成本估算
  - 礼部: 文档全文、邮件草稿、会议纪要
  - 兵部: 代码实现、技术方案、架构设计
  - 刑部: 安全审查、风险清单、合规报告
  - 工部: 部署方案、环境配置、自动化脚本
  - 吏部: 人员分工、团队建议

【第六步: 汇总】
- 整合各部门成果为最终交付物

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请你现在按照上面的流程，依次扮演各个角色来处理这个任务。
每个角色都要输出**实际内容**，不要空话。""")


def main():
    if len(sys.argv) < 2:
        print("三省六部 . CLI 技能 (支持双语)")
        print("")
        print("用法: python3 edict.py '<JSON>'")
        print("")
        print("参数:")
        print("  task      - 任务描述 (必填)")
        print("  priority  - 优先级: high/normal/low (默认 normal)")
        print("  lang      - 语言: zh/en (默认 zh)")
        print("")
        print("示例:")
        print("  python3 edict.py '{\"task\":\"帮我写一份项目周报\"}'")
        print("  python3 edict.py '{\"task\":\"Design technical solution for user points system\",\"priority\":\"high\",\"lang\":\"en\"}'")
        print("  python3 edict.py '{\"task\":\"润色提示词：一只猫在窗台看雨\"}'")
        print("")
        print(f"Claude CLI: {'已检测到' if HAS_CLAUDE else '未检测到 (将使用框架模式)'}")
        print(f"SANSHENG_DIR: {SANSHENG_DIR or '未找到'}")
        sys.exit(0)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        sys.exit(1)

    task = params.get('task', '')
    if not task:
        print("错误: 缺少 task 参数")
        sys.exit(1)

    priority = params.get('priority', 'normal')
    lang = params.get('lang', 'zh')  # 默认中文

    # 如果是英文模式，导入英文版本的函数
    if lang == 'en':
        try:
            from edict_en import run_with_llm, run_framework_mode
            print("[Language: English]")
        except ImportError:
            print("[Warning: English version not found, using Chinese version]")
            lang = 'zh'

    if HAS_CLAUDE:
        print("[探测 Claude CLI 模型可用性...]")
        if probe_claude():
            print("[模式: LLM调度 | Claude CLI]")
            run_with_llm(task, priority)
        else:
            print("[Claude CLI 模型不可用，切换到框架模式]")
            print("[提示: 请运行 'claude --model' 选择可用模型]")
            print("")
            run_framework_mode(task, priority)
    else:
        print("[模式: 框架指引 | 无LLM]")
        run_framework_mode(task, priority)


if __name__ == '__main__':
    main()
