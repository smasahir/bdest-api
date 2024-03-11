# bdest-api
- C, H, N, Oで構成される分子の結合解離エネルギー（BDE）を予測するAPI
- [smasahir/bde-ml](https://github.com/smasahir/bde-ml)で作成した予測モデルをAPIで利用できるようにした。
- [SMILES](https://ja.wikipedia.org/wiki/SMILES%E8%A8%98%E6%B3%95)で分子を指定してリクエストすると、"単結合"かつ"環状構造に含まれない結合"のBDEのみ予測し、結果をデータベースに登録する。
- API利用方法はSwagger UI`http://{hostname}/docs`を参照。

## 前提条件
- dockerが利用可能であること

## 起動手順
1. docker composeをビルドする。
   ```bash
   docker compose build --no-cache
   ```

2. docker composeを起動する。
   ```bash
   docker compose up
   ```

3. Swagger UI`http://localhost:8000/docs`にブラウザでアクセスする。

4. Swagger UIから各種APIを実行
   - `POST /molecules`にて、Request bodyを下記のように指定して発行すると、構造情報と予測結果がデータベースに登録される。レスポンスとしてその構造のBDEの予測結果が返却される。
     ```json
     {
      "smiles": "CN1CCC[C@H]1c2cccnc2"
     }
     ```
   - SMILESとして無効な文字列や、C, N, H, O以外の元素を含めてPOSTリクエストすると、`400 Bad Request`となる。
   - `GET /molecules`にて、データベースに登録済みのすべての構造情報（BDEを含む）が返却される。
   - `DELETE /molecules/{molecule_id}`にて、指定したIDの分子とその構造情報（BDEを含む）がデータベースから削除される。

## 開発環境
- 本リポジトリをvscodeの「Reopen in container」にて起動すると、開発環境が起動する（[.devcontainer/devcontainer.json](.devcontainer/devcontainer.json)で設定）。
- デバッグ実行時は`8001`でAPIが公開される（[.vscode/launch.json](.vscode/launch.json)で設定）。
