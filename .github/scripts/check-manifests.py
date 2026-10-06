"""プラグインの JSON と案内の文書を検査する（CI 用）。

- リポジトリの JSON がすべて読めること
- Codex 用（portable）の plugin.json・mcp.json が Agent Plugins 1.0.0 の schema に合うこと
- Codex のマーケットプレイスの source.path が、リポジトリの根から中のディレクトリに解決できること
- MCP サーバーの URL が完全な URL（末尾スラッシュなし）で、接続の設定に client ID・秘密・ヘッダーを入れないこと
- README の導入コマンドがマーケットプレイスの名前と合うこと、ChatGPT の案内に完全な URL があること
- 秘密鍵・トークン・メールアドレスを含まないこと

schema は .github/schemas/ に置いた写し（https://agent-plugins.org/schemas/1.0.0/）を使い、検査のときに外へ取りに行かない。
"""

import json
import pathlib
import re
import sys

from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / ".github/schemas/agent-plugins-1.0.0"

# プラグインの名前 → 接続先の MCP サーバー（Claude 用・Codex 用で同じ URL を使う）
MCP_URLS = {"sighted-stg": "https://mcp.stg.sighted-aeo.com/mcp"}

errors = []


def error(path, message):
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        error(path, f"JSON として読めません: {e}")
        return None


def validate(path, schema_file):
    data = load(path)
    if data is None:
        return None
    schema = json.loads((SCHEMAS / schema_file).read_text(encoding="utf-8"))
    for e in sorted(Draft202012Validator(schema).iter_errors(data), key=str):
        where = "/".join(map(str, e.absolute_path)) or "(root)"
        error(path, f"schema に合いません: {where}: {e.message}")
    return data


def check_servers(path, servers, plugin_name, transport):
    expected = MCP_URLS.get(plugin_name)
    if expected is None:
        error(path, f"{plugin_name} の MCP の URL を MCP_URLS に足してください")
    if not isinstance(servers, dict) or not servers:
        error(path, "mcpServers が要ります")
        return
    for name, server in servers.items():
        if not isinstance(server, dict) or set(server) != {"type", "url"}:
            error(path, f"{name} は type と url だけにします（client ID・秘密・ヘッダーを入れない）")
            continue
        if server["type"] != transport:
            error(path, f"{name} の type は {transport} にします")
        if expected is not None and server["url"] != expected:
            error(path, f"{name} の url は {expected} にします（末尾スラッシュなし）")


repo_files = [
    p for p in sorted(ROOT.rglob("*")) if p.is_file() and ".git" not in p.relative_to(ROOT).parts
]

for p in repo_files:
    if p.suffix == ".json":
        load(p)

readme = (ROOT / "README.md").read_text(encoding="utf-8")

# Codex（portable）
codex_market_path = ROOT / ".agents/plugins/marketplace.json"
codex_market = load(codex_market_path)
if isinstance(codex_market, dict):
    market_name = codex_market.get("name")
    entries = codex_market.get("plugins")
    if not isinstance(market_name, str) or not market_name:
        error(codex_market_path, "name が要ります")
    if not isinstance(entries, list) or not entries:
        error(codex_market_path, "plugins が要ります")
        entries = []
    for i, entry in enumerate(entries):
        where = f"plugins[{i}]"
        source = entry.get("source") if isinstance(entry, dict) else None
        if not isinstance(source, dict) or source.get("source") != "local":
            error(codex_market_path, f"{where}.source.source は local にします")
            continue
        rel = source.get("path")
        if not isinstance(rel, str) or not rel.startswith("./"):
            error(codex_market_path, f"{where}.source.path は ./ で始めます（リポジトリの根から）")
            continue
        plugin_dir = (ROOT / rel).resolve()
        if ROOT not in plugin_dir.parents or not plugin_dir.is_dir():
            error(codex_market_path, f"{where}.source.path {rel} はリポジトリの中のディレクトリにします")
            continue
        policy = entry.get("policy") or {}
        if policy.get("installation") not in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}:
            error(codex_market_path, f"{where}.policy.installation が不正です")
        if policy.get("authentication") != "ON_INSTALL":
            error(codex_market_path, f"{where}.policy.authentication は ON_INSTALL にします（契約で固定）")
        manifest = validate(plugin_dir / "plugin.json", "plugin.schema.json")
        if isinstance(manifest, dict) and manifest.get("name") != entry.get("name"):
            error(plugin_dir / "plugin.json", f"name をマーケットプレイスの {entry.get('name')} と合わせます")
        mcp = validate(plugin_dir / "mcp.json", "mcp.schema.json")
        if isinstance(mcp, dict):
            check_servers(plugin_dir / "mcp.json", mcp.get("mcpServers"), entry.get("name"), "streamable-http")
        if not (plugin_dir / "skills").is_dir():
            error(plugin_dir, "skills/ を同梱します")
        command = f"codex plugin add {entry.get('name')}@{market_name}"
        if command not in readme:
            error(ROOT / "README.md", f"導入のコマンド `{command}` がありません")

