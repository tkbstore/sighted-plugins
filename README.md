# sighted-plugins

Sighted plugins for AI agents (Claude / Codex)

Sighted を AI エージェントから使うためのプラグインです。いまは Claude 向けのプラグインを 1 つ置いています。

| プラグイン | 使える場所 | 中身 |
| --- | --- | --- |
| [`sighted-stg`](plugins/sighted-stg/)（Sighted — Staging） | claude.ai・Cowork・Claude Code | Sighted ステージング環境（stg）の MCP サーバーへの接続と、分析・計測の手順（skill） |

本番環境向けを出すときは、別のプラグインにします。`sighted-stg` の接続先を本番に切り替えることはしません。

## インストール

このリポジトリは Claude のプラグインのマーケットプレイス（名前は `sighted`）です。

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

```text
/plugin marketplace add tkbstore/sighted-plugins
/plugin install sighted-stg@sighted
/mcp
```

- `/plugin install` で開く画面で、インストールの範囲を選びます。
- `/mcp` で `plugin:sighted-stg:sighted-stg` を選び、ブラウザで Sighted にログインして同意します。
- シェルからは `claude plugin marketplace add tkbstore/sighted-plugins` と `claude plugin install sighted-stg@sighted` でも入れられます。
- 同じ URL（`https://mcp.stg.sighted-aeo.com/mcp`）の MCP サーバーを手で追加していると、Claude Code はそちらを使い、プラグインのサーバーは重複として使いません。プラグイン経由で使うときは、手で追加したほうを外してください。

### Sighted のアカウントが無いとき

接続のときのログイン画面から登録できます。登録・メールアドレスの確認・ワークスペースの作成が終わると、接続の同意画面に戻ります。途中で時間がかかって戻れなかったときは、Claude から接続し直してください。登録した内容は残っています。

## データの扱い

- プラグインに入っているのは、MCP サーバーの URL と、Claude が従う手順（skill）だけです。秘密情報・client ID・利用者ごとの値は入っていません。
- 接続すると、Claude は利用者が同意画面で選んだ範囲で Sighted のデータを読みます。渡る範囲は接続のときの同意画面に表示されます。
- 計測の実行はクレジットを使います。skill は、実行の前に見積もりと残りを見せて確認を取るよう Claude に指示しています。サーバー側で金額の上限を強制する仕組みではありません。
- 接続は Sighted の設定の「AI 接続」からいつでも解除できます。

## 開発する人へ

- 構成: `.claude-plugin/marketplace.json`（マーケットプレイス）と `plugins/sighted-stg/`（`.claude-plugin/plugin.json`・`.mcp.json`・`skills/sighted-analysis/SKILL.md`）。
- 変更したら `claude plugin validate --strict .` と `claude plugin validate --strict ./plugins/sighted-stg` を通します。
- `plugin.json` の `version` を上げないと、Claude Code に入れた人には更新が届きません。変更を出すたびに上げます。
- skill は外部から手順を取りに行かない作りにします。手順はファイルに書いたことだけです。
