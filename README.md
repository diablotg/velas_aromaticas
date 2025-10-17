# Tienda en linea con enfoque a expansion

Aplicación de ventas en línea, con enfoque en experiencia de usuario simple, segura y orientada a la conversión. Permite agregar productos al carrito, elegir envío o recolección, y pagar con tarjeta.

---

## Características

- Venta de cualquier producto con carrito de compras.
- Checkout en dos columnas:
  - **Columna izquierda:** correo del comprador, dirección de entrega o recolección.
  - **Columna derecha:** pago con tarjeta (Stripe) en una sola exhibición.
- Validaciones en tiempo real con warnings y resaltado de campos faltantes.
- Integración con **PostgreSQL**.
- Autenticación opcional con **Google** o correo electrónico.
- Preparado para ampliar con descuentos, envíos y otros métodos de pago.

---

## Requisitos

- Python 3.13
- Django 5.1.1
- PostgreSQL
- pip
- Dependencias en `requirements.txt`:
  - stripe==10.5.0
  - python-dotenv==1.0.1
  - django-crispy-forms==2.3
  - crispy-bootstrap5==0.7
  - django-allauth==64.0.0
  - django-cors-headers==4.5.0
  - requests==2.32.3
  - psycopg2-binary==2.9.9

---

## Configuración del entorno

1. Crear y activar entorno virtual:

```bash
python -m venv venv
```
