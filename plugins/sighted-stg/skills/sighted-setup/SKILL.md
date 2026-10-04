---
name: sighted-setup
description: Sighted を使えるようにする／接続する手順。「Sighted を使えるようにして」「接続」「セットアップ」「ログイン」「Sighted のツールが無い」「Needs authentication」で使う。Set up or connect Sighted, including when Sighted's MCP tools are missing or show "Needs authentication". Use before troubleshooting any Sighted connection issue.
---

# Sighted を使えるようにする

Sighted のプラグイン（MCP サーバーと skill）の接続手順。**利用者と同じ言語で答える**（日本語で話しかけられたら日本語）。

入口: `https://stg.sighted-aeo.com`。この skill の中では以降「入口」と書き、`<入口>` で参照する（本番ではここだけ差し替える。`sighted-analysis` にも同じ値を同じ形で定義している）。**利用者への答えでは必ず入口を展開した完全な `https://` の URL を出す**。

まず、このセッションがどの製品で動いているかを見る（セッション自身の情報や、利用者がどう頼んできたかで判断する）。**Bash・シェルが使えるかどうかでは判断しない**（Cowork もシェルを実行できるが、Sighted への接続は Connectors タブで行う製品なので、シェルの有無は判断材料にならない）。判断できないときは、下の両方の案内を短く示す。

## 利用者がまずやること（アカウントが無いとき）

Sighted のアカウントが無ければ、先に `<入口>/signup` で登録し、ワークスペースの作成まで済ませてもらう。登録済みならこの節は不要。

## Claude Code

1. `claude mcp list` を見る。`plugin:sighted-stg:sighted-stg` と**別に**、同じ URL（`https://mcp.stg.sighted-aeo.com/mcp`）を指すサーバーがないか確かめる。`claude mcp list` はスコープを出さないので、候補が見つかったら `claude mcp get "<名前>"` で URL とスコープを確かめる。URL は、ホストの大文字・小文字・既定ポート・末尾スラッシュの違いだけを同一視した**完全一致**で比べる（ホスト名だけの一致・部分一致では候補にしない）。一致したら、その名前とスコープを利用者に見せて消してよいか同意をもらい、OK が出たら確かめたスコープを付けて `claude mcp remove -s <スコープ> "<名前>"` で外す（勝手に消さない）。
   - **外したら、設定が変わっている。** `/reload-plugins`（保留になったら `/reload-plugins --force`）→ `/sighted-stg:sighted-setup` の順で打つよう伝え、**ここで一旦止める**。この後の手順（2 以降）は、その再読み込み後の会話で続ける。手で入れたサーバーが重なっていても、今の会話には skill 自体は読まれているが、外した直後はプラグインの MCP サーバーがまだ今の会話に自動では加わらないため、再読み込みを省くと次の `/mcp` にサーバーが見当たらず案内が途切れる。
   - 省けるのは、**設定の変更が無く**、かつ `plugin:sighted-stg:sighted-stg` が**今の会話でもう見えている**ときだけ。
2. `plugin:sighted-stg:sighted-stg` が `Needs authentication` と出るのは正常。まだログインしていないだけ。
3. CLI（`claude plugin install` など）でプラグインを入れた直後は、そのセッションにまだ読み込まれていない（次回起動か `/reload-plugins` で読まれる）。利用者に `/reload-plugins`（保留になったら `/reload-plugins --force`）を打ってもらい、続けて `/sighted-stg:sighted-setup` を打ってもらう。**この会話の中でこの skill がもう動いているなら**、それ自体が読み込み済みという証拠なので、そのまま次に進む。
4. 利用者に次を伝える。
   - `/mcp` を打って `plugin:sighted-stg:sighted-stg` を選び、開いたブラウザで Sighted にログインし、ワークスペースと連携先を選んで同意する。
   - **Claude は `claude mcp login` を自分で実行しない（できない）。** ブラウザでの OAuth は利用者が行う。
5. 利用者が「接続した」「ログインした」などと言ったら `list_workspaces` を呼んで確かめる。取れたら、何ができるか（分析・計測の実行など）を一言で紹介する。エラーになったら sighted-analysis の 7 章（足りないときの案内）の表に従う。

## claude.ai・デスクトップアプリ・Cowork

これらの製品での Sighted への接続は、**プラグインの Connectors タブ**から行う（Cowork もシェルを実行できるが、MCP の接続は `claude mcp`・`/mcp` ではなく Connectors タブが正しい導線）。Claude はこの接続作業を代行できない。利用者に次を案内する。

1. プラグインを開き、**Connectors** タブから Sighted のコネクタを追加する。
2. 開いたブラウザで Sighted にログインし、ワークスペースと連携先を選んで同意する。

接続できたら `list_workspaces` で確かめ、何ができるかを一言で紹介する。エラーになったら sighted-analysis の 7 章に従う。
