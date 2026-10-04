# Sighted — Staging（`sighted-stg`）

Sighted のステージング環境（stg）のデータを Claude との会話で分析し、計測クエリを実行するためのプラグインです。
claude.ai（Web・デスクトップ・モバイル）、Cowork、Claude Code で使えます。インストールの手順は[リポジトリの README](../../README.md) にあります。

## 中身

| ファイル | 役割 |
| --- | --- |
| `.mcp.json` | Sighted の MCP サーバー `https://mcp.stg.sighted-aeo.com/mcp` への接続。ログインは OAuth で、client ID の入力は要りません |
| `skills/sighted-setup/SKILL.md` | Claude が従う手順。接続・ログインの案内、重複する MCP サーバーの整理、`Needs authentication` の扱い |
| `skills/sighted-analysis/SKILL.md` | Claude が従う手順。ワークスペースの選び方、データの取り方と数字の読み方、計測の実行前の確認、足りないときの案内、Meta 広告データの利用制限 |

## 使い方

Claude Code では、次のプロンプトを貼るだけでインストールから接続の案内までを Claude が進めます。

```text
Sighted を使えるようにして。次を実行してから、Sighted プラグインの接続の手順に従って最後まで案内して。
claude plugin marketplace add tkbstore/sighted-plugins
claude plugin install sighted-stg@sighted --scope user
```

接続したあと、たとえば次のように頼みます。

- 「先週の AI の回答での露出と、Search Console の検索流入を比べて」
- 「GA4 のセッション数を先月と比べて」
- 「このクエリの計測を回して」

## 計測の実行前の確認

計測の実行（`run_query`）はクレジットを使います。skill は Claude に次の順を守らせます。

1. 見積もり（`estimate_query`）で、使うクレジットと残りを見せる。残りはアカウント全体で共有です
2. 利用者がその会話ではっきり OK するまで実行しない
3. 実行の直前に見積もりを取り直し、変わっていたら聞き直す
4. 残りが足りなければ実行せず、足りない量と購入の方法を伝える

これは Claude への手順で、サーバー側で金額の上限を強制する仕組みではありません。実際の額は実行のときに Sighted が計算します。

## できないこと

- ワークスペース・クエリの作成、連携（Google Search Console・Google Analytics 4・Meta）の追加、クレジットの購入。これらは Sighted の画面で行います
- YouTube のデータの取得（MCP では提供していません）
- 接続のときの同意画面で選んでいないワークスペース・連携先のデータの取得
