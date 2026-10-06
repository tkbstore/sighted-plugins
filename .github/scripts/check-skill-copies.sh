#!/usr/bin/env bash
# skill の原稿（skills-src/）と、各プラグインに置いたコピーが一致するかを調べる。
# コピーを作る仕組みは持たない。直すときは原稿を直し、cp でコピーして一緒に commit する。
set -u
cd "$(dirname "$0")/../.." || exit 1

# 原稿 コピー（コピーごとに 1 行。コピーは原稿とだけ比べる）
pairs='
skills-src/sighted-analysis/SKILL.md plugins/sighted-stg/skills/sighted-analysis/SKILL.md
skills-src/sighted-analysis/SKILL.md plugins/sighted-stg-codex/skills/sighted-analysis/SKILL.md
skills-src/claude/sighted-setup/SKILL.md plugins/sighted-stg/skills/sighted-setup/SKILL.md
skills-src/codex/sighted-setup/SKILL.md plugins/sighted-stg-codex/skills/sighted-setup/SKILL.md
'

fail=0
error() {
  echo "::error file=$1::$2"
  fail=1
}

while read -r src dst; do
  [ -z "$src" ] && continue
  ok=1
  for f in "$src" "$dst"; do
    if [ -L "$f" ] || [ ! -f "$f" ]; then
      error "$f" "$f が無いか、通常のファイルではありません（symlink にしない）"
      ok=0
    fi
  done
  if [ "$ok" -eq 1 ] && ! cmp -s "$src" "$dst"; then
    error "$dst" "$dst が原稿 $src と違います。原稿を直して cp でコピーしてください"
    diff -u "$src" "$dst"
  fi
done <<EOF
$pairs
EOF

# プラグインの skill は上のコピーだけにする（原稿の無い skill を置かない）
expected=$(printf '%s\n' "$pairs" | awk 'NF == 2 { print $2 }' | sort)
actual=$(find plugins -path '*/skills/*' \( -type f -o -type l \) | sort)
if [ "$expected" != "$actual" ]; then
  error plugins "plugins/*/skills/ の中身が対応表と違います"
  diff <(printf '%s\n' "$expected") <(printf '%s\n' "$actual")
fi

# インストール先で外を指さないよう、symlink を使わない
links=$(find plugins skills-src -type l)
if [ -n "$links" ]; then
  error plugins "symlink を使わない: $links"
fi

if [ "$fail" -ne 0 ]; then
  echo "skill の原稿とコピーが一致しません"
  exit 1
fi
echo "skill の原稿とコピーは一致しています"
