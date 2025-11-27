# MySQL 文字化け対策と my.cnf の設置方針

本プロジェクトでは、Docker 環境下の MySQL において、  
デフォルト設定が `latin1` であることに起因する文字化けが発生する。

これを回避するために MySQL に `my.cnf` を読み込ませる必要があるが、  
Windows / WSL のファイルシステム差により、以下の問題が発生した。

---

## ■ 発生した問題

### 1. MySQL はパーミッション 666 の設定ファイルを読まない
Docker 内部では、`my.cnf` が 644 でないと読み込まれない。

### 2. Windows ファイルシステムでは chmod が効かない
Windows 側に置いた `my.cnf` は、権限を変更できず、MySQL に拒否される。

### 3. WSL 側で作成した my.cnf は、Windows から見えない
WSL 側で作成すれば正しい権限になるが、  
Windows 管理下の VS Code や Git はそのファイルを参照できない。

---

## ■ 結論：my.cnf は環境依存とし、手動配置とする

以上の理由により、`my.cnf` をプロジェクトに同梱せず、  
**各環境で個別に作成する方針**とした。

また、Docker Compose の設定では `my.cnf` のパスを直書きせず、  
`.env` で外から指定する。

```
${MYSQL_CONF_PATH}:/etc/mysql/conf.d/my.cnf
```

---

## ■ 推奨配置場所
```
/home/<user_name>/ltm_mysql_conf/my.cnf
```

---

## ■ my.cnf（推奨内容）
```
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_general_ci

[client]
default-character-set = utf8mb4

[mysql]
default-character-set = utf8mb4
```

`.env` に以下を記述してパスを渡す：

```
MYSQL_CONF_PATH=/home/<user_name>/ltm_mysql_conf/my.cnf
```

---

## ■ 備考
この仕様は、Windows / WSL 混在環境で開発を行う際の  
“構造的制約”によって必然的に導かれたものである。  
移行や再構築の際には、本方針を参照すること。
