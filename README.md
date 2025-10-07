# UniMove

UniMove es una plataforma web para estudiantes nacionales e internacionales que se trasladan a **Madrid**, facilitando su **mudanza**, búsqueda de **vivienda** y acceso a **servicios de salud**, todo en un solo lugar.

![UniMove Logo](/frontend/assets/images/prototipo-readme.png)

---

## 📌 Descripción General

UniMove simplifica la reubicación estudiantil conectando a los usuarios con:  
- **Universidades**  
- **Empresas de mudanza**  
- **Apartamentos y residencias**  
- **Servicios médicos y seguros**

*Problemas que resuelve:*  
- Dudas sobre transporte (tren, autobús, avión)  
- Límites de equipaje y envío de pertenencias  
- Coordinación de viaje y logística  

---

## 🎯 Objetivos

- Facilitar acceso a **universidades, viviendas y mudanzas** en Madrid  
- Comparar opciones para **decisiones informadas**  
- Acceso rápido a **servicios de salud** y seguros  
- Experiencia personalizada para necesidades **académicas, logísticas y médicas**  
- Plataforma escalable para otras ciudades  

---

## 📝 Funcionalidades Principales

### Usuario y Perfil
- Registro / inicio de sesión (**email + contraseña**)  
- Perfil básico: *nombre, nacionalidad, grado de interés, foto*  
- Seguimiento del proceso de nacionalidad y aprendizaje de español  

### Universidades
- Buscar grados y universidades en Madrid  
- Información detallada: *ranking, contacto, ubicación*  
- Sugerencias de grados similares  

### Vivienda
- Explorar apartamentos por **precio y ubicación**  
- Detalles: *fotos, disponibilidad*  
- Conectar con otros estudiantes  
- Publicación de pisos por particulares  

### Mudanzas y Transporte
- Conexión con empresas de mudanza  
- Comparativa de precios y servicios  
- Integración con transporte público  
- Pagos integrados: *Stripe, PayPal, Bizum*  

### Salud y Bienestar
- Perfil biomédico: *alergias, medicamentos, grupo sanguíneo*  
- Conexión con clínicas y seguros médicos  
- Chatbot de salud con IA  
- Alertas sanitarias en tiempo real  
- Botón SOS médico y protocolos preconfigurados  

---

## ⚡ Funcionalidades Avanzadas

- Calculadora inteligente de mudanza (bultos, peso, transporte)  
- Tracking de envío y notificaciones en tiempo real  
- Marketplace de segunda mano (muebles, libros)  
- Comunidad de estudiantes para tips logísticos  

---

## 💻 Consideraciones Técnicas

- Plataforma web **responsive**  
- Mapas: *Google Maps API / OpenStreetMap*  
- Datos: APIs de universidades, vivienda y mudanza  
- Escalable a otras ciudades  

---

## ✅ Criterios de Éxito (MVP)

- Registro e inicio de sesión funcional  
- Búsqueda y comparación de viviendas, universidades y mudanzas  
- Reducción del tiempo de logística para estudiantes  
- Integración efectiva de servicios académicos, residenciales y médicos

---

## 📘 Requisitos y Criterios de Validación

### R1: Registro con email + contraseña
**Criterio de Validación:**
1. Entrar en la pantalla donde se meten los datos de registro (email + contraseña).  
2. Permitir que un usuario mete sus datos (email + contraseña).  
3. Cuando el usuario mete los datos adecuados el sistema dice **“Account created”**.  
4. Cuando el usuario mete los datos no adecuados y/o que no conforman con un formato dado el sistema dice **“Error”**.  

---

### R2: Inicio de sesión con email + contraseña
**Criterio de Validación:**
1. Entrar en la pantalla donde se meten los datos de inicio de sesión (email + contraseña).  
2. Permitir que un usuario mete sus datos (email + contraseña).  
3. Cuando el usuario mete los datos adecuados el sistema dice **“Welcome”**.  
4. Cuando el usuario mete los datos no adecuados el sistema dice **“Error”**.  

---

