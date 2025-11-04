# **Ejercicio**: Implementa GitHub Flow completo con convenciones profesionales
Ejercicio práctico para aplicar los conceptos aprendidos.

## Crear feature branch descriptiva:
```sh
git checkout -b feature/dashboard-ventas-v1
# Hacer cambios con commits descriptivos:
```
#Modificar código
```sh
echo "import matplotlib.pyplot as plt" >> analisis_ventas.py
```
# Commit con convención
```sh
git add analisis_ventas.py
git commit -m "feat: Agregar visualización básica de ventas"
```
- Importar matplotlib para gráficos
- Preparar estructura para dashboard de ventas
- Configurar colores corporativos por defecto"
## Push y crear Pull Request:
```sh
git push -u origin feature/dashboard-ventas-v1
```
## En GitHub:

### Crear PR desde la branch
- Título: "feat: Dashboard básico de análisis de ventas"
- Descripción detallada del cambio y su impacto
- Solicitar revisión a compañeros
- Simular revisión y merge:

### Agregar comentarios en el PR
- Hacer cambios solicitados
- Aprobar y mergear el PR
- Eliminar la branch después del merge
- Verificación: Confirma que el flujo completo funciona y que el historial refleja un proceso profesional de colaboración.

### equerimientos:
- Git y GitHub configurados completamente (de días anteriores)
- Repositorio con historial de trabajo
- Conocimiento básico de branches y merges (del día 4)