from database.DB_connect import DBConnect
from model.go_products import Go_products
from model.connessione import Connessione


class DAO:
    @staticmethod
    def getAllColors():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT gp.Product_color as color
                FROM go_products gp 
                """
        cursor.execute(query)
        for row in cursor:
            result.append(row['color'])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodesColor(color):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT gp.*
                FROM go_products gp 
                WHERE gp.Product_color = %s
                """
        cursor.execute(query, (color,))
        for row in cursor:
            result.append(Go_products(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMap, color, year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT gp1.Product_number as p1, gp2.Product_number as p2, COUNT(DISTINCT gds1.`Date`) as peso
                FROM go_products gp1, go_products gp2, go_daily_sales gds1, go_daily_sales gds2
                WHERE YEAR(gds1.`Date`) = %s
                AND YEAR(gds2.`Date`) = YEAR(gds1.`Date`)
                AND gp2.Product_number = gds2.Product_number 
                AND gp1.Product_number = gds1.Product_number 
                AND gp1.Product_number < gp2.Product_number 
                AND gds1.`Date` = gds2.`Date`
                AND gds1.Retailer_code = gds2.Retailer_code 
                AND gp1.Product_color = %s 
                AND gp1.Product_color = gp2.Product_color
                GROUP BY gp1.Product_number, gp2.Product_number
                """
        cursor.execute(query, (year, color))
        for row in cursor:
            result.append(Connessione(idMap[row['p1']], idMap[row['p2']], row['peso']))
        cursor.close()
        conn.close()
        return result
