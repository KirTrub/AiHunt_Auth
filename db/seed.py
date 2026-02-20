import asyncio
from sqlalchemy import select, text
from db.session import async_session
from models.permissions import Permission
from models.resources import Resource
from models.role import Role
from models.user import User
from models.product import Product
from models.article import Article

from security import hash_password



ROLES = [
    {"id": 1, "name": "Admin"},
    {"id": 2, "name": "Creator"},
    {"id": 3, "name": "User"},
]


RESOURCES = [
    {"id": 1, "name": "product"},
    {"id": 2, "name": "article"},
    {"id": 3, "name": "user"},
]


PERMISSIONS_MAP = [
    # ADMIN
    (1, 1, {"create_perm": True, "read_perm": True, "read_all_perm": True, "update_perm": True, "update_all_perm": True, "delete_perm": True, "delete_all_perm": True}),
    (1, 2, {"create_perm": True, "read_perm": True, "read_all_perm": True, "update_perm": True, "update_all_perm": True, "delete_perm": True, "delete_all_perm": True}),
    (1, 3, {"create_perm": True, "read_perm": True, "read_all_perm": True, "update_perm": True, "update_all_perm": True, "delete_perm": True, "delete_all_perm": True}),

    # CREATOR
    (2, 1, {"create_perm": True, "read_perm": True, "read_all_perm": True, "update_perm": True, "delete_perm": True}),
    (2, 2, {"create_perm": True, "read_perm": True, "read_all_perm": True, "update_perm": True, "delete_perm": True}),
    (2, 3, {"read_perm": True, "update_perm": True, "delete_perm": True}),

    # USER
    (3, 1, {"read_all_perm": True}),
    (3, 2, {"read_all_perm": True}),
    (3, 3, {"read_perm": True, "update_perm": True, "delete_perm": True}),
]


MOCK_USERS = [
    {"id": 2, "first_name": "Ivan", "last_name": "Creator", "email": "creator@aihunt.com", "password_hashed": hash_password("123"), "role_id": 2},
    {"id": 3, "first_name": "Petr", "last_name": "User", "email": "user1@aihunt.com", "password_hashed": hash_password("123"), "role_id": 3},
    {"id": 4, "first_name": "Anna", "last_name": "User", "email": "user2@aihunt.com", "password_hashed": hash_password("123"), "role_id": 3},
]


MOCK_PRODUCTS = [
    {"id": 1, "resource_type_id": 1, "name": "Кофемашина эспрессо", "description": "Давление 15 бар, встроенная кофемолка", "price": 35000, "owner_id": 2},
    {"id": 2, "resource_type_id": 1, "name": "Электросамокат CityDrive", "description": "Запас хода 30 км, складная конструкция", "price": 28000, "owner_id": 3},
    {"id": 3, "resource_type_id": 1, "name": "Набор для йоги", "description": "Коврик, два блока и ремень в чехле", "price": 4500, "owner_id": 4},
    {"id": 4, "resource_type_id": 1, "name": "Гриль электрический", "description": "Съемные панели, антипригарное покрытие", "price": 12000, "owner_id": 2},
    {"id": 5, "resource_type_id": 1, "name": "Умный сад на подоконнике", "description": "Автоматический полив и LED-освещение", "price": 8000, "owner_id": 3},
    {"id": 6, "resource_type_id": 1, "name": "Рюкзак туристический 60л", "description": "Анатомическая спинка, чехол от дождя", "price": 15000, "owner_id": 4},
    {"id": 7, "resource_type_id": 1, "name": "Набор инструментов (82 предмета)", "description": "Хром-ванадиевая сталь, ударопрочный кейс", "price": 9500, "owner_id": 2},
    {"id": 8, "resource_type_id": 1, "name": "Кресло-кокон подвесное", "description": "Выдерживает до 150 кг, мягкая подушка в комплекте", "price": 19000, "owner_id": 3},
    {"id": 9, "resource_type_id": 1, "name": "Проектор для домашнего кинотеатра", "description": "Поддержка Full HD, встроенные динамики", "price": 25000, "owner_id": 4},
    {"id": 10, "resource_type_id": 1, "name": "Велосипед горный 21 скорость", "description": "Алюминиевая рама, дисковые тормоза", "price": 42000, "owner_id": 2},
]


