# Backend

## Estructura de carpetas

El proyecto sigue una arquitectura limpia (Clean Architecture) con separación por dominios:

```
hello-world-backend/
├── src/
│   ├── api/                    # Configuración central de routers API
│   │   ├── router.py
│   │   └── v1/
│   │       └── router.py
│   ├── auth/                   # Dominio de autenticación
│   │   ├── api/
│   │   ├── application/
│   │   │   ├── service/
│   │   │   └── usecase/        # Casos de uso de autenticación
│   │   └── infrastructure/
│   │       └── security.py     # JWT y seguridad
│   ├── game/                   # Dominio de juegos
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── v1/
│   │   │       ├── endpoints/  # Un archivo por endpoint
│   │   │       │   ├── create_game.py
│   │   │       │   ├── get_game.py
│   │   │       │   └── ...
│   │   │       ├── schemas/    # Pydantic schemas
│   │   │       └── router.py
│   │   ├── application/
│   │   │   ├── service/        # Servicios de negocio
│   │   │   └── usecase/        # Casos de uso
│   │   ├── domain/             # Entidades de dominio
│   │   │   ├── game.py
│   │   │   ├── level.py
│   │   │   └── ...
│   │   └── infrastructure/
│   │       └── repositories/   # Repositorios
│   ├── shared/                 # Componentes compartidos
│   │   ├── application/
│   │   │   └── usecase/
│   │   │       └── base_service.py
│   │   ├── domain/
│   │   │   └── exceptions.py   # Excepciones personalizadas
│   │   ├── infrastructure/
│   │   │   ├── base.py         # Base de SQLAlchemy
│   │   │   ├── config.py       # Configuración
│   │   │   ├── models.py       # Modelos base
│   │   │   ├── repositories/
│   │   │   │   └── base_repository.py
│   │   │   └── session.py      # Gestión de sesiones DB
│   │   └── seed/               # Scripts de seed
│   ├── statistic/              # Dominio de estadísticas
│   ├── sync/                   # Dominio de sincronización
│   └── users/                  # Dominio de usuarios
│       ├── api/
│       ├── application/
│       ├── domain/
│       └── infrastructure/
├── tests/                      # Tests organizados por dominio
│   ├── conftest.py            # Fixtures globales
│   ├── auth/                  # Tests de autenticación
│   ├── users/                 # Tests de usuarios
│   └── ...
├── alembic/                   # Migraciones de base de datos
├── migrations/                # Configuración de Alembic
├── main.py                    # Punto de entrada FastAPI
└── pyproject.toml            # Configuración del proyecto
```

## Convención de nombres

### General

| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Clases | PascalCase | `UserService`, `CreateUserUseCase` |
| Funciones | snake_case | `get_by_id`, `execute` |
| Variables | snake_case | `user_id`, `user_data` |
| Constantes | UPPER_CASE | `DATABASE_URL`, `SECRET_KEY` |
| Archivos de endpoint | {action}.py | `create_user.py`, `login.py` |
| Módulos | snake_case | `user_service.py` |

### Estructura de nombres por capa

**Servicios** (`src/{domain}/application/service/`):
- Heredan de `BaseService`
- Nombre: `{Entidad}Service`
- Ejemplo: `UserService`, `GameService`

**UseCases** (`src/{domain}/application/usecase/`):
- Nombre: `{Accion}{Entidad}UseCase`
- Método principal: `execute()`
- Ejemplo: `AuthenticateUseCase`, `RegisterUserUseCase`

**Endpoints** (`src/{domain}/api/v1/endpoints/`):
- Un endpoint por archivo
- Nombre del archivo: `{accion}_{entidad}.py`
- Router con prefijo específico
- Ejemplo: `create_user.py`, `get_game.py`

**Repositorios** (`src/{domain}/infrastructure/repositories/`):
- Nombre: `{Entidad}Repository`
- Ejemplo: `UserRepository`, `GameRepository`

**Schemas** (`src/{domain}/api/v1/schemas/`):
- Nombre: `{Accion}{Entidad}Response`, `{Entidad}Create`, `{Entidad}Response`
- Ejemplo: `UserCreate`, `UserResponse`, `SingleUserResponse`

### Imports

Orden de imports (separados por líneas en blanco):

1. Librerías estándar (stdlib)
2. Librerías de terceros (third-party)
3. Imports locales

```python
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.config import settings
from src.shared.application.usecase.base_service import BaseService
from src.users.application.service.user_service import UserService
from src.users.api.v1.schemas.user import UserCreate
```

## Linting, identación, formateo

### Configuración actual

El proyecto utiliza `pyproject.toml` como archivo de configuración central. Actualmente **no hay herramientas de linting/formateo configuradas explícitamente** en `pyproject.toml`.

### Python

- **Versión mínima**: Python 3.14
- **Indentación**: 4 espacios (PEP 8)
- **Longitud máxima de línea**: 100 caracteres (recomendado)
- **Encoding**: UTF-8

### Herramientas recomendadas

Se recomienda agregar al `pyproject.toml`:

