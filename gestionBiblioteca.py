

class Usuario:
    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contraseña = contraseña
        self.admin = False
        self.contraseñaADMON = ['DASDF1231224', '2131231FERF', 'VDCGV12341F']  # Lista de contraseñas de administrador

    def getTipoUser(self):
        return self.admin

    def getNombre(self):
        return self.nombre
    
    def getContraseña(self):
        return self.contraseña
    
    def convertirseEnAdmin(self, contraseñaDeAdmin):
        if contraseñaDeAdmin in self.contraseñaADMON:
            self.admin = True
            return f"Ahora eres administrador!!!!."
        else:
            return "Contraseña incorrecta. No tienes permisos para convertirte en administrador."

class Libro:
    def __init__(self, idLibro, titulo, autor, disponible=True):
        self.idLibro = idLibro
        self.titulo = titulo
        self.autor = autor
        self.disponible = disponible

    def getTitulo(self):
        return self.titulo
    
    def getAutor(self):
        return self.autor
    
    def getDisponible(self):
        return self.disponible

    def getIdLibro(self):
        return self.idLibro
    
    def setDisponible(self, estado):
        self.disponible = estado

class SistemaBiblioteca:
    def __init__(self):
        self.usuarios = {}
        self.libros = []
        self.usuarioActual = None

    def registrarUsuario(self, nombre, contraseña):
        if nombre in self.usuarios:
            return "El usuario ya está registrado."
        self.usuarios[nombre] = Usuario(nombre, contraseña)
        return "Usuario registrado exitosamente."

    def iniciarSesion(self, nombre, contraseña):
        if nombre in self.usuarios and self.usuarios[nombre].getContraseña() == contraseña:
            self.usuarioActual = self.usuarios[nombre]
            return f"Inicio de sesión exitoso. Bienvenido, {self.usuarioActual.getNombre()}."
        return "Nombre de usuario o contraseña incorrectos."

    def cerrarSesion(self):
        if self.usuarioActual:
            print(f"Sesión cerrada para {self.usuarioActual.getNombre()}.")
            self.usuarioActual = None
        else:
            print("No hay ninguna sesión activa.")

    def verificarAutenticacion(self):
        if self.usuarioActual is None:
            print("Debe iniciar sesión para realizar esta acción.")
            return False
        return True

    def verificarAdmin(self):
        if not self.usuarioActual or not self.usuarioActual.getTipoUser():
            print("Debe ser administrador para realizar esta acción.")
            return False
        return True

    def convertirEnAdmin(self, contraseñaDeAdmin):
        if self.usuarioActual and self.usuarioActual.convertirseEnAdmin(contraseñaDeAdmin):
            return "Se han otorgado privilegios de administrador."
        else:
            return "Contraseña incorrecta o usuario no autorizado."

    def agregarLibro(self, idLibro, titulo, autor, disponible=True):
        if not self.verificarAdmin():
            return
        self.libros.append(Libro(idLibro, titulo, autor, disponible))
        print(f"Libro '{titulo}' agregado exitosamente.")

    def eliminarLibro(self, idLibro):
        if not self.verificarAdmin():
            return
        for libro in self.libros:
            if libro.getIdLibro() == idLibro:
                self.libros.remove(libro)
                print(f"Libro '{libro.getTitulo()}' eliminado exitosamente.")
                return
        print("No se encontró el libro con el ID proporcionado.")

    def buscarLibros(self, criterio):
        return [libro for libro in self.libros if criterio.lower() in libro.getTitulo().lower()]

    def reservarLibro(self, idLibro):
        if not self.verificarAutenticacion():
            return
        for libro in self.libros:
            if libro.getIdLibro() == idLibro:
                if libro.getDisponible():
                    libro.setDisponible(False)
                    return f"Reserva exitosa: {libro.getTitulo()}."
                else:
                    return "El libro no está disponible. Agregado a la lista de espera."
        return "Libro no encontrado."

    def devolverLibro(self, idLibro):
        if not self.verificarAutenticacion():
            return
        for libro in self.libros:
            if libro.getIdLibro() == idLibro:
                if not libro.getDisponible():
                    libro.setDisponible(True)
                    return f"El libro '{libro.getTitulo()}' ha sido devuelto exitosamente."
                else:
                    return "El libro no necesita ser devuelto porque ya está disponible."
        return "No se encontró el libro con el ID proporcionado."

    def menu(self):
        print("Bienvenido al Sistema de Gestión de Bibliotecas en Línea")
        while True:
            if self.usuarioActual is None:
                print("\n1. Registrar Usuario")
                print("2. Iniciar Sesión")
                print("3. Buscar Libro")
                print("4. Reservar Libro")
                print("5. Convertirse en Admin")
                print("6. Cerrar Sesión")
                print("7. Salir")
                print("12. Ver Libros")
            else:
                print("\n3. Buscar Libro")
                print("4. Reservar Libro")
                print("10. Devolver Libro")
                print("5. Convertirse en Admin")
                if self.usuarioActual.getTipoUser():
                    print("8. Agregar Libro")
                    print("9. Eliminar Libro")
                print("6. Cerrar Sesión")
                print("7. Salir")
                print("12. Ver Libros")

            opcion = input("Seleccione una opción: ")

            if opcion == "1" and self.usuarioActual is None:
                nombre = input("Ingrese su nombre de usuario: ")
                contraseña = input("Ingrese su contraseña: ")
                print(self.registrarUsuario(nombre, contraseña))
            elif opcion == "2" and self.usuarioActual is None:
                nombre = input("Ingrese su nombre de usuario: ")
                contraseña = input("Ingrese su contraseña: ")
                print(self.iniciarSesion(nombre, contraseña))
            elif opcion == "3":
                if not self.verificarAutenticacion():
                    continue
                criterio = input("Ingrese el título del libro que busca: ")
                resultados = self.buscarLibros(criterio)
                if resultados:
                    for libro in resultados:
                        estado = "Disponible" if libro.getDisponible() else "No disponible"
                        print(f"{libro.getIdLibro()}. {libro.getTitulo()} - {libro.getAutor()} ({estado})")
                else:
                    print("No se encontraron libros.")
            elif opcion == "4":
                if not self.verificarAutenticacion():
                    continue
                try:
                    idLibro = int(input("Ingrese el ID del libro que desea reservar: "))
                    print(self.reservarLibro(idLibro))
                except ValueError:
                    print("Debe ingresar un ID válido.")
            elif opcion == "5":
                if not self.verificarAutenticacion():
                    continue
                token = input("Ingrese el token de administrador: ")
                print(self.convertirEnAdmin(token))
            elif opcion == "10":
                if not self.verificarAutenticacion():
                    continue
                try:
                    idLibro = int(input("Ingrese el ID del libro que desea devolver: "))
                    print(self.devolverLibro(idLibro))
                except ValueError:
                    print("Debe ingresar un ID válido.")
            elif opcion == "6":
                self.cerrarSesion()

            elif opcion == "12":
                if self.libros:
                    print("Lista de libros disponibles:")
                    for libro in self.libros:
                        estado = "Disponible" if libro.getDisponible() else "No disponible"
                        print(f"{libro.getIdLibro()}. {libro.getTitulo()} - {libro.getAutor()} ({estado})")
                else:
                    print("No hay libros registrados en el sistema.")

            elif opcion == "7":
                print("Gracias por usar el sistema. ¡Hasta pronto!")
                break
            elif opcion == "8" and self.usuarioActual and self.usuarioActual.getTipoUser():
                idLibro = int(input("Ingrese el ID del libro: "))
                titulo = input("Ingrese el título del libro: ")
                autor = input("Ingrese el autor del libro: ")
                self.agregarLibro(idLibro, titulo, autor)
            elif opcion == "9" and self.usuarioActual and self.usuarioActual.getTipoUser():
                idLibro = int(input("Ingrese el ID del libro que desea eliminar: "))
                self.eliminarLibro(idLibro)
            else:
                print("Opción no válida o acceso denegado.")


biblioteca = SistemaBiblioteca()
biblioteca.menu()
