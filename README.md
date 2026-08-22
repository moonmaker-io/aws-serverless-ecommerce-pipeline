# AWS Serverless E-Commerce Processing Architecture

Arquitectura serverless desacoplada, resiliente y de alta disponibilidad diseñada en AWS para la ingesta, validación, orquestación y persistencia de transacciones de comercio electrónico.

---

  ##  Arquitectura del Sistema
```
                [ Cliente / App ]
                        │
                        ▼
                [ Amazon Cognito ]  ──▶  [ AWS WAF + API Gateway ]
                        │
                        ▼
                [ AWS Step Functions ]
                        ├──▶ Validar Orden (AWS Lambda)
                        ├──▶ Procesar Pago (AWS Lambda) ──[ Fallo ]──▶ [ Amazon SQS (DLQ) ]
                        └──▶ Guardar & Notificar (AWS Lambda)
                        │
        ┌───────────────┴────────────────┐
        ▼                                ▼
[ Amazon DynamoDB ]                [ Amazon SNS ]
(Persistencia NoSQL)           (Notificaciones de Estado)
```

### Flujo de Componentes:
* **Autenticación y Seguridad Perimetral:**
  * **Amazon Cognito:** Control de acceso y validación de tokens JWT para clientes autorizados.
  * **AWS WAF:** Reglas de inspección perimetral asociadas a **Amazon API Gateway** (Rate Limiting, protección contra inyecciones SQL y XSS).
* **Orquestación y Lógica Serverless:**
  * **AWS Step Functions:** Máquina de estados que coordina el flujo transaccional con manejo de errores declarativo y retroceso exponencial (`BackoffRate`).
  * **AWS Lambda:** Funciones de backend dedicadas ejecutadas dentro de subredes privadas en **AWS VPC** para aislamiento y seguridad.
* **Persistencia y Resiliencia:**
  * **Amazon DynamoDB:** Base de datos NoSQL con clave de partición optimizada para almacenamiento de órdenes con latencia de un solo dígito de milisegundo.
  * **Amazon SQS (Dead-Letter Queue):** Enrutamiento de transacciones fallidas para desacoplar componentes y evitar pérdida de datos ante caídas de pasarelas externas.
* **CI/CD y Observabilidad:**
  * **AWS CodePipeline & S3:** Canalización automatizada de integración y despliegue continuo.
  * **Amazon SNS & CloudWatch:** Monitoreo y trazabilidad de logs en tiempo real, alarmas operativas y alertas de eventos.

---

##  Tecnologías y Servicios

* **Cómputo & Orquestación:** AWS Lambda, AWS Step Functions (Amazon States Language).
* **Bases de Datos & Almacenamiento:** Amazon DynamoDB, Amazon S3.
* **Seguridad & Redes:** AWS WAF, Amazon Cognito, Amazon VPC.
* **Integración & Mensajería:** Amazon SQS, Amazon SNS, Amazon API Gateway.
* **DevOps & Monitoreo:** AWS CodePipeline, Amazon CloudWatch.
* **Lenguaje de Desarrollo:** Python 3.11 (`boto3`).

---

##  Estructura del Repositorio

* `step-functions/`: Definición de la máquina de estados en Amazon States Language (ASL) con bloques `Retry` y `Catch`.
* `src/handlers/`: Lógica de funciones Lambda de procesamiento y persistencia con `boto3`.

---

> *Nota: Este proyecto fue desarrollado y validado en un entorno sandbox de laboratorio práctico bajo las mejores prácticas del AWS Well-Architected Framework.*
