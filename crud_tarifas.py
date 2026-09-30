from mysql.connector import Error # type: ignore
import conexion

db = conexion.Conexion()

class crud_tarifas:
    def consultar(self, buscar=""):
        if buscar and str(buscar).strip() != "":
            try:
                monto = float(buscar)
                sql = f"SELECT * FROM tabla_tarifaria WHERE desde <= {monto} AND hasta >= {monto}"
            except ValueError:
                return []
        else:
            sql = "SELECT * FROM tabla_tarifaria ORDER BY desde ASC"
        return db.consultar(sql)

    def administrar(self, datos):
        try:
            if datos['accion'] == 'nuevo':
                sql = """
                    INSERT INTO tabla_tarifaria(desde, hasta, precio_base, adicional, porcentaje)
                    VALUES(%s, %s, %s, %s, %s)
                """
                valores = (
                    datos['desde'],
                    datos['hasta'],
                    datos['precio_base'],
                    datos['adicional'],
                    datos['porcentaje']
                )
            elif datos['accion'] == 'modificar':
                sql = """
                    UPDATE tabla_tarifaria 
                    SET desde=%s, hasta=%s, precio_base=%s, adicional=%s, porcentaje=%s
                    WHERE idTarifa=%s
                """
                valores = (
                    datos['desde'],
                    datos['hasta'],
                    datos['precio_base'],
                    datos['adicional'],
                    datos['porcentaje'],
                    datos['idTarifa']
                )
            else:
                sql = "DELETE FROM tabla_tarifaria WHERE idTarifa=%s"
                valores = (datos['idTarifa'],)
            return db.ejecutar(sql, valores)
        except Error as e:
            return f"Error al guardar la tarifa: {e}"