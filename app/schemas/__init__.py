# app/schemas/__init__.py
from .person import (
    Person,
    PersonCreate,
    PersonUpdate,
)

from .meal import (
    Meal,
    MealCreate,
    MealUpdate,
)

from .supply import (
    Supply,
    SupplyCreate,
    SupplyUpdate,
)

from .meal_log import (
    MealLog,
    MealLogCreate,
    MealLogUpdate,
)

from .allergy import (
    Allergy,
    AllergyCreate,
    AllergyUpdate,
)

from .pending_box import (
    PendingBox,
    PendingBoxCreate,
    PendingBoxUpdate,
)

from .daily_stock import (
    DailyStock,
    DailyStockCreate,
    DailyStockUpdate,
)

from .order import (
    Order,
    OrderCreate,
    OrderUpdate,
)
