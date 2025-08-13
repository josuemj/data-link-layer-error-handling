# Error Detection and Correction Lab

Repositorio del laboratorio sobre detección y corrección de errores en la capa de enlace de datos.



## Cómo correr el emisor

```bash
cd emisor_ts
npm install
npm start
```

### Uso del emisor

1. El programa te pedirá ingresar una cadena binaria (solo 0s y 1s)
2. Luego podrás seleccionar el algoritmo de detección/corrección de errores:
   - Opción 1: Hamming
   - Opción 2: TODO (por implementar)
3. El resultado se procesará según el algoritmo seleccionado
4. Se escribe el mensaje del emisor en tests/mensaje.txt


# USO DE APLICACIONES

### Instalar dependiencias en emisor
```bash
cd emisor_ts
npm install
npx ts-node src/app.ts
```