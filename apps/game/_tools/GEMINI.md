# Contexto del Proyecto

El proyecto de manera general consiste en un videojuego educativo para el aprendizaje de programación, utilizando una novela visual junto a puzzles interactivos. Este videojuego tiene una particularidad y es que puede adaptar sus niveles acorde al rendimiento del estudiante, mediante un agente inteligente que se encarga de realizar los cambios a nivel de BD. Además de que da un feedback automático al estudiante y registrar todo su progreso en una tabla en la BD.

Este videojuego forma parte de un proyecto mucho más grande, con una integración a un backend en el cúal lo único que hace es sincronizar la información de los datos de la bd local a la bd online. Esta información después se ve en una plataforma web docente. Pero esto sería otro proyecto aparte, que se integra en conjunto a este. Al videojuego lo llamó módulo Estudiante y a la interfaz web docente lo llamó módulo profesor.

## Niveles

### Nivel 1 - Cafeteria

### Nivel 2 - Biblioteca



# Arquitectura del Proyecto
La arquitectura general del videojuego consiste en un MVC adaptado a Godot, compuesto de las siguientes capas:

- En la carpeta scripts, seria la capa Controller, donde se ubica los script relacionado con la lógica del videojuego. Por ejemplo los game controllers o los repositorios.
- En la carpeta scenes, seria la capa View, aqui es donde se ubica cada una de las escenas del videojuegos, componentes de la UI, etc
- En la carpeta models, sería la capa Models, aquí es donde se ubican las clases que se mapean en la bd local, y las representaciones de los estados en el juego.

Esas son las carpetas principales representando el proyecto, pero además tiene otras carpetas más:

- La carpeta data, es para almacenar el fichero de la base de datos.
- La carpeta assets, es para guardar las imagenes, los sprites, sonido, etc del videojuego.
- La carpeta config, guarda las configuraciones del videojuego
- La carpeta addons, son los plugins que le instalo a Godot.
- La carpeta dialogue, guarda los dialogos de un addons
- La carpeta test, es para ubicar los distintos tipos de test del proyecto.


# Reglas

- Las respuestas serán en inglés
- El código proporcionado siempre estará en inglés y estará ubicado en su sección correcta del proyecto
