### import_all.py
---
## 初期状態のDBに、必要なデーターを一気に投入するスクリプトです。
---
実行時：
```
docker compose -f docker-compose.dev.yml exec api python scripts/import_all.py
```
### import_meals.py 
---
## mealsに初期データを流し込むだけの役割しか持ちません。
---
実行時：
```
docker compose -f docker-compose.dev.yml exec api python scripts/import_meals.py
```
---
### import_allergies.py 
---
## allergyに初期データを流し込むだけの役割しか持ちません。
---
実行時：
```
docker compose -f docker-compose.dev.yml exec api python scripts/import_allergies.py
```