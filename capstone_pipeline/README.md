# Capstone pipeline

The shared team pipeline that every module's project contributes to. It does not exist yet. This file records the intended shape so module projects can be written to fit it.

## Intended stages

1. **Collect**: read sensor streams (Level 2)
2. **Log**: write synchronized, timestamped sessions with metadata (Level 2)
3. **Clean**: handle dropouts, duplicates, and bad samples (Levels 0 and 2)
4. **Process**: filter and extract features (Level 3a)
5. **Visualize**: live monitoring and offline review (Level 3b)
6. **Model**: train and evaluate on the logged data (Level 4)
7. **Deploy**: run a trained model on device with safety checks (Level 5)

## Open decisions

- Session file format (CSV, Parquet, HDF5, or something else)
- How sessions and subjects are named and versioned
- Which sensors are first-class once hardware is chosen
- Whether any real-time middleware is needed

Decide these as a team before writing the Level 2 module, since the later modules depend on them.
