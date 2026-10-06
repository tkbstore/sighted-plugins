---
name: sighted-setup
description: Codex で Sighted を使えるようにする／接続する手順。「Sighted を使えるようにして」「接続」「セットアップ」「ログイン」「Sighted のツールが無い」「Not logged in」で使う。Set up or connect Sighted in Codex, including when Sighted's MCP tools are missing or show "Not logged in". Use before troubleshooting any Sighted connection issue.
---

# Sighted を使えるようにする（Codex）

Codex で Sighted のプラグイン（MCP サーバーと skill）を使うための接続手順。**利用者と同じ言語で答える**（日本語で話しかけられたら日本語）。

入口: `https://stg.sighted-aeo.com`。この skill の中では以降「入口」と書き、`<入口>` で参照する（本番ではここだけ差し替える。`sighted-analysis` にも同じ値を同じ形で定義している）。**利用者への答えでは必ず入口を展開した完全な `https://` の URL を出す**。

Sighted の MCP サーバーの URL は `https://mcp.stg.sighted-aeo.com/mcp`（以下「Sighted の URL」）。

- この手順の中では計測（`run_query`）を実行しない。
- Codex の設定（`config.toml`・承認の設定）を、利用者の OK なしに書き換えない。

## 利用者がまずやること（アカウントが無いとき）

Sighted のアカウントが無ければ、先に `<入口>/signup` で登録し、ワークスペースの作成まで済ませてもらう。登録済みならこの節は不要。

## 1. Sighted の MCP サーバーを確かめる

この skill がこの会話で読めているなら、プラグインは読み込まれている。利用者に `/mcp` を打ってもらうか（詳しくは `/mcp verbose`）、`codex mcp list` を実行して、URL が Sighted の URL のサーバーを探す。`/plugins` でプラグイン `sighted-stg` を開いても、含まれる MCP サーバーを見られる。

- プラグインの中でのサーバーの名前は `sighted-stg` だが、Codex での表示名は版などで変わりうる。名前は推測せず、表示された名前（`codex mcp list` の `Name`）をそのまま使う。以下 `<名前>` と書く。
- URL は、ホストの大文字・小文字・既定ポート・末尾スラッシュの違いだけを同一視した**完全一致**で比べる。ホスト名だけの一致・部分一致では候補にしない。
- `Auth` が `Not logged in` なのは正常。まだログインしていないだけ。2 に進む（同じ URL のサーバーが二つ以上あれば、先に下の「重なっているとき」）。
- 見つからないときは、`/plugins` で `sighted-stg` が入っていて有効か見てもらう。

### 同じ URL のサーバーが重なっているとき

手で追加した MCP サーバー（`codex mcp add` や `config.toml` の `[mcp_servers.<名前>]`）は、プラグインのサーバーとは別に並ぶ。Sighted の URL を指すサーバーが二つ以上あると、それぞれが別の接続になり、ログインと同意も別々になる。

1. Sighted の URL を指すサーバーの名前と URL を利用者に見せ、手で追加したほうを外すか聞く。手で追加したものは `~/.codex/config.toml`（またはプロジェクトの `.codex/config.toml`）の `[mcp_servers.<名前>]` にある。プラグインのサーバーはそこには書かれていない。
2. 手で追加したサーバーの名前がプラグインのサーバーと同じだと、プラグインのサーバーは一覧に出ず、手で追加したほうだけが使われる。この場合も 1 と同じく利用者に見せて聞く。
3. 外してよいと言われたときだけ、`codex mcp remove "<名前>"` で外す（勝手に消さない）。Codex から実行できなければ、利用者に自分のターミナルで実行してもらう。このコマンドで外れるのは手で追加したものだけで、プラグインのサーバーは外れない。
4. **外したら、設定が変わっている。** Codex を起動し直して新しい会話を始め、「sighted-stg の sighted-setup に従って Sighted に接続して」と送るよう伝え、**ここで一旦止める**。この後の手順は、その新しい会話で続ける。

## 2. ログインと同意

ブラウザでのログインと提供の同意は利用者が行う。**Codex は `codex mcp login` を自分で実行しない。** 利用者に次を伝える。

1. 自分のターミナルで `codex mcp login "<名前>"` を実行する（`<名前>` は 1 で確かめた名前を展開して示す）。
2. 開いたブラウザで Sighted にログインし、Sighted の同意画面で、接続先が `Codex（OpenAI）` であることと、ワークスペース・連携先を確かめて同意する。client ID などの入力は要らない。
   - アカウントが無ければ、そのログイン画面から登録できる。登録・メールアドレスの確認・ワークスペースの作成が終わると同意画面に戻る。戻れなかったときは、`codex mcp login "<名前>"` からやり直す（登録した内容は残っている）。
3. ブラウザで終わったら Codex に戻る。

ログインした後もこの会話で Sighted のツールが使えないときは、Codex を起動し直して新しい会話で続けてもらう。

## 3. 確かめる

利用者が「ログインした」「接続した」などと言ったら `list_workspaces` を呼んで確かめる。取れたら、何ができるか（分析・計測の実行など）を一言で紹介する。計測はこの手順では実行しない。エラーになったら sighted-analysis の 7 章（足りないときの案内）の表に従う。

## 4. 接続し直すとき

sighted-analysis から接続し直しを案内するとき（`mcp_consent_scope_required`、使える WS が無い、WS・連携先を選び直したいなど）や、Sighted の画面に「接続元のアプリに戻って接続し直してください。」と出たときは、2 と同じく利用者に `codex mcp login "<名前>"` を実行してもらい、同意画面で WS と連携先を選び直してもらう。前のログインを消してからやり直したいときは、先に `codex mcp logout "<名前>"` を実行してもらう。

ツールの結果に `reauthorize_url` があれば、sighted-analysis の「画面の URL」の節の決まり（`https://` で入口と同じ origin のときだけ使う）を守って示す。
