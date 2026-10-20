# Sessions and metadata

Training sessions use a directory containing `samples.csv` and `metadata.json`. This simple format is a teaching convention, pending a team decision. Metadata must include nonempty `session_id`, `subject_id`, `task`, `sensor_placement`, and `firmware_version`. Use synthetic identifiers such as `synthetic_01`; do not store names or medical information.

Write only into a new directory. Validate before writing, and clean partial output if writing fails. A manifest should explain units, schema version, and processing history before this format is adopted for team data.

**Try:** open a generated session in a text editor. Could another teammate tell what every channel measures? Describe the extra metadata needed for actual hardware.
