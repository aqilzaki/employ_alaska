from flask.cli import with_appcontext
import click
from sqlalchemy import inspect

@click.command("sync-db")
@with_appcontext
def sync_db():
    """
    Sinkronisasi tabel database agar mengikuti model SQLAlchemy
    tanpa menghapus data.
    """

    # Import DI DALAM function → FIX circular import
    from app import db

    engine = db.engine
    inspector = inspect(engine)

    click.echo("🔍 Mengecek struktur database...")

    # Ambil semua model
    models = db.Model.__subclasses__()
    
    for model in models:
        table_name = model.__tablename__
        click.echo(f"\n📌 Memproses tabel: {table_name}")

        # Cek apakah tabel sudah ada
        if not inspector.has_table(table_name):
            click.echo(f"  ➕ Membuat tabel {table_name}")
            model.__table__.create(engine)
            continue

        # ============================================
        # CEK KOLOM
        # ============================================
        existing_cols = [c["name"] for c in inspector.get_columns(table_name)]

        for col in model.__table__.columns:
            if col.name not in existing_cols:
                col_type = str(col.type)
                nullable = "NULL" if col.nullable else "NOT NULL"

                sql = f"ALTER TABLE {table_name} ADD COLUMN {col.name} {col_type} {nullable};"
                click.echo(f"  🔧 Menambah kolom {col.name}")
                engine.execute(sql)

        # ============================================
        # CEK FOREIGN KEY
        # ============================================
        existing_fk = inspector.get_foreign_keys(table_name)
        existing_fk_cols = [fk["constrained_columns"][0] for fk in existing_fk]

        for fk in model.__table__.foreign_keys:
            fk_col = fk.parent.name
            ref_table = fk.column.table.name
            ref_col = fk.column.name

            if fk_col not in existing_fk_cols:
                click.echo(f"  🔗 Menambah FK {fk_col} → {ref_table}.{ref_col}")
                sql = f"""
                ALTER TABLE {table_name}
                ADD CONSTRAINT fk_{table_name}_{fk_col}
                FOREIGN KEY ({fk_col}) REFERENCES {ref_table}({ref_col});
                """
                engine.execute(sql)

    click.echo("\n✅ SINKRONISASI SELESAI! Database sudah mengikuti model.")
