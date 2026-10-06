# ChatGPT で Sighted を使う（stg）

ChatGPT の Developer mode で、Sighted のステージング環境（stg）の MCP サーバーを app として追加する手順です。ChatGPT はプラグインを使わず、MCP サーバーの URL を直接登録します。

画面の項目名は表示言語や ChatGPT の版によって違うことがあります。

## 先に知っておくこと

- **ChatGPT Free では使えません。** Developer mode は Plus・Pro などの有料プランの Web 版で使えます。Business・Enterprise・Edu では、組織の管理者の設定によって使えないことがあります。
- 計測の実行（書き込み）を使えるかは、プランによって違うことがあります。Plus・Pro での結果は確かめているところです。
- **skill は付きません。** このリポジトリの skill（分析の手順・接続の手順）は ChatGPT には届かず、Codex・Claude 向けの分析の手順は ChatGPT では使われません。計測を実行する前は、使うクレジットと残りを `estimate_query` の結果で自分で確かめてください。
- 試す人は、ChatGPT の **Settings → Data controls → Improve the model for everyone** をオフにしてください。

## 1. Developer mode を有効にする

ChatGPT の **Settings → Security and login → Developer mode** をオンにします。

## 2. app を追加する

1. [ChatGPT の Plugins](https://chatgpt.com/plugins) を開き、**＋** から **Create custom MCP server** を選びます。
2. 名前（例: `Sighted stg`）と説明を入れます。
3. MCP サーバーの URL に、次をそのまま貼ります。

   ```text
   https://mcp.stg.sighted-aeo.com/mcp
   ```

   **末尾にスラッシュを付けません**（`/mcp/` にしない）。`https://` から `/mcp` まで一字も変えずに貼ってください。違う URL だと接続できません。
4. 認証は **OAuth** を選びます（`No authentication` ではありません）。client ID・client secret は入力しません（欄があっても空のまま）。[OpenAI の custom MCP server の手順](https://developers.openai.com/api/docs/guides/custom-mcp-server)（2026-10-06 時点）は、client ID・secret を自分で入れない場合に ChatGPT が CIMD（Client ID Metadata Document）を使えると説明していますが、これは**自動ではなく**、「認可サーバーが対応を広告していて、かつ作成者が CIMD を選んだとき」が条件です（原文: "ChatGPT can use Client ID Metadata Documents when the authorization server advertises support **and the app creator chooses CIMD**"）。つまり、client ID・secret を空のままにするだけでなく、**CIMD を選ぶ操作が別途必要**です。この画面でその選択がどの項目名（ボタン・ドロップダウンなど）で出るかは、公式手順には書かれておらず確かめられていません。選択肢が見えたら「CIMD」を選び、見当たらない場合は画面の指示に従ってください。画面の表記は変わることがあります。
5. 注意の表示を読み、**I understand and want to continue** → **Create as a plugin** を選びます。

## 3. ログインと同意

開いたブラウザで Sighted にログインし、Sighted の同意画面で、接続先が `ChatGPT（OpenAI）` であることと、ワークスペース・連携先・渡る範囲を確かめて同意します。

- Sighted のアカウントが無ければ、そのログイン画面から登録できます。登録・メールアドレスの確認・ワークスペースの作成が終わると同意画面に戻ります。戻れなかったときは、ChatGPT から接続し直してください。

## 4. 使う

新しい会話を開き、入力欄で `@` を打って追加した app を選びます。たとえば次のように頼みます。

- 「Sighted のワークスペースの一覧を見せて」
- 「このクエリの AEO の計測結果と推移を見せて」
- 「このクエリを計測するときのクレジットを見積もって」

計測の実行（`run_query`）はクレジットを使います。ChatGPT が実行の確認を求めたら、見積もりで使うクレジットと残りを確かめてから許可してください。ChatGPT の確認画面にはクレジットの額は出ません。確認を記憶させる（以後聞かない）選択はしないでください。

## 5. 更新・接続し直し・解除

- Sighted のツールが変わったときは、ChatGPT の Plugins で app を開いて **Refresh** を選び、新しい会話で使います。
- 同意の範囲を変えたいとき、ログインが切れたときは、ChatGPT の Plugins で app を開いて接続し直し、Sighted の同意画面で選び直します。
- 解除するときは、ChatGPT の Plugins で app を外し、Sighted の設定の「AI 接続」からも解除します。解除しても、すでに ChatGPT に渡った内容は Sighted からは消せません。

## できないこと

- ワークスペース・クエリの作成、連携（Google Search Console・Google Analytics 4・Meta）の追加、クレジットの購入。これらは Sighted の画面（https://stg.sighted-aeo.com）で行います
- YouTube のデータの取得（MCP では提供していません）
- 同意画面で選んでいないワークスペース・連携先のデータの取得
