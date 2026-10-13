from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
import time
import random

# ====== APNI DETAILS YAHAN DAALO ======
API_ID = 36743746                    # my.telegram.org se lo
API_HASH = "209195fc67b4aa2c94a692bab4d51a0b"     # my.telegram.org se lo
STRING_SESSION = "BQIwqkIAPjE7ngzBXBAssVPmQXxiWLn5el8SVuRZPFawn_soWwe72cxX1n_bvSsEv3U46ib1cDSraXzTyGPPRaX2TB96jDC7_j9HFxq6eMOKGbbIKlhqqjQ58PAFOfuCVRYnoDMxEMtwYltwjis7FczBYhCFDYRlwA3a32o5Fveb1Rqv_yqB-uzJYv6h33-QCWjbJdCFAC9MtDxG0DLkepPQWsSgdjmk0qiU54DEmCbilaeuSWaAdWuLstkQxISt3duoBdJhTKN4j-ogfkqkVR48g__TZykWKqUt6OFkeKSf4Xw7nBuricqB_OSYao53hw38h6c-05E7cViiqGMOSr4_3Ldj8wAAAAG7P6rjAA"  # pyrogram string session
BOT_USERNAME = "@yt_test_zhidi_bot" # target bot
MESSAGE = "/yt"
BATCH_SIZE = 100                    # har batch me kitni requests
DELAY_MIN = 1                       # min delay (seconds)
DELAY_MAX = 3                       # max delay (seconds)
WAIT_BETWEEN_BATCHES = 30           # batch ke baad wait
TOTAL_BATCHES = 0                   # kitne batches (0 = infinite)
# =======================================

app = Client(
    name="session_yt",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    in_memory=True,
)


async def main():
    await app.start()
    me = await app.get_me()
    print(f"✅ Login successful! Logged in as: {me.first_name} (@{me.username})")

    # Bot ko resolve karo
    try:
        bot = await app.get_users(BOT_USERNAME)
        print(f"🎯 Target bot: @{bot.username}")
    except Exception as e:
        print(f"❌ Bot resolve nahi hua: {e}")
        await app.stop()
        return

    batch_count = 0
    try:
        while True:
            batch_count += 1
            print(f"\n🚀 Batch #{batch_count} start — {BATCH_SIZE} requests bhej raha hun...")

            for i in range(BATCH_SIZE):
                try:
                    await app.send_message(bot.id, MESSAGE)
                    delay = random.uniform(DELAY_MIN, DELAY_MAX)
                    print(f"  [{i+1}/{BATCH_SIZE}] sent | next in {delay:.2f}s")
                    await asyncio.sleep(delay)
                except FloodWait as fw:
                    print(f"  ⏳ FloodWait: {fw.value}s wait kar raha hun...")
                    await asyncio.sleep(fw.value + 1)
                except Exception as e:
                    print(f"  ⚠️ Error: {e}")
                    await asyncio.sleep(2)

            print(f"✅ Batch #{batch_count} complete. {WAIT_BETWEEN_BATCHES}s wait...")

            if TOTAL_BATCHES != 0 and batch_count >= TOTAL_BATCHES:
                print("🏁 All batches done.")
                break

            await asyncio.sleep(WAIT_BETWEEN_BATCHES)

    except KeyboardInterrupt:
        print("\n⛔ Manually stopped.")
    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())