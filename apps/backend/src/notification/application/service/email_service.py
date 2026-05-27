import logging
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Optional

from fastapi import BackgroundTasks
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from src.shared.infrastructure.config import Settings

logger = logging.getLogger(__name__)

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


class EmailService:
    """
    Servicio de envío de emails vía SMTP con templates Jinja2.

    Usa FastAPI BackgroundTasks para envío asincrónico.
    En desarrollo (SMTP_HOST=localhost:1025), funciona con Mailpit.
    En producción, configurar vía env vars con cualquier proveedor SMTP.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self._template_env: Optional[Environment] = None

    @property
    def template_env(self) -> Environment:
        if self._template_env is None:
            self._template_env = Environment(
                loader=FileSystemLoader(str(_TEMPLATES_DIR)),
                autoescape=True,
            )
        return self._template_env

    def is_configured(self) -> bool:
        """
        Verifica si el servicio de email está configurado para enviar.

        Consideramos que está configurado si SMTP_HOST no es 'localhost'
        O si se proporcionaron credenciales SMTP.
        """
        host = self.settings.SMTP_HOST
        user = self.settings.SMTP_USER
        return host.lower() not in ("localhost", "127.0.0.1", "") or bool(user)

    def send_email_async(
        self,
        background_tasks: BackgroundTasks,
        to_email: str,
        subject: str,
        template_name: str,
        context: dict,
    ) -> None:
        """
        Encola el envío de un email via BackgroundTasks.

        Args:
            background_tasks: FastAPI BackgroundTasks para ejecución async.
            to_email: Destinatario del email.
            subject: Asunto del email.
            template_name: Nombre del template Jinja2 (ej: 'email/course_enrollment.html').
            context: Diccionario de variables para el template.
        """
        background_tasks.add_task(
            self._send_email_task,
            to_email=to_email,
            subject=subject,
            template_name=template_name,
            context=context,
        )

    async def _send_email_task(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        context: dict,
    ) -> None:
        """
        Tarea asincrónica que renderiza el template y envía el email.

        NOTA: Esta función se ejecuta en un BackgroundTask (no es async real
        porque smtplib es síncrono). FastAPI BackgroundTasks ejecuta en un
        threadpool separado, por lo que no bloquea el event loop principal.
        """
        try:
            html_content = self._render_template(template_name, context)
            self._send_email(to_email, subject, html_content)
            logger.info(
                "Email sent successfully to %s | subject: %s",
                to_email,
                subject,
            )
        except Exception as e:
            logger.warning(
                "Failed to send email to %s | subject: %s | error: %s",
                to_email,
                subject,
                str(e),
                exc_info=True,
            )

    def _render_template(self, template_name: str, context: dict) -> str:
        """
        Renderiza un template Jinja2 a HTML string.

        Args:
            template_name: Ruta relativa al template (ej: 'email/course_enrollment.html').
            context: Variables para el template.

        Returns:
            HTML string renderizado.

        Raises:
            TemplateNotFound: Si el template no existe.
        """
        try:
            template = self.template_env.get_template(template_name)
            return template.render(**context)
        except TemplateNotFound:
            logger.error("Email template not found: %s", template_name)
            raise

    def _send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
    ) -> None:
        """
        Envía el email via SMTP.

        Si SMTP no está configurado, loguea un warning y no intenta el envío.
        Conexión TLS opcional vía SMTP_USE_TLS.
        """
        settings = self.settings

        # Check if SMTP is minimally configured
        if not settings.SMTP_HOST:
            logger.warning(
                "SMTP_HOST not configured. Email not sent to %s | subject: %s",
                to_email,
                subject,
            )
            return

        # Build email message
        msg = EmailMessage()
        msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(
            f"Este correo requiere HTML. Por favor usa un cliente que soporte HTML.\n\n"
            f"---\nAsunto original: {subject}",
        )
        msg.add_alternative(html_content, subtype="html")

        # Send via SMTP
        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
                if settings.SMTP_USE_TLS:
                    server.starttls()

                if settings.SMTP_USER and settings.SMTP_PASS:
                    server.login(settings.SMTP_USER, settings.SMTP_PASS)

                server.send_message(msg)
        except smtplib.SMTPException as e:
            logger.warning(
                "SMTP error sending to %s: %s",
                to_email,
                str(e),
            )
            raise
        except OSError as e:
            logger.warning(
                "Connection error sending to %s: %s",
                to_email,
                str(e),
            )
            raise
