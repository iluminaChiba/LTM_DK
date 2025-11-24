# app/crud/__init__.py
from .person import (
    create_person,
    get_person,
    get_people,
    update_person,
    delete_person,
)

from .meal import (
    create_meal,
    get_meal,
    get_meals,
    update_meal,
    delete_meal,
)

from .supply import (
    create_supply,
    get_supply,
    get_supplies,
    update_supply,
    delete_supply,
)

from .meal_log import (
    create_meal_log,
    get_meal_log,
    get_meal_logs,
    update_meal_log,
    delete_meal_log,
)
