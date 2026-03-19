# Cambio: Corrección de la Funcionalidad de Registro

## Intent
Mejorar la experiencia de usuario en el formulario de registro mediante:
1. Mantener el correcto comportamiento del backend para prevenir usuarios duplicados
2. Agregar toggle de visibilidad de contraseña con ícono de ojo en los campos de contraseña
3. Implementar validación a nivel de campo que preserve los inputs válidos y muestre errores solo para los campos problemáticos

## Scope
Los siguientes archivos/componentes serán afectados:
- `apps/frontend/src/components/auth/signup-form.tsx` - Formulario de registro principal
- Posiblemente se crearán componentes reutilizables para el toggle de contraseña si se determina necesario

## Approach
1. **Mantener comportamiento del backend**: No se requieren cambios en el backend ya que funciona correctamente según las pruebas de duplicados.

2. **Agregar toggle de visibilidad de contraseña**:
   - Modificar los campos de contraseña y confirmar contraseña para incluir un botón de toggle
   - Implementar estado local para controlar la visibilidad de cada campo de contraseña
   - Usar ícono de ojo (abierto/cerrado) de shadcn/ui o crear uno personalizado
   - Alternar entre `type="password"` y `type="text"` basado en el estado de visibilidad

3. **Implementar validación a nivel de campo**:
   - Modificar el manejo de estado para mantener los valores válidos incluso cuando hay errores en otros campos
   - Actualizar la lógica para mostrar errores específicos debajo de cada campo en lugar de consolidarlos
   - Preservar los valores de los campos que pasaron la validación cuando se envía el formulario con errores
   - Mantener la compatibilidad con la existente `signupAction` y sus esquemas de validación Zod

4. **Referencias a hallazgos de exploración**:
   - El archivo `/apps/frontend/src/components/auth/signup-form.tsx` muestra la implementación actual del formulario
   - El archivo `/apps/frontend/src/lib/actions.ts` contiene la `signupAction` con esquemas de validación Zod que funcionan correctamente
   - Las pruebas en `/apps/backend/tests/auth/test_register_user_usecase.py` confirman que el backend correctamente previene usuarios duplicados

## Próximos pasos recomendados
- Implementar los cambios en el componente de formulario de registro
- Crear pruebas unitarias para verificar el comportamiento del toggle de contraseña
- Verificar que la validación a nivel de campo funcione correctamente
- Asegurar que no se rompa la funcionalidad existente

## Riesgos
- Bajo: Los cambios están limitados al frontend y no afectan la lógica de negocio del backend
- Bajo: Mantendremos la compatibilidad con los esquemas de validación existentes
- Medio: Asegurar que el estado del formulario se maneje correctamente para no perder datos válidos