### R3: Creación de perfil básico (nombre, nacionalidad, grado de interés, foto de perfil)
**Criterio de Validación:**
1. Entrar a la pantalla de datos personales.
2. Permitir al usuario ingresar sus datos.  
3. Hacer ciertos datos obligatorios (**Nombre, Nacionalidad y grado de interés**).
4. Cuando el usuario mete los datos adecuados el sistema dice **"Profile updated"**.
5. Cuando el usuario mete los datos no adecuados y/o no mete los datos obligatorios el sistema dice **"Error updating profile"**.

---

### R4: Orientación y seguimiento del proceso de solicitud de nacionalidad española
**Criterio de Validación:**
1. Entrar en la pantalla de estudiantes internacionales.  
2. Permitir al usuario introducir el país de donde procede.  
3. En base a su respuesta, mostrarle el proceso que debe realizar.  

---

### R5: Módulo de apoyo al aprendizaje del idioma español
**Criterio de Validación:**
1. Entrar en la pantalla de idiomas.  
2. Permitir al usuario seleccionar su lengua materna.  
3. Permitir al usuario ingresar su nivel de español del **1 al 10**.  

---

### R6: Recomendador de material y equipo académico según la carrera elegida
**Criterio de Validación:**
1. Entrar a la pantalla donde se muestran los materiales.  
2. Permitir al usuario seleccionar su carrera.  
3. Una vez seleccionado, mostrarle los materiales adecuados para su carrera.  
4. Comprobar que haya stock de los materiales, sino hay, lanza **Error**.  
5. Proceder al Check out.  

---

### R7: Conectar a los usuarios con universidades en Madrid
**Criterio de Validación:**
1. Permite al usuario ingresar el grado/grados de interés.  
2. Entra a una pantalla donde se muestran todas las universidades donde esté disponible el grado seleccionado.  
3. Permite al usuario enviar cartas de interés.  
4. Permite hablar con la universidad en el caso de tener dudas sobre su programa.  
5. Si no existe ninguna universidad que imparta el grado seleccionado, lanza un error.  

---

### R8: Permitir buscar un grado y ver todas las universidades que lo ofrecen
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestran diferentes universidades con sus respectivos grados.  
2. Permitir al usuario insertar el grado deseado.  
3. Si el grado no existe, lanzar un **Error**.  
4. En base al grado, mostrarle las mejores universidades para dicho grado.  

---

### R9: Mostrar la ubicación de cada universidad en Madrid en un mapa
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestra un mapa.  
2. En el mapa se verán iconos que determinen la ubicación de la universidad además del nombre de esta.  
3. Permitir que el usuario seleccione un icono.  
4. Si selecciona un icono, se añade en la pantalla la información específica de la universidad.  

---

### R10: Alertas meteorológicas geolocalizadas para estudiantes en Madrid
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestra el tiempo.  
2. Preguntar al usuario por su ubicación.  
3. Si el usuario no comparte su localización, lanzará un error.  
4. En base a la ubicación del usuario, mostrar al usuario posibles alertas meteorológicas.  

---

### R11: Mostrar información detallada de cada universidad (ranking, datos clave, contacto)
**Criterio de Validación:**
1. Entra en una pantalla donde se muestra la información de cada universidad ordenadas por ranking (incluyendo fotos del campus) de forma resumida y fácil de leer.  
2. Permite al usuario filtrarlas ingresando el grado/grados de interés.  
3. Si no existe ninguna universidad que imparta el grado seleccionado, lanza un error.  

---

### R12: Sugerir grados similares cuando un usuario realice una búsqueda
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestran los grados.  
2. Permitir al usuario seleccionar el grado que desea.  
3. Si el grado no existe, lanzar un error.  
4. Una vez el usuario haya seleccionado el grado, mostrarle grados similares.  

---

### R13: Mostrar apartamentos disponibles dentro de un rango de precios accesible para estudiantes
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestran apartamentos con sus precios.  
2. Permitir al usuario ingresar aproximadamente un presupuesto.  
3. Permitir que el usuario ingrese la zona donde desea vivir.  
4. Si no hay apartamentos disponibles según sus requisitos, lanzar un error.  

---

