import ast
import sys
from pathlib import Path

SETTINGS_PATH = Path(__file__).resolve().parents[1] / "projectBPL" / "settings.py"


def extract_assignments():
    source = SETTINGS_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    values[target.id] = ast.get_source_segment(source, node.value)
    return values


def main():
    assignments = extract_assignments()
    findings = []

    for key in ("SECRET_KEY", "DEBUG", "ALLOWED_HOSTS", "CORS_ALLOW_ALL_ORIGINS"):
        value = assignments.get(key, "")
        if "os.getenv" not in value:
            findings.append(f"`{key}` should be environment-aware.")

    if findings:
        print("Security check failed:")
        for item in findings:
            print(f"- {item}")
        sys.exit(1)

    print("Security check passed: critical settings are environment-aware.")


if __name__ == "__main__":
    main()
