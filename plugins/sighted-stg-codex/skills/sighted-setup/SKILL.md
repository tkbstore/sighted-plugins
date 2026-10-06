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

手で追加した MCP サーバーは、保存元によって片付け方が違う（codex-cli 0.159.2 で確認済み）。

| 保存元 | 見つかる場所 | `codex mcp list`／`get` に出るか | 同名のときの優先 | 外すコマンド |
| --- | --- | --- | --- | --- |
| グローバル（手で `codex mcp add` した分） | `$CODEX_HOME/config.toml`（既定 `~/.codex/config.toml`）の `[mcp_servers.<名前>]` | 出る | プラグインより優先 | `codex mcp remove "<名前>"` で外れる |
| プロジェクト（手で `.codex/config.toml` に書いた分） | そのプロジェクトの `.codex/config.toml` の `[mcp_servers.<名前>]` | **そのプロジェクトを Codex が trusted にしているときだけ**出る（untrusted だと無視される） | trusted なら**プラグインより優先**（グローバルと同格） | `codex mcp remove` では**外れない**（後述） |
| プラグイン（`codex plugin add` で入れた分） | `config.toml` の `[plugins."<plugin>@<marketplace>"]`（`mcp_servers` ではない） | 出る（グローバル・プロジェクトに同名が無いときだけ） | 最も低い | `codex plugin remove "<plugin>@<marketplace>"` |

1. Sighted の URL を指すサーバーの名前と URL を利用者に見せ、手で追加したほうを外すか聞く。`codex mcp list` の `Name`／`Url` で見つける。
2. **重なる場所によって見え方が違う**。
   - グローバルに手で追加した名前がプラグインのサーバーと同じだと、`codex mcp list` にはプラグインのほうが出ず、手で追加した URL だけが使われる（確認済み）。
   - そのプロジェクトを Codex が trusted にしているときは、プロジェクトの `.codex/config.toml` の同名 `[mcp_servers.<名前>]` も `codex mcp list`／`codex mcp get` に出て、プラグインの代わりに使われる（確認済み。untrusted なプロジェクトでは無視され、プラグインが使われる）。`codex mcp list` に出ているサーバーがプロジェクト起因かもしれないので、重複が疑わしいときは、そのプロジェクトのディレクトリで `cat .codex/config.toml` も直接見て確かめる。
3. 外してよいと言われたときだけ、保存元に応じて外す（勝手に消さない。関係ない設定は触らない）。
   - **グローバル**: `codex mcp remove "<名前>"` を実行する。「Removed global MCP server '<名前>'.」と出て外れる。
   - **プラグイン**: `codex mcp remove` ではなく `codex plugin remove "<名前>@<marketplace>"`（`codex plugin list` で `<marketplace>` を確かめる）。
   - **プロジェクト**: `codex mcp remove` を実行しても、グローバル設定にその名前が無ければ `No MCP server named '<名前>' found.`（終了コード 0）と出るだけで、プロジェクトの `.codex/config.toml` は**変わらない**（trusted でも同じ）。利用者に `.codex/config.toml` の中の名前を見せて同意を得てから、そのプロジェクトの `.codex/config.toml` を開き、重複している `[mcp_servers.<名前>]` の表だけを手で削除してもらう（他の設定は残す）。Codex からファイルを直接書き換えない。
   - Codex から実行できなければ、利用者に自分のターミナルで実行・編集してもらう。
4. 外した後の確認は保存元で分ける。グローバル・プラグインは `codex mcp list` に重複が無くなったことで確認できる。プロジェクトも trusted なら `codex mcp list` に出ているので同様に確認できるが、untrusted のときは `codex mcp list` に出ないため、そのプロジェクトの `.codex/config.toml` を再度見て、該当の表が無くなったことを確認する。
5. **設定を変えたら、Codex を起動し直して新しい会話を始める。** 「sighted-stg の sighted-setup に従って Sighted に接続して」と送るよう伝え、**ここで一旦止める**。この後の手順は、その新しい会話で続ける。

## 2. ログインと同意

ブラウザでのログインと提供の同意は利用者が行うが、そのきっかけとなる `codex mcp login` 自体は Codex が自分で実行する。

1. 実行する前に一言伝える：「ブラウザが開くので Sighted にログインし、同意画面で、接続先が `Codex（OpenAI）` であることとワークスペース・連携先を確かめて同意してください」（`<名前>` は 1 で確かめた名前を展開して示す）。
2. `codex mcp login "<名前>"` を実行する。コマンドは認可 URL を出力し、ブラウザでの認可が終わるまで待つ作りだが、**一括実行（ワンショットの exec）には既定で短い（10 秒程度の）タイムアウトがかかることがあり、ブラウザでの作業中に打ち切られる**。打ち切られずに待てる実行方法（セッションを保持する／タイムアウトを伸ばせる・無効化できる実行）があれば、それを使う。
   - 出力された認可 URL は、ブラウザが自動で開かないときの逃げ道として、完全な `https://` の URL をそのまま会話にも貼る。
   - アカウントが無ければ、そのログイン画面から登録できる。登録・メールアドレスの確認・ワークスペースの作成が終わると同意画面に戻る。戻れなかったときは、`codex mcp login "<名前>"` からやり直す（登録した内容は残っている）。
3. タイムアウトで打ち切られた（終了コード `124` 等）ときは、そのとき出た URL はもう使えない（待受が閉じている）。利用者にその URL を使わせず、`codex mcp login "<名前>"` をもう一度実行して新しい URL を発行し直す。
4. サンドボックス等の制約でコマンドがそもそも実行できない・ネットワークに届かないときは、昇格した権限（ネットワークを使える承認）で同じコマンドを実行する許可を利用者に求める。
   - それでも実行できない・待てる実行方法が無い・許可が得られないときは、利用者に自分のターミナルで `codex mcp login "<名前>"` を実行してもらう案内に切り替える。

ログインした後もこの会話で Sighted のツールが使えないときは、Codex を起動し直して新しい会話で続けてもらう。

## 3. 確かめる

`codex mcp login` がコマンドとして成功で終わったら（2 で利用者のターミナルに切り替えた場合は、利用者が「ログインした」「接続した」などと言ったら）`list_workspaces` を呼んで確かめる。取れたら、何ができるか（分析・計測の実行など）を一言で紹介する。計測はこの手順では実行しない。エラーになったら sighted-analysis の 7 章（足りないときの案内）の表に従う。`codex mcp list` の `Auth` は再接続時も `OAuth` のままで変わらないことがあるため、接続できたかの判断には使わない。

## 4. 接続し直すとき

sighted-analysis から接続し直しを案内するとき（`mcp_consent_scope_required`、使える WS が無い、WS・連携先を選び直したいなど）や、Sighted の画面に「接続元のアプリに戻って接続し直してください。」と出たときは、2 と同じく `codex mcp login "<名前>"` を実行し、同意画面で WS と連携先を選び直してもらう。前のログインを消してからやり直したいときは、先に `codex mcp logout "<名前>"` を実行する。

ツールの結果に `reauthorize_url` があれば、sighted-analysis の「画面の URL」の節の決まり（`https://` で入口と同じ origin のときだけ使う）を守って示す。
