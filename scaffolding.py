# create_domain.py
# Scaffolding para arquitectura con main.py en la raíz y DB en app/core/db.py

from pathlib import Path
import re
import sys
from textwrap import dedent


def fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(1)


domain = input("Nombre del dominio: ").strip().lower()
if not re.fullmatch(r"[a-z][a-z0-9_]*", domain):
    fail("Nombre inválido. Usa minúsculas, números y _; debe empezar por letra.")

Pascal = "".join(p.capitalize() for p in domain.split("_"))

# Rutas según tu árbol
project_root = Path(".").resolve()
app_dir = project_root / "app"
domain_dir = app_dir / "domain" / domain
routers_dir = app_dir / "routers"
main_file = project_root / "main.py"

if not main_file.exists():
    fail(
        f"No se encontró main.py en {main_file}. Ajusta el script si tu main está en app/main.py."
    )

# Crear carpetas/paquetes
domain_dir.mkdir(parents=True, exist_ok=True)
routers_dir.mkdir(parents=True, exist_ok=True)

for p in [app_dir, app_dir / "core", app_dir / "domain", domain_dir, routers_dir]:
    initf = p / "__init__.py"
    if not initf.exists():
        initf.write_text("", encoding="utf-8")

# ===== files =====

models_py = dedent(
    f"""\
    from __future__ import annotations
    from typing import Optional
    from sqlmodel import SQLModel, Field

    class {Pascal}(SQLModel, table=True):
        __tablename__ = "{domain}"
        id: Optional[int] = Field(default=None, primary_key=True)
    """
)

schemas_py = dedent(
    f"""\
    from __future__ import annotations
    from typing import Optional, List
    from sqlmodel import SQLModel

    class {Pascal}Base(SQLModel):
        pass  # añade campos compartidos aquí

    class {Pascal}Create({Pascal}Base):
        pass  # campos requeridos para crear

    class {Pascal}Read({Pascal}Base):
        id: int

    class {Pascal}Page(SQLModel):
        total: int
        items: List[{Pascal}Read]
    """
)

repository_py = dedent(
    f"""\
    from typing import Sequence
    from sqlmodel import Session, select
    from sqlalchemy import func
    from .models import {Pascal}

    class {Pascal}Repository:
        def __init__(self, session: Session):
            self.session = session

        def list(self, offset: int = 0, limit: int = 50) -> Sequence[{Pascal}]:
            stmt = select({Pascal}).offset(offset).limit(limit)
            return self.session.exec(stmt).all()

        def count(self) -> int:
            stmt = select(func.count()).select_from({Pascal})
            return int(self.session.exec(stmt).one())

        def create(self, obj: {Pascal}) -> {Pascal}:
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
    """
)

service_py = dedent(
    f"""\
    from typing import List
    from sqlmodel import Session
    from .models import {Pascal}
    from .repository import {Pascal}Repository
    from .schemas import {Pascal}Create

    class {Pascal}Service:
        def __init__(self, session: Session):
            self.repo = {Pascal}Repository(session)

        def list_with_total(self, offset: int, limit: int) -> tuple[list[{Pascal}], int]:
            items_seq = self.repo.list(offset=offset, limit=limit)
            items: List[{Pascal}] = list(items_seq)
            total = self.repo.count()
            return items, total

        def create(self, data: {Pascal}Create) -> {Pascal}:
            # CORREGIDO: convertir schema a dict
            obj = {Pascal}.model_validate(data.model_dump())
            return self.repo.create(obj)
    """
)

router_py = dedent(
    f"""\
    from fastapi import APIRouter, Depends
    from sqlmodel import Session
    from app.core.db import get_session
    from app.domain.{domain}.service import {Pascal}Service
    from app.domain.{domain}.schemas import {Pascal}Create, {Pascal}Read, {Pascal}Page

    router = APIRouter(prefix="/{domain}", tags=["{domain}"])

    def get_service(session: Session = Depends(get_session)) -> {Pascal}Service:
        return {Pascal}Service(session)

    @router.get("", response_model={Pascal}Page)
    def list_{domain}(offset: int = 0, limit: int = 50, svc: {Pascal}Service = Depends(get_service)):
        items, total = svc.list_with_total(offset=offset, limit=limit)
        return {Pascal}Page(total=total, items=items)

    @router.post("", response_model={Pascal}Read)
    def create_{domain}(payload: {Pascal}Create, svc: {Pascal}Service = Depends(get_service)):
        return svc.create(payload)
    """
)

(domain_dir / "models.py").write_text(models_py, encoding="utf-8")
(domain_dir / "schemas.py").write_text(schemas_py, encoding="utf-8")
(domain_dir / "repository.py").write_text(repository_py, encoding="utf-8")
(domain_dir / "service.py").write_text(service_py, encoding="utf-8")
(routers_dir / f"{domain}.py").write_text(router_py, encoding="utf-8")

# ===== registrar en main.py =====
main_txt = main_file.read_text(encoding="utf-8")

import_stmt = f"from app.routers.{domain} import router as {domain}_router"
include_stmt = f"app.include_router({domain}_router)"

if import_stmt not in main_txt:
    lines = main_txt.splitlines()
    last_import_idx = 0
    for i, l in enumerate(lines):
        if l.startswith("from ") or l.startswith("import "):
            last_import_idx = i
    lines.insert(last_import_idx + 1, import_stmt)
    main_txt = "\n".join(lines)

if include_stmt not in main_txt:
    if "app = FastAPI" in main_txt and "include_router" in main_txt:
        lines = main_txt.splitlines()
        idxs = [i for i, l in enumerate(lines) if "include_router" in l]
        insert_at = idxs[-1] + 1 if idxs else len(lines)
        lines.insert(insert_at, include_stmt)
        main_txt = "\n".join(lines) + "\n"
    else:
        main_txt += "\n" + include_stmt + "\n"

main_file.write_text(main_txt, encoding="utf-8")

print(f"✅ Dominio creado en: {domain_dir}")
print(f"✅ Router creado en: {routers_dir / (domain + '.py')}")
print("✅ Router registrado en main.py")
