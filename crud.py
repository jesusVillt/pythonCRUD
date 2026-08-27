# librerias necesarios para el funcionamineto del programa:
import os
import oracledb

# Esta es la libreria que nos permite guardar las variables de entorno
from dotenv import load_dotenv

# Lee el archivo .env y carga las variables en nuestra memoria
load_dotenv()

# si algo sale mal, lo informamos
try:
    connection = oracledb.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), dsn=os.getenv("DB_DSN"))
    print("Se logro la conexion")
except Exception as error:
    print("algo salio mal :( :")
    print(error)
  

# Funcion crear registro
# con ayuda de el objeto curso podemos lograr insertar registros dentro de la tabla
def crear_registro():
    # 10 caracteres nomas, si ponemos mas nos va a dar error
    # por como esta definida la base de datos
    job_id = input("ingrese id_job: ") 
    job_title = input("titulo del job: ")
    min_salary = input("salario minimo: ")
    max_salary = input("salario maximo: ")

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO jobs (job_id, job_title, min_salary, max_salary)
            VALUES (:1, :2, :3, :4)
            """,
            [job_id, job_title, min_salary, max_salary]
        )
        connection.commit()
        print()
        print("Se inserto correctamente")
        print()
        cursor.close()
        # esto es importante, por ejemplo por si repetimos id
        # por aqui nos vamos a dar cuenta
    except Exception as error:
        print(error)
        cursor.close() # cerramos siempre siempre de todas formas


# Funcion para borrar registro
def borrar_registro():
    job_id = input("ingrese el id del job a eliminar: ")
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM jobs WHERE job_id = :1", [job_id])
        # si la ejecución no afecto a ningun registro
        # eso quiere decir que este no existe, de lo contrario si, y
        # por se borrara correctamente
        if cursor.rowcount == 0: 
            print("No existe un registro con ese id")
        else:
            connection.commit()
            print()
            print("Se borro el registro") 
            print()
            cursor.close()

    except Exception as error:
        print(error)
        cursor.close()


# Funcion actualizar registro
# esta funcion permite actualizar uno o todos los atributos
# de un registro (con excepcion del id)
def actualizar_registro():
    job_id = input("ingrese el id del registro a actualizar: ")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM jobs WHERE job_id = :1", [job_id])        

        # si no lo encontramos el registro dado, no tiene caso seguir con 
        # la ejecucion de esta funcion, de ahi el return
        if cursor.fetchone() is None:
            print("No existe un job con ese ID.\n")
            return 

        nuevo_title = ""
        nuevo_min = ""
        nuevo_max = ""

        cambiar_titulo = "n"
        cambiar_min = "n" 
        cambiar_mac = "n"

        ## preguntamos primero uno por uno
        ## para ver cuales quiere cambiar
        cambiar_titulo = input("Quieres cambiar el TITULO de este registro y/n:")
        if(cambiar_titulo == "y"):
                nuevo_title = input("Ingrese el nuevo titulo: ")
        print("ok")

        cambiar_min = input("Quieres cambiar el Min salario de este registro y/n:")
        if(cambiar_min == "y"):
             nuevo_min = input("Ingrese el nuevo Min salario: ")
        print("ok")


        cambiar_mac = input("Quieres cambiar el Max salario de este registro y/n:")
        if(cambiar_mac == "y"):
             nuevo_max = input("Ingrese el nuevo Max salario: ")
        print("ok")

        # si se quedaron vacios es porque nunca lo eligio cambiar
        # entonces esto no se ejecutaria
        if nuevo_title:
            cursor.execute("UPDATE jobs SET job_title = :1 WHERE job_id = :2", [nuevo_title, job_id])
        if nuevo_min:
            cursor.execute("UPDATE jobs SET min_salary = :1 WHERE job_id = :2", [nuevo_min, job_id])
        if nuevo_max:
            cursor.execute("UPDATE jobs SET max_salary = :1 WHERE job_id = :2", [nuevo_max, job_id])

        connection.commit()
        print()
        print("Se actualizo el registro")
        print()
        cursor.close()

    except Exception as error:
        print(error)


# Funcion mostrar_jobs
# esta funcion recupera todos los registros con todos sus atributos
# de la tabla jobs
def mostrar_jobs():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM jobs")
        mis_filas = cursor.fetchall()
        print()
        print("######################## Tablita Jobs #########################")
        print(f"JOB_ID  JOB_TITLE MIN_SALARY  MAX_SALARY")
        if(len(mis_filas) == 0):
            print("No tenemos nada todavia")
        else:
            for fila in mis_filas:
                print(f"{fila[0]}     {fila[1]}     {fila[2]}     {fila[3]}")
        print("###############################################################")
        print()

        cursor.close()

    except Exception as error:
        print(error)
        cursor.close()


# Funcion que da incio al flujo de nuestro programa
# Despliga el menu 
def menu():
    while True:
        print("(1) insertar trabajo")
        print("(2) Mostrar trabajos")
        print("(3) actualizar trabajo")
        print("(4) borrar trabajo")
        print("(5) salir")

        opcion = input("Que quieres hacer: ")


        match (opcion):
            case "1":
                crear_registro()
            case  "2":
                mostrar_jobs()
            case "3":
                actualizar_registro()
            case "4":
                borrar_registro()
            case "5":
                print("muy bien, adios ")
                connection.close()
                break


# incia el programa
menu()