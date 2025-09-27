# 🐾 MS1 - Pet Adoption

Primer microservicio de los cinco microservicios que constituyen el proyecto parcial, Pet Adoption, del curso 
de Cloud Computing para el pre-grado de Computer Science.

**MS1** gestiona la información de `mascotas`, `centros de adopción`, `estados de adopción` y `vacunas`, 
incluyendo la generación masiva de datos con imágenes alojadas en **Amazon S3**.

---

## 🚀 Características
- API REST construida con **FastAPI**.
- Persistencia en **PostgreSQL**.
- Migraciones con **Alembic**.
- Datos de prueba generados con **Faker**.
- Integración con **AWS S3** para las imágenes de mascotas.
- Contenedorizado con **Docker Compose**.

---

## 📂 Estructura del proyecto

```text
ms1-mascotas/
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
├── README.md
│
├── app/                  # Código principal
│   ├── main.py           # Punto de entrada FastAPI
│   ├── factory.py        # Inicialización de la app
│   ├── config/           # Configuración Pydantic
│   ├── db/               # Sesión, migraciones
│   ├── models/           # Modelos SQLAlchemy
│   ├── routes/           # Endpoints de la API
│   ├── schemas/          # Schemas Pydantic
│   ├── services/         # Lógica de negocio
│   ├── utils/            # Utilidades
│   └── errors/           # Manejo de errores
│
├── scripts/
│   └── seed_massive.py   # Script para poblar la BD
│
├── tests/                # Pruebas unitarias e integración
│   ├── unit/
│   └── integration/
```

---

## ⚙️ Requisitos

- Python 3.11+
- PostgreSQL 15+
- [Docker](https://docs.docker.com/get-docker/)
- Cuenta en **AWS S3** con un bucket configurado

---

## 🛠️ Instalación y ejecución en VM de EC2 con Docker 🐳

1. Clonar el repositorio:
```bash
git clone https://github.com/chiru-codes/ms1-pets.git
cd ms1-mascotas
```

2. Crear un entorno virtual e instala dependencias:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configura la variables de entorno en un archivo .env:

4. Construir el contenedor
```bash
docker compose up -d
```

5. Verifica que las variables estén bien dentro del contenedor:
```bash
docker compose run --rm web env | grep AWS
```

5. Migrar la base de datos para crear todas las tablas:
```bash
docker compose run --rm web alembic upgrade head
```

6. Correr el seeder para poblar datos (puede tomar 20 min):
```bash
docker compose run --rm web python -m scripts.seed_massive
```
Documentación:
```bash
http://<PublicIPs>:8000/docs
```

---

## 📚 Endpoints

### 🐾 Pets
| Método  | Endpoint          | Descripción        |
|---------|-------------------|--------------------|
| GET     | `/pets/`          | Listar mascotas    |
| POST    | `/pets/`          | Crear mascota      |
| GET     | `/pets/{pet_id}`  | Obtener mascota    |
| PATCH   | `/pets/{pet_id}`  | Actualizar mascota |
| DELETE  | `/pets/{pet_id}`  | Eliminar mascota   |

### 🏢 Centers
| Método  | Endpoint                | Descripción       |
|---------|-------------------------|-------------------|
| GET     | `/centers/`             | Listar centros    |
| POST    | `/centers/`             | Crear centro      |
| GET     | `/centers/{center_id}`  | Obtener centro    |
| PATCH   | `/centers/{center_id}`  | Actualizar centro |
| DELETE  | `/centers/{center_id}`  | Eliminar centro   |

### 💉 Vaccines
| Método  | Endpoint                      | Descripción        |
|---------|-------------------------------|--------------------|
| GET     | `/vaccines/`                  | Listar vacunas     |
| POST    | `/vaccines/`                  | Crear vacuna       |
| GET     | `/vaccines/{vaccine_id}`      | Obtener vacuna     |
| PATCH   | `/vaccines/{vaccine_id}`      | Actualizar vacuna  |
| DELETE  | `/vaccines/{vaccine_id}`      | Eliminar vacuna    |

### 📋 Adoption Status
| Método  | Endpoint                          | Descripción                  |
|---------|-----------------------------------|------------------------------|
| GET     | `/adoption-status/{pet_id}`       | Obtener estado de adopción   |
| PATCH   | `/adoption-status/{pet_id}`       | Actualizar estado de adopción|
| DELETE  | `/adoption-status/{pet_id}`       | Eliminar estado de adopción  |
| POST    | `/adoption-status/`               | Crear estado de adopción     |

