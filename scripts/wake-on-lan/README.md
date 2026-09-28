# Wake-on-LAN example

Set `WOL_MAC_ADDRESS`, `WOL_BROADCAST`, and optionally `WOL_PORT` in a local environment. `.env` is ignored by Git; this script reads exported environment variables and does not parse a dotenv file. The MAC and broadcast defaults are documentation examples only. Run from a network that can deliver a Layer 2 broadcast to the target. A successful send does not confirm the host booted.

```bash
export WOL_MAC_ADDRESS='AA:BB:CC:DD:EE:FF'
export WOL_BROADCAST='192.0.2.255'
python3 scripts/wake-on-lan/wol.py
```
