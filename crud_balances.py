from mysql.connector import Error
import conexion

db = conexion.Conexion()

class crud_balances:
    def consultar(self, idCliente=""):
        # Consulta los balances de un cliente específico o todos si está vacío
        if idCliente and str(idCliente).strip() != "":
            try:
                id_c = int(idCliente)
                sql = f"""
                    SELECT b.*, c.nombre AS cliente_nombre 
                    FROM balances b 
                    INNER JOIN clientes c ON b.idCliente = c.idCliente 
                    WHERE b.idCliente = {id_c} 
                    ORDER BY b.fecha DESC
                """
            except ValueError:
                return []
        else:
            sql = """
                SELECT b.*, c.nombre AS cliente_nombre 
                FROM balances b 
                INNER JOIN clientes c ON b.idCliente = c.idCliente 
                ORDER BY b.fecha DESC
            """
        return db.consultar(sql)

    def administrar(self, datos):
        try:
            if datos['accion'] == 'nuevo':
                sql = """
                    INSERT INTO balances (idCliente, monto, fecha, concepto)
                    VALUES (%s, %s, %s, %s)
                """
                valores = (
                    datos['idCliente'],
                    datos['monto'],
                    datos['fecha'],  # Formato: 'YYYY-MM-DD HH:MM:SS'
                    datos.get('concepto', '')
                )
            elif datos['accion'] == 'modificar':
                sql = """
                    UPDATE balances 
                    SET monto=%s, fecha=%s, concepto=%s
                    WHERE idBalance=%s
                """
                valores = (
                    datos['monto'],
                    datos['fecha'],
                    datos.get('concepto', ''),
                    datos['idBalance']
                )
            else:  # eliminar
                sql = "DELETE FROM balances WHERE idBalance=%s"
                valores = (datos['idBalance'],)
                
            return db.ejecutar(sql, valores)
        except Error as e:
            return f"Error al procesar el balance: {e}"