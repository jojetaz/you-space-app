import sqlite3

try:
    conn = sqlite3.connect('ia_tools.db')
    cursor = conn.cursor()
    
    print("=== ESTRUCTURA DE LA BASE DE DATOS ===")
    
    # Verificar si existe la tabla categoria
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categoria'")
    if cursor.fetchone():
        print("✓ Tabla 'categoria' existe")
        
        # Mostrar estructura de la tabla categoria
        cursor.execute("PRAGMA table_info(categoria)")
        columns = cursor.fetchall()
        print("\nColumnas en tabla 'categoria':")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
            
        # Verificar si existe la columna imagen
        imagen_exists = any(col[1] == 'imagen' for col in columns)
        print(f"\n¿Existe columna 'imagen'? {'✓ SÍ' if imagen_exists else '✗ NO'}")
        
    else:
        print("✗ Tabla 'categoria' NO existe")
    
    # Verificar otras tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nTodas las tablas en la base de datos:")
    for table in tables:
        print(f"  - {table[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}") 