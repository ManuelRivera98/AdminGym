# AdminGym

AdminGym es un proyecto personal, que permite administrar los clientes y membresias de un gimnasio, CRUD disponible y entre otras funcionalidades.
Basado en arquitectura orientada a servicios, donde el backend y el frontend son independientes y capaces de funcionar por si mismos.
La comunicación e intercambio de datos es API restful.
Proyecto enfocado a intercambio de data entre aplicaciones, no responsive.

backend: Django + django-rest
frontend: React + redux + react-router

## Empezar

* Tener instalado node, docker, docker-compose.

* Ir al archivo local.yml (backend) y ejecutar `export COMPOSE_FILE=local.yml`
* Construir imágenes docker `docker-compose build`
* Arrancar `docker-compose up`
* Ir al archivo package.json (frontend) `yarn add`
* Correr `yarn run dev`
* email: example@gmail.com  ---password: example123456789

## Licencia

MIT

## Autor

Manuel Rivera.
