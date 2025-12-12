from app.dto.jabatan_dto import (
    jabatan_schema, 
    jabatan_list_schema, 
    jabatan_create_schema, 
    jabatan_update_schema
)
from app.dto.status_kerja_dto import (
    status_kerja_schema, 
    status_kerja_list_schema, 
    status_kerja_create_schema, 
    status_kerja_update_schema
)
from app.dto.karyawan_dto import (
    karyawan_schema, 
    karyawan_list_schema, 
    karyawan_create_schema, 
    karyawan_update_schema
)

from app.dto.status_pernikahan_dto import (
    status_pernikahan_schema,
    status_pernikahan_list_schema,
    status_pernikahan_create_schema,
    status_pernikahan_update_schema
)

from app.dto.departemen_dto import (
    departemen_schema,
    departemen_list_schema,
    departemen_create_schema,
    departemen_update_schema
)   

from app.dto.agama_dto import (
    agama_schema,
    agama_list_schema,
    agama_create_schema,
    agama_update_schema
)

__all__ = [
    'jabatan_schema', 'jabatan_list_schema', 'jabatan_create_schema', 'jabatan_update_schema',
    'status_kerja_schema', 'status_kerja_list_schema', 'status_kerja_create_schema', 'status_kerja_update_schema',
    'karyawan_schema', 'karyawan_list_schema', 'karyawan_create_schema', 'karyawan_update_schema'
    'status_pernikahan_schema',
    'status_pernikahan_list_schema',
    'status_pernikahan_create_schema',
    'status_pernikahan_update_schema',
    'departemen_schema',
    'departemen_list_schema',
    'departemen_create_schema',
    'departemen_update_schema',
    'agama_schema',
    'agama_list_schema',
    'agama_create_schema',
    'agama_update_schema'
]