MOCK_ARTICLES = [
    {"id": 1, "resource_type_id": 2, "name": "Секреты идеального стейка", "text": "Как выбрать мясо и почему важен «отдых» после прожарки...", "owner_id": 2},
    {"id": 2, "resource_type_id": 2, "name": "История забытых цивилизаций", "text": "Тайны древних городов, скрытых в джунглях Амазонки...", "owner_id": 3},
    {"id": 3, "resource_type_id": 2, "name": "Искусство прокрастинации", "text": "Почему мы откладываем дела и как обмануть свой мозг...", "owner_id": 4},
    {"id": 4, "resource_type_id": 2, "name": "Путеводитель по Исландии", "text": "Маршрут по долине гейзеров и лучшим водопадам острова...", "owner_id": 2},
    {"id": 5, "resource_type_id": 2, "name": "Выращивание микрозелени", "text": "Пошаговое руководство: от выбора семян до первого урожая...", "owner_id": 3},
    {"id": 6, "resource_type_id": 2, "name": "Влияние классической музыки", "text": "Как прослушивание Моцарта меняет продуктивность работы...", "owner_id": 4},
    {"id": 7, "resource_type_id": 2, "name": "Мифы о правильном питании", "text": "Разбираем, вреден ли глютен и сколько воды нужно пить...", "owner_id": 2},
    {"id": 8, "resource_type_id": 2, "name": "Архитектура модернизма", "text": "Основные черты стиля и самые знаковые здания XX века...", "owner_id": 3},
    {"id": 9, "resource_type_id": 2, "name": "Основы финансовой грамотности", "text": "Как вести бюджет и начать инвестировать с малых сумм...", "owner_id": 4},
    {"id": 10, "resource_type_id": 2, "name": "Йога для начинающих", "text": "Пять простых асан для снятия стресса после рабочего дня...", "owner_id": 2}
]



async def seed_all():
    from db.session import engine, Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():

            # ROLES
            for r_data in ROLES:
                res = await session.execute(select(Role).filter_by(id=r_data["id"]))
                if not res.scalar_one_or_none():
                    session.add(Role(**r_data))

            # RESOURCES
            for res_data in RESOURCES:
                db_res = await session.execute(select(Resource).filter_by(id=res_data["id"]))
                if not db_res.scalar_one_or_none():
                    session.add(Resource(**res_data))

            await session.flush()

            # PERMISSIONS
            for role_id, resource_id, perms in PERMISSIONS_MAP:
                check = await session.execute(
                    select(Permission).filter_by(role_id=role_id, resource_id=resource_id)
                )
                if not check.scalar_one_or_none():
                    session.add(Permission(role_id=role_id, resource_id=resource_id, **perms))

            # ADMIN
            admin_check = await session.execute(select(User).filter_by(email="admin@aihunt.com"))
            if not admin_check.scalar_one_or_none():
                session.add(User(
                    id=1,
                    first_name="Admin",
                    last_name="System",
                    email="admin@aihunt.com",
                    password_hashed=hash_password("123"),
                    role_id=1
                ))

            # MOCK USERS
            for user_data in MOCK_USERS:
                check = await session.execute(select(User).filter_by(id=user_data["id"]))
                if not check.scalar_one_or_none():
                    session.add(User(**user_data))

            await session.flush()

            # MOCK PRODUCTS
            for product_data in MOCK_PRODUCTS:
                check = await session.execute(select(Product).filter_by(id=product_data["id"]))
                if not check.scalar_one_or_none():
                    session.add(Product(**product_data))

            # MOCK ARTICLES
            for article_data in MOCK_ARTICLES:
                check = await session.execute(select(Article).filter_by(id=article_data["id"]))
                if not check.scalar_one_or_none():
                    session.add(Article(**article_data))

            tables = ["users", "products", "articles", "roles", "resources"]
    
            for table in tables:
                await session.execute(text(
                    f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), coalesce(max(id), 1), max(id) IS NOT NULL) FROM {table};"))
        await session.commit()
        print("Seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_all())
