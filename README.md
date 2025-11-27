# LTM_DK

FastAPI / MySQL / Docker Compose を基盤とした、昼食管理システムです。  
現場運用に必要な機能を、最小構成で安定的に提供することを目的としています。

---

## ■ 技術スタック
- Python 3.11
- FastAPI
- SQLAlchemy
- MySQL 8
- Docker Compose

---

## ■ ディレクトリ構成（暫定）
```
LTM_DK/
├─ app/
│ ├─ api/
│ ├─ crud/
│ ├─ models/
│ ├─ schemas/
│ ├─ template_manager/
│ ├─ templates/
│ ├─ database.py
│ └─ main.py
├─ infra/
│ ├─ db/
│ ├─ Dockerfile.dev
│ ├─ Dockerfile.prod
│ ├─ requirements.dev
│ └─ requirements.prod
├─ scripts/
├─ docs/（後述）
├─ docker-compose.dev.yml
├─ docker-compose.prod.yml
└─ README.md

※ .dev(開発用)  .prod(本番用)
```


---

## ■ 現在の状態
第二期構造移行中のため、コードベース全体を再構成しています。  
今後、順次ドキュメントを追加し、整備を進めていきます。

---

## ■ docs/
詳細な環境構築手順や設計方針については docs/ を参照してください。
プロジェクト仕様、環境構築、運用フローなどの資料をここにまとめていきます。
