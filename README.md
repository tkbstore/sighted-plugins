# sighted-plugins

Sighted plugins for AI agents (Claude / Codex)

Sighted を AI エージェントから使うためのプラグインです。Claude 用と Codex 用のプラグインを置いています。ChatGPT はプラグインを使わず、[ChatGPT での追加手順](docs/chatgpt.md)で接続します。

| プラグイン | 使える場所 | 中身 |
| --- | --- | --- |
| [`sighted-stg`](plugins/sighted-stg/)（Sighted — Staging） | claude.ai・Cowork・Claude Code | Sighted ステージング環境（stg）の MCP サーバーへの接続と、分析・計測の手順（skill） |
| [`sighted-stg`](plugins/sighted-stg-codex/)（Codex 用） | Codex | 同じ MCP サーバーへの接続と、同じ分析・計測の手順。接続の手順（`sighted-setup`）だけ Codex 用 |

どちらも接続先は同じ MCP サーバー `https://mcp.stg.sighted-aeo.com/mcp` です。本番環境向けを出すときは、別のプラグインにします。`sighted-stg` の接続先を本番に切り替えることはしません。

## インストール

このリポジトリは Claude と Codex のプラグインのマーケットプレイス（どちらも名前は `sighted`）です。

### claude.ai・Claude デスクトップアプリ・Cowork

1. **Customize > Plugins** を開きます。
2. **Add > Add marketplace** で `tkbstore/sighted-plugins`（または `https://github.com/tkbstore/sighted-plugins`）を追加します。
3. 一覧に出る **Sighted — Staging** を選んで追加します。
4. プラグインを開き、**Connectors** タブで Sighted のコネクタを追加して接続します。ブラウザで Sighted にログインし、同意画面でワークスペースと連携先を選びます。client ID の入力は要りません。

- 追加したプラグインはアカウントに保存され、チャット・Cowork・同じアカウントでログインした Claude Code で使えます。
- プラグインを追加しただけでは接続されません。4 の接続が要ります。
- Team・Enterprise プランでは、組織の設定によって自分でマーケットプレイスやコネクタを追加できないことがあります。その場合は組織の Owner に追加を頼んでください。
- 画面の項目名は表示言語によって違うことがあります。

### Claude Code

Sighted のアカウントが無ければ、先に https://stg.sighted-aeo.com/signup で登録し、ワークスペースの作成まで済ませてください。登録済みなら次のプロンプトをそのまま貼ってください。

```text
Sighted を使えるようにして。次を実行してから、/reload-plugins → /sighted-stg:sighted-setup の順で打つよう伝えて（この会話でもう sighted-setup が使えるなら、それに従ってそのまま進めて）。
claude plugin marketplace add tkbstore/sighted-plugins
claude plugin install sighted-stg@sighted --scope user
```

- CLI でプラグインを入れた直後はそのセッションにまだ読み込まれていないため、`/reload-plugins` → `/sighted-stg:sighted-setup` の順に打つと `sighted-setup` skill の手順で接続まで案内されます。`/reload-plugins` が保留になったら `/reload-plugins --force` を打ってください。
- `/plugin install` で開く画面で、インストールの範囲を選ぶこともできます（上のコマンドは `user` スコープ）。
- `/mcp` で `plugin:sighted-stg:sighted-stg` を選び、ブラウザで Sighted にログインして同意します。
- 同じ URL（`https://mcp.stg.sighted-aeo.com/mcp`）の MCP サーバーを手で追加していると、Claude Code はそちらを使い、プラグインのサーバーは重複として使いません。プラグイン経由で使うときは、手で追加したほうを外してください。

### Codex

Sighted のアカウントが無ければ、先に https://stg.sighted-aeo.com/signup で登録し、ワークスペースの作成まで済ませてください。登録済みなら次のプロンプトを Codex にそのまま貼ってください。

```text
Sighted の stg を使えるようにして。次を順に実行して。
codex plugin marketplace add tkbstore/sighted-plugins
codex plugin add sighted-stg@sighted

追加できたら、新しい Codex の会話を開いて
「sighted-stg の sighted-setup に従って Sighted に接続して」
と送るよう案内して。この会話ですでにその skill と MCP が使える場合は、
その setup に従って続けて。
ブラウザでのログインと提供の同意は私が行う。接続後は WS 一覧で確かめて。
このセットアップだけで計測を実行しない。
```

