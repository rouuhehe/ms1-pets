from typing import Any, Dict, Optional, Sequence
from sqlalchemy.orm import Query, Session


def paginate_query(
        query: Query,
        page: int = 1,
        page_size: int = 10,
        db: Optional[Session] = None
) -> Dict[str, Any]:
    """
    Pagina una consulta SQLAlchemy.

    Args:
        query (Query): Consulta SQLAlchemy.
        page (int, opcional): Página actual (empieza en 1). Por defecto 1.
        page_size (int, opcional): Número de resultados por página. Por defecto 16.
        db (Session, opcional): Sesión de SQLAlchemy (si necesitas ejecutar count separado).

    Returns:
        Dict con metadata y resultados.
    """

    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 16

    total = query.count()

    offset = (page - 1) * page_size
    items: Sequence[Any] = query.offset(offset).limit(page_size).all()

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
        "results": items,
    }
