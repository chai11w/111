import argparse
from pathlib import Path


def build_record(time: str, user_input: str, model_output: str, changed_files: list[str]) -> str:
    changed_files_text = "\n".join(changed_files) if changed_files else "无"
    return f"""### {time}

**用户输入**

```
{user_input}
```

**模型输出**

```
{model_output}
```

**本轮修改文件**

```
{changed_files_text}
```
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="追加写入 codex过程记录.md")
    parser.add_argument("--record-path", default=".agents/codex过程记录.md")
    parser.add_argument("--time", required=True)
    parser.add_argument("--user-input", required=True)
    parser.add_argument("--model-output", required=True)
    parser.add_argument("--changed-file", action="append", default=[])
    return parser


def main() -> None:
    args = build_parser().parse_args()
    record_path = Path(args.record_path)
    record = build_record(args.time, args.user_input, args.model_output, args.changed_file)
    with record_path.open("a", encoding="utf-8", newline="\n") as file:
        file.write("\n")
        file.write(record)


if __name__ == "__main__":
    main()
