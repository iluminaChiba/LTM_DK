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