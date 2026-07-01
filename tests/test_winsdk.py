import asyncio
from winsdk.windows.ui.notifications.management import UserNotificationListener
from winsdk.windows.ui.notifications import NotificationKinds

async def main():
    listener = UserNotificationListener.current
    await listener.request_access_async()
    notis = await listener.get_notifications_async(NotificationKinds.TOAST)
    if notis:
        noti = notis[0]
        print(dir(noti))
    else:
        print("No notis")

asyncio.run(main())
