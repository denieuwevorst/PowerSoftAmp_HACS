# Powersoft Duecanali for Home Assistant

Custom integration to control a Powersoft Duecanali DSP+ amplifier (developed for the Duecanali 1604) from Home Assistant, over the local network.

> **Unofficial.** This project is not affiliated with or endorsed by Powersoft. It uses the same JSON-over-HTTP endpoint (`POST /am`) that the amplifier's built-in web interface uses.

> **Status: early / experimental (v0.1.0).** The standby write is verified against a real amplifier. The read-back parsing and the preset-slot sensor are based on the write response format and have not been confirmed yet. Please open an issue with the amp's READ response if something looks wrong.

## Features

- **Power switch**: on = awake, off = standby (`/Device/Audio/Presets/Live/Generals/Standby/Value`)
- **Preset slot sensor**: current snapshot slot (`/Device/Audio/Presets/Live/ReadOnly/SnapshotSlotId/Current`)
- The IP address is entered in the UI when you add the integration
- Local polling every 10 seconds, no cloud

## Installation

### HACS (custom repository)

1. In HACS, open the three-dot menu and choose **Custom repositories**.
2. Add `https://github.com/denieuwevorst/duecanali-ha` with category **Integration**.
3. Download **Powersoft Duecanali** and restart Home Assistant.

### Manual

1. Copy the `custom_components/duecanali` folder into the `custom_components` folder of your Home Assistant configuration directory (the folder containing `configuration.yaml`).
2. Restart Home Assistant.

## Setup

1. Go to **Settings → Devices & services → Add integration**.
2. Search for **Powersoft Duecanali**.
3. Enter the IP address of the amplifier.

## Security

The amplifier's `/am` endpoint has no authentication. Anyone who can reach the amp on the network can change its settings, so keep it on a trusted network or VLAN.

## How it works

Requests are JSON documents posted to `http://<amp-ip>/am`, for example:

```json
{"clientId":"x8-panel","payload":{"type":"ACTION","action":{"type":"WRITE","values":[{"id":"/Device/Audio/Presets/Live/Generals/Standby/Value","data":{"type":"BOOL","boolValue":false}}]}}}
```

The amplifier replies directly in the HTTP response. Open the amp's web interface with your browser's developer tools (Network tab) to discover other parameter ids.

## Roadmap

- Volume / attenuation, mute and preset recall entities
- Confirm read response format and adjust parsing

## License

MIT, see [LICENSE](LICENSE).
