from __future__ import annotations
from pathlib import Path
from typing import Optional

# Carpeta local usada por defecto para las exportaciones.
DEFAULT_EXPORT_DIR = Path(__file__).resolve().parent.parent / "exports"
# Garantizamos que exista desde el arranque del módulo.
DEFAULT_EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def _normalizar_directorio(ruta: Optional[str]) -> Optional[Path]:
    if not ruta:
        return None
    path = Path(ruta).expanduser()
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    return path if path.is_dir() else None

def _ruta_configurada_por_usuario(usuario: Optional[str]) -> Optional[Path]:
    """Obtiene la ruta de exportación almacenada en la cuenta del usuario."""
    if not usuario:
        return None
    try:
        from models import usuarios  # Importación perezosa para evitar ciclos.
        datos = usuarios.obtener_datos_usuario(usuario)
    except Exception:
        # Si hay cualquier problema con la consulta (p.ej. conexión),
        # devolvemos ``None`` para usar la carpeta por defecto.
        return None
    if not datos:
        return None
    return _normalizar_directorio(datos.get("ruta_export"))

def resolver_ruta_exportacion(*, usuario: Optional[str] = None, ruta_destino: Optional[str] = None) -> Path:
    ruta = _normalizar_directorio(ruta_destino)
    if ruta:
        return ruta
    ruta_usuario = _ruta_configurada_por_usuario(usuario)
    if ruta_usuario:
        return ruta_usuario
    return DEFAULT_EXPORT_DIR