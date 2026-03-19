# Diseño Técnico: Corrección de la Funcionalidad de Registro

## Decisiones de Arquitectura

### 1. Mantener el Comportamiento del Backend
- No se requieren cambios en el backend ya que funciona correctamente según las pruebas de duplicados
- El backend ya previene usuarios duplicados mediante el caso de uso `RegisterUserUseCase`
- Se mantiene la integración existente con el cliente API de TypeScript (`@workspace/api-client-ts`)

### 2. Enfoque de State Management Local
- Implementar estado local de React para controlar la visibilidad de los campos de contraseña
- Mantener la compatibilidad con `useActionState` para el manejo de acciones del servidor
- Preservar los valores válidos del formulario usando estado controlado de los campos

### 3. Componentización
- Modificar el componente existente `SignupForm` en lugar de crear nuevos componentes
- Implementar el toggle de contraseña como lógica interna del campo de entrada
- Evitar la creación de componentes reutilizables innecesarios para mantener la simplicidad

## Cambios en la Estructura de Componentes

### Archivo Modificado
- `apps/frontend/src/components/auth/signup-form.tsx`

### Nuevos Estados Locales
```typescript
const [showPassword, setShowPassword] = useState(false);
const [showConfirmPassword, setShowConfirmPassword] = useState(false);
```

### Modificaciones al Componente Input
Reemplazar los `Input` estándar con componentes que incluyan:
- Icono de toggle (ojo abierto/cerrado) al lado derecho del campo
- Manejo de clic para alternar visibilidad
- Cambio dinámico entre `type="password"` y `type="text"`

## Enfoque de State Management

### Estado Actual vs. Estado Propuesto
**Actual:** Solo estado del servidor vía `useActionState`
**Propuesto:** Combinación de:
1. Estado del servidor (`useActionState`) para envío y validación
2. Estado local de React para visibilidad de contraseñas
3. Estado controlado de los campos para preservar valores válidos

### Flujo de Estado
1. Usuario ingresa datos en los campos
2. Los valores se mantienen en estado controlado de los inputs
3. Al hacer toggle en el ojo, solo cambia el estado de visibilidad local
4. Al enviar formulario, se envían los valores actuales del estado controlado
5. Si hay errores, solo los campos con errores se marcan como inválidos, pero se preservan sus valores
6. Los campos válidos mantienen sus valores y no se marcan como inválidos

## Detalles de UI/UX para Password Toggle

### Iconografía
- Usar iconos de ojo de `lucide-react` (ya disponible en shadcn/ui)
- Ojo cerrado cuando la contraseña está oculta (`type="password"`)
- Ojo abierto cuando la contraseña es visible (`type="text"`)

### Implementación Visual
```tsx
<div className="relative">
  <Input 
    id="password"
    name="password"
    type={showPassword ? "text" : "password"}
    // ... otros props
  />
  <button
    type="button"
    className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-primary"
    onClick={() => setShowPassword(!showPassword)}
    aria-label="Mostrar contraseña"
  >
    {showPassword ? (
      <EyeOff className="h-4 w-4" />
    ) : (
      <Eye className="h-4 w-4" />
    )}
  </button>
</div>
```

### Consideraciones de Accesibilidad
- `aria-label` descriptivo en el botón de toggle
- Enfoque visible adecuado en el botón
- Contraste suficiente para el icono

## Detalles de Implementación para Validación a Nivel de Campo

### Preservación de Valores Válidos
- Mantener los valores de los campos incluso cuando el envío falla
- Solo marcar como inválido los campos que realmente tienen errores
- No limpiar ni resetear campos válidos cuando hay errores en otros campos

### Mostrado de Errores
- Mostrar errores específicos debajo de cada campo en lugar de consolidados
- Mantener el estilo existente de mensajes de error (`text-destructive text-xs mt-1`)
- Preservar el comportamiento de `aria-invalid` para cada campo

### Lógica de Validación
1. Al enviar el formulario, `signupAction` realiza validación Zod
2. Si hay errores, devuelve `fieldErrors` con errores específicos por campo
3. El componente muestra errores solo para los campos que los tienen
4. Los valores de todos los campos se preservan en el estado controlado
5. Al corregir un campo con error, solo ese campo se vuelve a validar en el próximo envío

## Flujo de Datos e Interacciones con API

### Flujo de Envío
1. Usuario completa formulario y hace clic en "Crear Cuenta"
2. Se ejecuta `signupAction` (Server Action) vía `useActionState`
3. `signupAction` valida datos con `signupSchema` (Zod)
4. Si validación pasa:
   - Llama a `authRegister` del servicio de autenticación
   - En caso de éxito, redirige a `/login`
   - En caso de error (usuario/email duplicado), devuelve error en `_form`
5. Si validación falla:
   - Devuelve `fieldErrors` con errores específicos por campo
   - El componente muestra errores debajo de cada campo problemático
   - Los valores de todos los campos se preservan

### Interacción con Servicios Existentes
- No se modifican los servicios de autenticación existentes (`@/services/auth`)
- Se mantiene la misma llamada a `authRegister` con los mismos parámetros
- Se conserva el manejo de errores existente para duplicados

## Consideraciones para Mantener Funcionalidad Existente

### Compatibilidad con Validación Zod
- No se modifican los esquemas de validación existentes en `actions.ts`
- Se mantiene la misma estructura de respuesta de `ActionState`
- Se preserva el manejo de errores de formulario (`_form`)

### Compatibilidad con Acciones del Servidor
- Se mantiene el uso de `useActionState` con `signupAction`
- No se cambia la firma ni el comportamiento de `signupAction`
- Se preserva el manejo de estados de carga y redirección

### Preservación de Estilos y Componentes
- Se mantiene el uso de componentes shadcn/ui existentes (`Field`, `Input`, `Button`)
- Se conservan las clases Tailwind existentes mediante `cn()`
- Se mantiene la estructura visual y espaciado del formulario

### Compatibilidad con Toast y Notificaciones
- Se mantiene el uso de `sonner` para toast de éxito/error
- Se preserva el `useEffect` que muestra notificaciones basado en el estado

## Riesgos Identificados y Mitigaciones

### Riesgo 1: Pérdida de Valores Válidos
- **Mitigar:** Usar estado controlado de los inputs para preservar todos los valores
- **Verificar:** Probar envío con errores parciales y confirmar que los campos válidos mantienen sus valores

### Riesgo 2: Inconsistencia en Estado de Visibilidad
- **Mitigar:** Inicializar estados de visibilidad en `false` (contraseña oculta)
- **Verificar:** Probar toggle múltiples veces y confirmar comportamiento correcto

### Riesgo 3: Conflictos con Estilos Existentes
- **Mitigar:** Usar las mismas clases y estructuras de shadcn/ui
- **Verificar:** Revisar visualmente que el toggle se integre bien con el diseño existente

### Riesgo 4: Problemas de Accesibilidad
- **Mitigar:** Añadir `aria-label` apropiado y asegurar enfoque visible
- **Verificar:** Probar con lector de pantalla y navegación por teclado