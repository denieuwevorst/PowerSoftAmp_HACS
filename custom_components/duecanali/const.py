"""Constants for the Powersoft Duecanali integration."""

DOMAIN = "duecanali"

# The amp's web UI uses this id; it is the one verified to work.
CLIENT_ID = "x8-panel"

PATH_STANDBY = "/Device/Audio/Presets/Live/Generals/Standby/Value"
PATH_SLOT = "/Device/Audio/Presets/Live/ReadOnly/SnapshotSlotId/Current"

SCAN_INTERVAL_SECONDS = 10
