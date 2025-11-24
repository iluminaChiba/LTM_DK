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
## mysqlの文字コード一覧
SHOW VARIABLES LIKE 'character_set%';

Docker内のmysqlのクライアント文字コードの変更は、my.cnfファイルを置くしか方法がない。
で、そのmy.cnfファイルは、Windows側で設置すると、chmod644が効かないので、666のままになり、
Dockerのセキュリティが働いて、読み込まない。だから、WSL側でフォルダを作り、そのフォルダに
my.cnfをcpして、linux管理にしてから、chmod 6444しないといけない。
この方法論に辿り着くまで、マジで大変だった。