### R14: Mostrar información detallada de cada apartamento (precio, fotos, ubicación, disponibilidad)
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestra información sobre apartamentos.  
2. Permitir al usuario ingresar el apartamento deseado.  
3. Mostrar al usuario el precio y fotos de dicho apartamento.  
4. Permitir al usuario contactar con el dueño/agencia de dicho apartamento, para conocer su disponibilidad.  

---

### R15: Mostrar otros estudiantes interesados en apartamentos similares (conexión social / confianza)
**Criterio de Validación:**
1. Entra en una pantalla donde se muestran todos los demás estudiantes interesados en estos apartamentos.  
2. Permite al usuario ver la información básica de los estudiantes (edad, nacionalidad, grado que estudian, etc).  
3. Permite al usuario chatear con los otros estudiantes interesados.  
4. Si no hay ningún otro estudiante interesado en los apartamentos seleccionados, lanza un error.  

---

### R16: Proporcionar opciones de transporte público entre apartamentos y universidades seleccionadas
**Criterio de Validación:**
1. Entra en una pantalla que muestra los tiempos de origen a destino desde cada apartamento a las universidades seleccionadas.  
2. Permitir al usuario ingresar la universidad a la que atiende, y donde vive.  
3. En base a su respuesta, mostrarle las mejores rutas teniendo en cuenta cuánto tarda cada transporte y cada cuanto recoge pasajeros.  
4. Si no existen medios de transporte que unan ambas ubicaciones, lanza un error.  

---

### R17: Permitir que propietarios o particulares publiquen apartamentos (función básica de “alquilar vivienda”)
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestran los apartamentos ofrecidos para estudiantes.  
2. Permitir que un usuario añada un apartamento especificando información sobre el alquiler: precio, fotos, metros cuadrados,...  
3. Publicar la oferta de ese apartamento en la web.  

---

### R18: Conectar a los usuarios con empresas de mudanzas en Madrid
**Criterio de Validación:**
1. Entra a una pantalla donde se muestran las distintas empresas de mudanzas.  
2. Permite al usuario ingresar la cantidad de bultos a transportar.  
3. Recomienda la opción más cómoda y económica.  

---

### R19: Comparar precios y servicios entre proveedores
**Criterio de Validación:**
1. Entrar en la pantalla donde te muestran diferentes tipos de proveedores.  
2. Permitir al usuario ingresar un presupuesto.  
3. Permitir al usuario filtrar lo que se muestra según el precio, mejores valoraciones…  

---

### R20: Mapa que muestre universidades, apartamentos y empresas de mudanza
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestra un mapa.  
2. El usuario podrá elegir si quiere ver en el mapa las universidades, apartamentos y/o empresas de mudanza.  
3. Una vez seleccionada la opción (u opciones si se seleccionan más de una), se añaden en el mapa.  
4. Si el usuario selecciona uno en el mapa, se añade en la pantalla la información específica de la universidad, apartamento o empresa de mudanza.  

---

### R21: Integración con rutas de transporte público (ej. Metro, bus, tren)
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestra un mapa.  
2. El usuario podrá elegir si quiere ver en el mapa las rutas de metro, bus y/o tren.  
3. Una vez seleccionada la opción (u opciones si se seleccionan más de una), se añaden en el mapa.  
4. Si el usuario selecciona uno en el mapa, se añade en la pantalla la información específica de la ruta de metro, bus o tren.  

---

### R22: Mostrar ofertas de empleo y/o becas en universidades
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestran las ofertas de empleo y becas en universidades en Madrid.  
2. Permite al usuario filtrar por barrio, universidad o sueldo.  
3. Cuando el usuario pulsa sobre una oferta de empleo o beca el sistema abre una nueva pestaña y redirige al usuario a la página web de la oferta.  

---

### R23: Sugerir restaurantes, librerías, cafés y lugares afines a estudiantes en Madrid
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestran las sugerencias de sitios en Madrid.  
2. Permite al usuario filtrar por restaurantes, librerías, cafés, y negocios.  
3. Cuando el usuario pone el ratón sobre una imagen de un sitio el sistema muestra la dirección y horario.  
4. Cuando el usuario mueve el ratón de la imagen de un sitio el sistema deja de mostrar la dirección y horario.  

