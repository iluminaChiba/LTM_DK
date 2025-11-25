# FastAPI-Docker「安全起動フロー」備忘録

## ① コンテナの状態確認（最初の1手）
```
docker compose -f docker-compose.dev.yml ps
```

## ② 安全な停止
```
docker compose -f docker-compose.dev.yml down
```

## ③ 通常起動
```
docker compose -f docker-compose.dev.yml up -d
```

## ④ 通常ビルド → 起動
```
docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.dev.yml up -d
```

## ⑤ キャッシュ破棄ビルド
```
docker compose -f docker-compose.dev.yml build --no-cache
docker compose -f docker-compose.dev.yml up -d
```

## ⑥ ログ確認
```
docker compose -f docker-compose.dev.yml logs -f api
docker compose -f docker-compose.dev.yml logs -f db
```

## ⑦ orphan コンテナ掃除
```
docker compose -f docker-compose.dev.yml down --remove-orphans
```

## ⑧ 全コンテナの生存確認
```
docker ps
```

## Docker内のMySQLを操作する方法
docker compose -f docker-compose.dev.yml exec db bash

sudo docker exec -it ltm_dk-db-1 bash

## mysqlの文字コード一覧
SHOW VARIABLES LIKE 'character_set%';

Docker内のmysqlのクライアント文字コードの変更は、my.cnfファイルを置くしか方法がない。
で、そのmy.cnfファイルは、Windows側で設置すると、chmod644が効かないので、666のままになり、
Dockerのセキュリティが働いて、読み込まない。だから、WSL側でフォルダを作り、そのフォルダに
my.cnfをcpして、linux管理にしてから、chmod 6444しないといけない。
この方法論に辿り着くまで、マジで大変だった。

以上の方法論だと、今度はamazon linuxで動かない。っていうか、wslのファイルシステム上にある
ファイルは、windowsからは見えないので、git管理できない。だから、当然、リポジトリをクローン
しても、ついてこない。つまり、my.cnfは、都度、環境ごとに手動配置するしかない。

本プロジェクトでは、以下を定位置にする。

 home/<user_name>/ltm_mysql_conf/my.cnf  

各端末で、この場所にmy.cnfを設置する。
以下はmy.cnfの内容 nanoで書くしかないね・・・・
--------------------------------------------------
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_general_ci

[client]
default-character-set = utf8mb4

[mysql]
default-character-set = utf8mb4
--------------------------------------------------

## 迷子になった時、ディレクトリを探すコマンド
$ find / -name "LTM_DK" -type d

## wsl側から見たデスクトップの場所
/mnt/c/Users/canar/Desktop/LTM_DK$


■ セクションA：Webアプリの基本構造

（抽象理解を測る）

1.

Webアプリには「フロント」と「バックエンド」があります。
それぞれ何を担当しているものだと考えていますか？

→ 抽象的な理解レベルを計測。

2.

1つの画面（例：一覧ページ）を作る時、
裏側では何種類くらいの処理が動くと思いますか？

→ 「1画面＝1ファイル」思考かどうかがわかる。

■ セクションB：API と DB の関係

（データの流れの把握を測る）

3.

Python から MySQL にデータを送ったり取ったりするには、
何か“仲介役”が必要だと思いますか？
その仲介はどのような役目をしていると思いますか？

→ ORM / ドライバ / 接続といった概念の想像力を見る。

4.

API が 1 つ増えるとしたら、
新しくどんな処理を追加する必要があると思いますか？
思いつくだけで構いません。

→ CRUD の理解段階が測れる。

■ セクションC：Docker・環境周り

（実行環境のイメージを測る）

5.

「自分のPCで実行するPython」と「Dockerの中で動くPython」は、
同じだと思いますか？違うと思いますか？
理由もあれば教えて下さい。

→ コンテナの概念の有無がわかる。

6.

Docker でアプリを動かすとき、.env の役割は何だと考えていますか？

→ 設定／環境差異の概念があるかどうか。

■ セクションD：コード構造・責務

（タスクを渡せるかどうかの判断材料）

7.

1つのPythonファイルの中に、
DBアクセス・データ加工・APIレスポンス生成を全部書く場合と、
処理ごとにファイルを分ける場合では、
どんな違いが生まれると思いますか？

→ 分割思想を理解しているか確認。

8.

「エラー処理」はどこで行うのが正しいと思いますか？
複数あれば複数で構いません。

→ 責務分離のセンスの有無を見抜ける。

■ セクションE：自己評価

（本人の認知スタイルを知るための質問）

9.

自分は “コードを書いて動かしながら覚えるタイプ” と
“まず全体像を聞いてから理解するタイプ” のどちらに近いですか？

→ 教え方を調整するための情報。

10.

このプロジェクトで、
自分が一番好き（または得意）な部分はどこですか？
逆に苦手だと感じる部分はどこですか？

→ タスク分配の最適化に使う。