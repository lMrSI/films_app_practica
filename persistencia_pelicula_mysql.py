#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import mysql.connector
import logging

class Persistencia_pelicula_mysql(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        self._conn = mysql.connector.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                database=credencials["database"]
                )
        if not self.check_table():
            self.create_table()

    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True
    
    def count(self) -> int:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        count = cursor.rowcount
        return count
    
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        mycursor = self._conn.cursor(buffered=True)
        peliculas = []
        if id is not None:
            mycursor.execute("SELECT * FROM PELICULA WHERE ID = %s LIMIT 10", (id,))
        else:
            mycursor.execute("SELECT * FROM PELICULA")
        for x in mycursor:
            pelicula = Pelicula(x[0], x[1], x[2], x[3])
            peliculas.append(pelicula)
        return peliculas 
        
    def desa(self, pelicula: Pelicula) -> Pelicula:
        try:
            mycursor = self._conn.cursor(buffered=True)
            
            # Verificar si la película ya existe
            mycursor.execute("SELECT * FROM PELICULA WHERE TITULO = %s", (pelicula.titol,))
            existPelicula = mycursor.fetchone()

            if not existPelicula:
                # Insertar la película si no existe
                query = "INSERT INTO PELICULA (TITULO, ANYO, PUNTUACION, VOTOS) VALUES (%s, %s, %s, %s)"
                values = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots)
                mycursor.execute(query, values)
                self._conn.commit()
                print("Película insertada")
            else:
                print("Este título ya existe. No se permiten títulos duplicados")

            return pelicula
        except Exception as e:
            # Manejar cualquier excepción que pueda ocurrir
            print(f"Error al insertar la película: {e}")
            self._conn.rollback()
    
    def llegeix(self, any: int) -> List[Pelicula]:
        mycursor = self._conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM PELICULA WHERE ANYO = %s", (any,))
        peliculas = []
        for x in mycursor:
            pelicula = Pelicula(x[0], x[1], x[2], x[3])
            peliculas.append(pelicula)
        return peliculas
    
    def llegeix(self, any: int) -> List[Pelicula]:
        try:
            mycursor = self._conn.cursor(buffered=True)
            mycursor.execute("SELECT * FROM PELICULA WHERE ANYO = %s", (any,))
            peliculas = []
            for x in mycursor:
                pelicula = Pelicula(x[1], x[2], x[3], x[4], id=x[0])  # Crear la película con los datos de la base de datos
                peliculas.append(pelicula)
            return peliculas
        except Exception as e:
            # Manejar cualquier excepción que pueda ocurrir
            print(f"Error al leer las películas del año {any}: {e}")
    
    def canvia(self, pelicula: Pelicula) -> Pelicula:
        try:
            mycursor = self._conn.cursor(buffered=True)
            mycursor.execute("UPDATE PELICULA SET VOTOS = %s WHERE id = %s", (pelicula.vots, pelicula.id))
            self._conn.commit()
            print("Número de votos actualizado correctamente")
            return pelicula
        except Exception as e:
            # Manejar cualquier excepción que pueda ocurrir
            print(f"Error al actualizar el número de votos de la película: {e}")
            self._conn.rollback()  # Revertir cualquier cambio en caso de error
            

    