---

### R24: Posibilidad de pagar a empresas de mudanza o propietarios directamente a través de la plataforma (Stripe, PayPal, Bizum)
**Criterio de Validación:**
1. Entrar en la pantalla donde se meten los datos financieros.  
2. Permitir que un usuario mete sus datos.  
3. Cuando el usuario mete los datos adecuados el sistema procesa el pago en la nube y dice **“Processing”**.  
4. Cuando el usuario mete los datos no adecuados el sistema dice **“Error with payment information”**.  
5. Cuando el pago se ha procesado correctamente el sistema dice **“Payment completed”**.  
6. Cuando el pago no se ha procesado correctamente el sistema dice **“Payment incomplete: Error”**.  

---

### R25: Proporcionar opciones de seguros médicos en caso de que lo requieran
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestran los seguros médicos más comunes en Madrid.  
2. Cuando el usuario pulsa el texto de un seguro médico el sistema abre una nueva pestaña y redirige al usuario a la página web del seguro médico.  

---

### R26: Crear un perfil biomédico mínimo del estudiante
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestra el perfil biomédico mínimo del estudiante, vacío.  
2. Permitir al usuario introducir toda o parte de sus datos biomédicos en su perfil biomédico: peso, altura, alergias, enfermedades, teléfonos de contacto.  
3. Cuando el usuario mete los datos adecuados el sistema dice **“Biomedical profile created”**.  
4. Cuando el usuario mete los datos no adecuados y/o que no conforman con un formato dado el sistema dice **“Error”**.  

---

### R27: Recibir notificaciones de brotes, alertas alimentarias, olas de calor, contaminación alta, polen en el perfil biomédico
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestra el perfil biomédico del estudiante.  
2. El sistema muestra las notificaciones de brotes, alertas alimentarias, olas de calor, contaminación alta y polen.  

---

### R28: Conectar con clínicas universitarias o centros de salud cercanos a las universidades
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestran las clínicas o centros de salud.  
2. Cuando el usuario pone el ratón sobre una imagen de una clínica o centro de salud el sistema muestra el nombre y dirección de la clínica o centro de salud.  
3. Cuando el usuario mueve el ratón de la imagen de una clínica o centro de salud el sistema deja de mostrar el nombre y dirección de la clínica o centro de salud.  

---

### R29: Uso de un chatbot biomédico (IA con fuentes validadas) que responda dudas sobre salud al llegar a Madrid
**Criterio de Validación:**
1. Entrar en la pantalla donde se comunica con el chatbot.  
2. Permitir que un usuario meta texto.  
3. Cuando el usuario meta texto el chatbot muestra la respuesta.  

---

### R30: Botón de pánico / SOS médico
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestra el perfil biomédica.  
2. Cuando el usuario pulsa el botón de pánica / SOS médico el sistema pide confirmación.  
3. Cuando el usuario confirma el sistema manda su ubicación a un contacto de emergencia.  
4. Cuando el usuario no confirma el sistema cierra el panel.  

---

### R31: Protocolos preconfigurados
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestra la enfermedad/condición del estudiante.  
2. Mostrar lista de pasos (protocolo) para saber cómo actuar.  

---

### R32: Descuentos en gimnasios o supermercados a través de la plataforma
**Criterio de Validación:**
1. Entrar en la pantalla donde se muestran las ofertas en gimnasios o supermercados.  
2. Mostrar lista de ofertas detalladas incluyendo porcentaje de descuento, precio antes y después de aplicar ese descuento, condiciones,...  
3. Permitir que el usuario pueda filtrar las ofertas.  
4. En caso de filtrar, mostrar la lista acorde a los filtros.  

---

### R33: Recordatorios para los estudiantes del mismo piso
**Criterio de Validación:**
1. Entrar en el perfil biomédico.  
2. Cuando el usuario pulsa **“notificar”**, el sistema pide un mensaje y números de teléfono.  
3. Cuando el usuario confirma, el sistema manda el mensaje.  
4. Cuando el usuario no confirma, el sistema cierra el panel.  