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


wsl内のipを、windowsから参照可能にするコマンド
wsl内で ip addr
ずらずら表示されるので、eth0 の inet を探す


netsh interface portproxy add v4tov4 `
  listenport=8000 listenaddress=0.0.0.0 `
  connectport=8000 connectaddress=172.28.7.75

cmd で以下のコマンドで確認
netstat -ano | findstr :8000



  {
    "meal_id": 26,
    "meal_name": "",
    "furigana": "",
    "side1": "",
    "side2": "",
    "side3": "",
    "kcal": ,
    "protein": ,
    "fat": ,
    "carb": ,
    "salt": 
  },