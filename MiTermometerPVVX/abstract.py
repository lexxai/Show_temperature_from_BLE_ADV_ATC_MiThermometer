from abc import ABC, abstractmethod
import logging

from discord_api import send_message as discors_send_message

# from plyer import notification

logger = logging.getLogger(f"BLEScanner.{__name__}")


class NotificationAbstract(ABC):

    is_async = False

    async def send_alert_async(self, title: str = None, message: str = None) -> None:
        """Sends async an alert message."""
        ...

    @abstractmethod
    def send_alert(self, title: str = None, message: str = None) -> None:
        """Sends an alert message."""
        ...


class PrintAbstract(ABC):
    @abstractmethod
    def print_value(self, text: str, pos: dict = None) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

    def clear_lines(self, lines: int = 1): ...


class LoggerNotification(NotificationAbstract):
    @staticmethod
    def send_alert(title: str = None, message: str = None) -> None:
        """Sends an alert message."""
        logger.info("*** START LOGGER NOTIFICATION ***")
        if title:
            logger.info(f"Title: {title}")
        if message:
            logger.info(f"Message: {message}")
        logger.info("*** END LOGGER NOTIFICATION ***")


class PrintNotification(NotificationAbstract):
    def send_alert(self, title: str = None, message: str = None) -> None:
        """Sends an alert message."""
        print("\n*** START PRINT NOTIFICATION ***")
        if title:
            print(f"Title: {title}")
        if message:
            print(f"Message: {message}")
        print("*** END PRINT NOTIFICATION ***\n")


class DicordNotification(NotificationAbstract):
    is_async = True
    async def send_alert_async(self, title: str = None, message: str = None) -> None:
        """Sends an alert message."""
        discord_message = f"{title}\n{message}"
        await discors_send_message(discord_message)

    def send_alert(self, title: str = None, message: str = None) -> None:
        logger.error("DicordNotification is not available in sync.")


class SystemNotification(NotificationAbstract):
    def send_alert(self, title: str = None, message: str = None) -> None:
        """Sends an alert message."""
        logger.info("*** START SYETEM NOTIFICATION ***")
        if title:
            logger.info(f"Title: {title}")
        if message:
            logger.info(f"Message: {message}")
        logger.info("*** END SYSTEM NOTIFICATION ***")
        # Using plyer for cross-platform notifications
        # notification.notify(
        #     title=alert_title,
        #     message=alert_message,
        #     timeout=10,  # Notification will disappear after 10 seconds
        # )


class ConsolePrint(PrintAbstract):
    def print_value(self, text: str, pos: dict = None) -> None:
        if pos is not None:
            print_text = f'\033[{str(pos["y"])};{str(pos["x"])}H{text}'
        else:
            print_text = text

        print(print_text)

    def clear(self):
        print("\033c\033[3J")

    def clear_lines(self, lines: int = 1):
        for _ in range(lines):
            print("\033[K")
