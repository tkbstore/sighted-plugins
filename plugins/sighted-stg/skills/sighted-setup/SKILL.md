---
name: sighted-setup
description: Sighted を使えるようにする／接続する手順。「Sighted を使えるようにして」「接続」「セットアップ」「ログイン」「Sighted のツールが無い」「Needs authentication」で使う。Set up or connect Sighted, including when Sighted's MCP tools are missing or show "Needs authentication". Use before troubleshooting any Sighted connection issue.
---

# Sighted を使えるようにする

Sighted のプラグイン（MCP サーバーと skill）の接続手順。**利用者と同じ言語で答える**（日本語で話しかけられたら日本語）。

まず、どこで動いているか（Bash が使えるか）を見分ける。コマンドを実行できるなら Claude Code、できなければ claude.ai・デスクトップアプリ・Cowork として扱う。

## Claude Code

1. `claude mcp list` を見る。`plugin:sighted-stg:sighted-stg` と**別に**、同じ URL（`https://mcp.stg.sighted-aeo.com/mcp`）を指すサーバーがあれば、プラグインのサーバーが重複として使われない状態になっている。見つけたサーバー名を利用者に見せ、消してよいか同意をもらってから `claude mcp remove <名前>` で外す（勝手に消さない。スコープが違うときは `-s` を付ける）。
2. `plugin:sighted-stg:sighted-stg` が `Needs authentication` と出るのは正常。まだログインしていないだけ。
3. プラグインを入れた直後で、Sighted のツールやこの skill 自体が見当たらないときは、利用者に `/reload-plugins` を打ってもらう。
4. 利用者にやってもらうことを短く伝える。
   - Sighted のアカウントが無ければ、先に https://stg.sighted-aeo.com/signup で登録し、ワークスペースの作成まで済ませる。
   - `/mcp` を打って `plugin:sighted-stg:sighted-stg` を選び、開いたブラウザで Sighted にログインし、ワークスペースと連携先を選んで同意する。
   - **Claude は `claude mcp login` を自分で実行しない（できない）。** ブラウザでの OAuth は利用者が行う。
5. 利用者が「接続した」「ログインした」などと言ったら `list_workspaces` を呼んで確かめる。取れたら、何ができるか（分析・計測の実行など）を一言で紹介する。エラーになったら sighted-analysis の 7 章（足りないときの案内）の表に従う。

## claude.ai・デスクトップアプリ・Cowork

Claude はコマンドを実行できない。利用者に次を案内する。

1. プラグインを開き、**Connectors** タブから Sighted のコネクタを追加する。
2. 開いたブラウザで Sighted にログインし、ワークスペースと連携先を選んで同意する。
3. Sighted のアカウントが無ければ、先に https://stg.sighted-aeo.com/signup で登録し、ワークスペースの作成まで済ませてから 1 に戻る。

接続できたら `list_workspaces` で確かめ、何ができるかを一言で紹介する。エラーになったら sighted-analysis の 7 章に従う。

## どこで動いているか分からないとき

Bash やシェルのツールが使えるかで見分ける。使えれば Claude Code として上の節に従い、使えない（ツールが無い・実行できない）なら claude.ai・デスクトップアプリ・Cowork として案内する。判断できないときは両方の手順を短く示す。
