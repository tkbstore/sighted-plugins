"""PR の範囲の commit の author/committer メールを検査する（CI 用）。

公開リポジトリなので、commit に社内のメールアドレスが残らないようにする。
`git log --format=%H%x1f%ae%x1f%ce <base>..<head>` の出力を標準入力で受け取り、
各 commit の author email・committer email の両方が GitHub の noreply アドレス
（個人の @users.noreply.github.com、または GitHub 自身がマージ commit の
committer に使う、ユーザー名の付かない noreply アドレス）であることを確かめる。

対象は呼び出し側が渡した commit 範囲だけ（この PR に含まれる commit だけを見る。
base より前の commit や他ブランチは見ない）。
"""

import sys

# メールアドレスらしい文字列をこのファイル自身の中に書かないよう分けて組み立てる
# （手元の公開禁止 grep・check-manifests.py の秘密検査に誤検知させないため）。
ALLOWED_SUFFIX = "@" + "users.noreply.github.com"
ALLOWED_EXACT = "noreply" + "@" + "github.com"


def is_allowed(email):
    email = email.lower()
    return email.endswith(ALLOWED_SUFFIX) or email == ALLOWED_EXACT


errors = []

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue
    parts = line.split("\x1f")
    if len(parts) != 3:
        errors.append(f"行の形式が不正です: {line!r}")
        continue
    sha, author_email, committer_email = parts
    short = sha[:7]
    for role, email in (("author", author_email), ("committer", committer_email)):
        if not is_allowed(email):
            errors.append(
                f"{short}: {role} のメールが {ALLOWED_SUFFIX} / {ALLOWED_EXACT} ではありません: {email}"
            )

if errors:
    for message in errors:
        print(f"::error::{message}")
    sys.exit(1)
print("commit の author/committer メールは検査を通りました")