- プラグインを入れた直後の会話には、プラグインの skill と MCP サーバーがまだ読み込まれていません。新しい会話で `sighted-setup` の手順に従うと、接続まで案内されます。
- ログインは自分のターミナルで `codex mcp login <サーバーの名前>` を実行し、ブラウザで Sighted にログインして同意します。サーバーの名前は `/mcp` か `codex mcp list` に出る名前で、`sighted-setup` が確かめて案内します。client ID の入力は要りません。
- 同じ URL（`https://mcp.stg.sighted-aeo.com/mcp`）の MCP サーバーを手で追加していると、プラグインのサーバーとは別の接続として並びます。名前が同じときは、手で追加したほうだけが使われます（codex-cli 0.159.2 で確認済み。保存元がグローバル（`~/.codex/config.toml`）でも、trusted なプロジェクトの `.codex/config.toml` でも同じ）。グローバルに追加したものは `codex mcp remove <名前>` で外せますが、**プロジェクトの `.codex/config.toml` に書いたものはこのコマンドでは外れません**（終了コードは 0 のまま何も変わりません）。その場合はプロジェクトの `.codex/config.toml` を開き、該当の `[mcp_servers.<名前>]` を手で削除してください。詳しくは `sighted-setup` の案内に従ってください。
- 計測の実行の前には、会話の中で見積もりを見せて確認を取ります。Codex が実行の許可を求める画面を出すかどうかは、Codex の承認の設定で決まります。プラグインはこの設定を変えません。設定例（`~/.codex/config.toml`。`approval_policy`・`approvals_reviewer` は codex-cli 0.159.2 で確認済みのキー）:

  ```toml
  approval_policy = "on-request"
  approvals_reviewer = "user"

  [plugins."sighted-stg@sighted".mcp_servers.sighted-stg.tools.run_query]
  approval_mode = "prompt"
  ```

  この設定でも、記憶された承認・`never`・組織やホスト側の上書きなどによって確認画面が出ないことがあります。**この設定だけで「必ず確認画面が出る」とは言えません。**

### ChatGPT

ChatGPT ではプラグインを使わず、Developer mode で MCP サーバーを app として追加します。手順は [docs/chatgpt.md](docs/chatgpt.md) にあります。

- MCP サーバーの URL は `https://mcp.stg.sighted-aeo.com/mcp` を**末尾スラッシュなし**で、そのまま貼ります。client ID・client secret は入力しません。
- ChatGPT Free では使えません。試す人は ChatGPT の設定でモデルの改善（Improve the model for everyone）をオフにしてください。
- ChatGPT には skill が付かず、分析・計測の手順は届きません。

### Sighted のアカウントが無いとき

接続のときのログイン画面から登録できます。登録・メールアドレスの確認・ワークスペースの作成が終わると、接続の同意画面に戻ります。途中で時間がかかって戻れなかったときは、使っている AI のアプリから接続し直してください。登録した内容は残っています。

## データの扱い

- プラグインに入っているのは、MCP サーバーの URL と、AI が従う手順（skill）だけです。秘密情報・client ID・利用者ごとの値は入っていません。
- 接続すると、AI は利用者が同意画面で選んだ範囲で Sighted のデータを読みます。渡る範囲と接続先は、接続のときの同意画面に表示されます。
- 計測の実行はクレジットを使います。クレジットはアカウントで 1 つで、どの AI から使っても同じ残高から減ります。skill は、実行の前に見積もりと残りを見せて確認を取るよう AI に指示しています（ChatGPT には skill が届きません）。サーバー側で金額の上限を強制する仕組みではありません。
- 接続は Sighted の設定の「AI 接続」からいつでも解除できます。

## 開発する人へ

- 構成:
  - `.claude-plugin/marketplace.json`（Claude のマーケットプレイス）と `plugins/sighted-stg/`（`.claude-plugin/plugin.json`・`.mcp.json`・`skills/`）。
  - `.agents/plugins/marketplace.json`（Codex のマーケットプレイス。`source.path` はリポジトリの根から）と `plugins/sighted-stg-codex/`（`plugin.json`・`mcp.json`・`skills/`）。
  - `skills-src/`: skill の原稿。`sighted-analysis` は両方に共通、`sighted-setup` は `claude/`・`codex/` で別。
  - `docs/chatgpt.md`: ChatGPT での追加手順。
- skill は `skills-src/` の原稿を直し、次のコマンドで各プラグインへコピーして一緒に commit します（プラグインの中のコピーを直接直さない）。CI（`.github/workflows/check.yml`）が原稿と各コピーの一致を検査します。

  ```sh
  cp skills-src/sighted-analysis/SKILL.md plugins/sighted-stg/skills/sighted-analysis/SKILL.md
  cp skills-src/sighted-analysis/SKILL.md plugins/sighted-stg-codex/skills/sighted-analysis/SKILL.md
  cp skills-src/claude/sighted-setup/SKILL.md plugins/sighted-stg/skills/sighted-setup/SKILL.md
  cp skills-src/codex/sighted-setup/SKILL.md plugins/sighted-stg-codex/skills/sighted-setup/SKILL.md
  ```

- 手元での検査: `bash .github/scripts/check-skill-copies.sh`、`uv run --no-project --with 'jsonschema==4.25.1' python .github/scripts/check-manifests.py`、`claude plugin validate --strict .`、`claude plugin validate --strict ./plugins/sighted-stg`。
- Codex 用の `plugin.json`・`mcp.json` は Agent Plugins 1.0.0 の形式です。CI は `.github/schemas/` に置いた schema の写し（https://agent-plugins.org/schemas/1.0.0/）で検査します。
- 中身を変えたら、そのプラグインの `version` を上げます（Claude 用は `.claude-plugin/plugin.json`、Codex 用は `plugin.json`）。上げないと、入れた人に更新が届きません（Codex も入れたプラグインを版ごとに保存します）。
- skill は外部から手順を取りに行かない作りにします。手順はファイルに書いたことだけです。
