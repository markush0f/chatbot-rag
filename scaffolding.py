from pathlib import Path
import re
import sys
from textwrap import dedent
import argparse

# ======= argumentos =======
parser = argparse.ArgumentParser(
    description="Generador de módulos para FastAPI sin base de datos."
)
parser.add_argument("-router", action="store_true", help="Generar solo el router.")
parser.add_argument("-service", action="store_true", help="Generar solo el servicio.")
args = parser.parse_args()

# ======= función de fallo =======
def fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(1)

# ======= input dominio =======
domain = input("Nombre del dominio: ").strip().lower()
if not re.fullmatch(r"[a-z][a-z0-9_]*", domain):
    fail("Nombre inválido. Usa minúsculas, números y _; debe empezar por letra.")

Pascal = "".join(p.capitalize() for p in domain.split("_"))

# ======= rutas =======
project_root = Path(".").resolve()
app_dir = project_root / "app"
domain_dir = app_dir / "domain" / domain
routers_dir = app_dir / "routers"
main_file = app_dir / "main.py"

if not main_file.exists():
    fail("No se encontró main.py. Ajusta la ruta si tu main está en otro sitio.")

# ======= crear carpetas/paquetes =======
domain_dir.mkdir(parents=True, exist_ok=True)
routers_dir.mkdir(parents=True, exist_ok=True)

for p in [app_dir, app_dir / "core", app_dir / "domain", domain_dir, routers_dir]:
    initf = p / "__init__.py"
    if not initf.exists():
        initf.write_text("", encoding="utf-8")

# ======= contenidos =======

service_py = dedent(
    f"""
class {Pascal}Service:
    def __init__(self):
        # Inicializa dependencias si las necesitas (FAISS, APIs externas, etc.)
        pass

    def process(self, data: str) -> str:
        # Ejemplo de función lógica
        return f"Procesado: {{data}}"
"""
)

router_py = dedent(
    f"""
from fastapi import APIRouter, Form
from app.domain.{domain}.service import {Pascal}Service

router = APIRouter(prefix="/{domain}", tags=["{domain}"])

svc = {Pascal}Service()

@router.post("/process")
def process_data(data: str = Form(...)):
    result = svc.process(data)
    return {{"result": result}}
"""
)

# ======= escritura condicional =======
generate_all = not (args.router or args.service)

if generate_all or args.service:
    (domain_dir / "service.py").write_text(service_py, encoding="utf-8")
    print(f"✅ Service creado en: {domain_dir}")

if generate_all or args.router:
    (routers_dir / f"{domain}.py").write_text(router_py, encoding="utf-8")
    print(f"✅ Router creado en: {routers_dir / (domain + '.py')}")

# ======= registrar en main.py solo si se genera el router =======
if generate_all or args.router:
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
    print("✅ Router registrado en main.py")