# Claude
claude_market_path = ROOT / ".claude-plugin/marketplace.json"
claude_market = load(claude_market_path)
if isinstance(claude_market, dict):
    for entry in claude_market.get("plugins") or []:
        rel = entry.get("source") if isinstance(entry, dict) else None
        if not isinstance(rel, str):
            continue
        mcp_path = (ROOT / rel / ".mcp.json").resolve()
        mcp = load(mcp_path) if mcp_path.is_file() else None
        if isinstance(mcp, dict):
            check_servers(mcp_path, mcp.get("mcpServers"), entry.get("name"), "http")

# ChatGPT の案内：MCP の URL を末尾スラッシュなしでそのまま示す
chatgpt = (ROOT / "docs/chatgpt.md").read_text(encoding="utf-8")
for url in MCP_URLS.values():
    if url not in chatgpt:
        error(ROOT / "docs/chatgpt.md", f"{url} がありません")
for p in repo_files:
    text = p.read_text(encoding="utf-8", errors="replace")
    for url in MCP_URLS.values():
        if url + "/" in text:
            error(p, f"{url}/ と末尾スラッシュ付きで書かない")

# 秘密・個人の情報を置かない
SECRET_PATTERNS = {
    "秘密鍵": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "API キー・トークン": re.compile(
        r"\b(?:sk-[A-Za-z0-9_-]{20,}|sk_live_[A-Za-z0-9]+|gh[pousr]_[A-Za-z0-9]{20,}"
        r"|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[abprs]-[A-Za-z0-9-]+)"
    ),
    "メールアドレス": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
}
for p in repo_files:
    text = p.read_text(encoding="utf-8", errors="replace")
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            error(p, f"{label}らしい文字列があります")

# 社内の SSOT・spec への参照を公開リポジトリに持ち込まない。
# このスクリプト自身も検査対象にする。パターンの文字列を "docs/" + "ssot/" のように
# 分けて組み立てているのは、このファイルの source テキストに検査対象そのものの
# 連続した文字列を書かないため（分けて書けば self-match しない）。
SSOT_PATH = "docs/" + "ssot/"
# spec ディレクトリの ID は YYYY-MM-DD-<slug> の形。公式サイトの changelog 等、
# 日付付きの公開 URL のパスも同じ形になりうるので、その場合は除外する
# （マッチ位置の手前を空白・引用符まで遡り、その中に "://" があれば URL の一部と見なす）。
SPEC_ID_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}-[a-z][a-z0-9]*(?:-[a-z0-9]+)+\b")


def _is_inside_url(text, start):
    boundary = re.compile(r"[\s\"'<>()\[\]]")
    token_start = start
    while token_start > 0 and not boundary.match(text[token_start - 1]):
        token_start -= 1
    return "://" in text[token_start:start]


for p in repo_files:
    text = p.read_text(encoding="utf-8", errors="replace")
    if SSOT_PATH in text:
        error(p, "SSOT のパスらしい文字列があります（社内の SSOT・spec への参照は公開しない）")
    for m in SPEC_ID_PATTERN.finditer(text):
        if _is_inside_url(text, m.start()):
            continue
        error(p, "spec ディレクトリの ID らしい文字列があります（社内の SSOT・spec への参照は公開しない）")
        break

if errors:
    for message in dict.fromkeys(errors):
        print(f"::error::{message}")
    sys.exit(1)
print("プラグインの JSON と案内は検査を通りました")