```toml
[tool.black]
line-length = 100
target-version = ['py314']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

[tool.flake8]
max-line-length = 100
extend-ignore = ["E203", "W503"]

[tool.mypy]
python_version = "3.14"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### Estilo de código

- Usar type hints en todas las funciones y métodos
- Documentar con docstrings (Google style o NumPy style)
- Máximo 4 niveles de indentación anidada
- Una clase por archivo (recomendado)
- Líneas en blanco:
  - 2 líneas entre clases
  - 1 línea entre métodos
  - 1 línea entre secciones de imports

## Manejo de errores

### Excepciones personalizadas

Ubicadas en `src/shared/domain/exceptions.py`:

```python
class AppException(HTTPException)
├── NotFoundException           # 404 - Recurso no encontrado
├── DuplicateEntryException     # 400 - Recurso duplicado
├── InvalidCredentialsException # 401 - Credenciales inválidas
├── UnauthorizedException       # 403 - No autorizado
└── DatabaseException          # 500 - Error de base de datos
```

### Uso en servicios

Los servicios lanzan excepciones de dominio:

```python
from src.shared.domain.exceptions import NotFoundException, DatabaseException

async def get_by_id(self, id: int):
    try:
        result = await self.repository.get_by_id(id)
        return result
    except Exception as e:
        raise DatabaseException(f"Error al buscar: {str(e)}")
```

### Uso en endpoints

Los endpoints capturan excepciones y convierten a HTTPException:

```python
from fastapi import HTTPException, status
from src.shared.domain.exceptions import DuplicateEntryException

@router.post("/")
async def create_user(user_data: UserCreate):
    try:
        user = await user_service.create_user(user_data)
        return SingleUserResponse(message="Usuario creado", data=user)
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
```

### Validaciones en BaseService

El `BaseService` proporciona métodos de validación:

- `_validate_id(id)` - Verifica que el ID sea entero positivo
- `_validate_pagination(skip, limit)` - Valida parámetros de paginación
- `_validate_data_not_empty(data, operation)` - Verifica datos no vacíos

### Logging

Usar el logger configurado en cada módulo:

```python
import logging

logger = logging.getLogger(__name__)

# Niveles de log
logger.debug("Mensaje de debug")
logger.info("Mensaje informativo")
logger.warning("Advertencia")
logger.error("Error")
```

## Pruebas

### Estructura de tests

```
tests/
├── conftest.py              # Fixtures globales y configuración
├── auth/                    # Tests de autenticación
│   ├── conftest.py         # Fixtures específicos de auth
│   ├── test_authenticate_usecase.py
│   ├── test_register_user_usecase.py
│   └── test_security.py
└── users/                   # Tests de usuarios
    ├── conftest.py
    ├── test_user_service.py
    └── test_repository.py
```

### Framework

- **pytest**: Framework principal de testing
- **pytest-asyncio**: Soporte para tests async
- **unittest.mock**: Mocking (AsyncMock, MagicMock, patch)
- **httpx.AsyncClient**: Cliente HTTP para tests de integración

### Fixtures principales (conftest.py)

```python
# Base de datos en memoria para tests
@pytest.fixture(scope="session")
async def test_db():
    TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    # Crear tablas, yield session, cleanup

# Cliente HTTP con DB de test
@pytest.fixture
async def test_client(test_db: AsyncSession):
    # Override de dependencias, crear cliente

# Datos de prueba
@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "role_id": None,
    }
```

### Tipos de tests

**Tests unitarios** (UseCases, Services):

```python
class TestAuthenticateUseCase:
    @pytest.mark.asyncio
    async def test_execute_successful_authentication(self, mock_user):
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(return_value=mock_user)
        
        with patch("...UserRepository", return_value=mock_user_repo):
            uc = AuthenticateUseCase(db=mock_db)
            result = await uc.execute(email="test@example.com", password="password")
            assert result.access_token is not None
```

**Tests de integración** (Endpoints):

```python
@pytest.mark.asyncio
async def test_create_user_endpoint(test_client: AsyncClient):
    response = await test_client.post("/api/v1/users/", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "SecurePass123!",
        "role_id": 1
    })
    assert response.status_code == 201
```

### Convenciones de tests

- Usar clases para agrupar tests relacionados
- Nombres descriptivos: `test_{accion}_{escenario}`
- Marcadores: `@pytest.mark.asyncio` para funciones async
- Comentarios indicando qué defecto se detecta
- Tests de casos límite y edge cases
- Tests de seguridad (SQL injection, XSS)
- Tests de concurrencia cuando aplique

### Ejecución de tests

```bash
# Todos los tests
pytest

# Un archivo específico
pytest tests/test_user.py

# Una función específica
pytest tests/test_user.py::test_create_user

# Con cobertura
pytest --cov=src --cov-report=html
```

### Patrones de testing

1. **Arrange-Act-Assert**: Preparar datos, ejecutar, verificar
2. **Given-When-Then**: Contexto, acción, resultado esperado
3. **Un assert por test** (idealmente)
4. **Independencia**: Cada test debe poder ejecutarse solo
5. **Mocking**: Aislar dependencias externasi
6. **Fixtures**: Reutilizar configuración de test
