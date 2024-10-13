# Crash Cam
## What is CrashCam?
As the name suggests, it's a camera that records your crashes. Through using live streaming services and AI, we are able to provide you with all the details for court after you get into an accident.

## How we built it
**Front End:** StreamLit <br>
**Data Input:** Arduino Vibration Module + Camera Module <br>
**Crash Recognition:** Fetch.ai's agentverse and uagents <br>
**Data Storage:** MongoDB 

## How we optimized our project
Instead of using actual live 30 fps 4k video recording, we broke it down into 64 hexabit images to make the data easy to transport. On top of that, we utilized direct connections through arduino powershell programming for the least amount of ping when receiving data.

## What's next for CrashCam?
We're looking to have the CrashCam more integrated to an actual dashcam that way we can put it into the commercial market and we would integrate it with more specialized hardware such as PCBs instead of using arduino kits.

