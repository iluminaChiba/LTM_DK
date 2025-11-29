# app/api/ui_test.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.person import Person
from app.schemas.person import PersonByTokenResponse
from app.template_manager import TemplateManager
from jinja2 import TemplateNotFound
from app.core.dependencies import get_template_manager

router = APIRouter()

@router.get("/{token}", response_class=HTMLResponse)
def get_report(
    token: str,
    db: Session = Depends(get_db),
    tm: TemplateManager = Depends(get_template_manager)
):
    # tokenからperson取得
    person = db.query(Person).filter(Person.token == token).first()
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # PydanticスキーマでデータをバリデーションしてからJinja2に渡す
    person_data = PersonByTokenResponse.model_validate(person)
    
    # Jinja2テンプレートにPydanticオブジェクトを渡す
    # テンプレート内で {{ person.name }} のようにアクセス可能
    html = tm.render("ui_test.html", {"person": person_data})
    return html