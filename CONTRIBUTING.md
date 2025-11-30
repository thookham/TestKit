# Contributing to TestKit

Thank you for your interest in contributing to TestKit! We aim to build a robust database of hardware profiles to help developers everywhere.

## How to Contribute

### Adding a New Profile
1.  **Check for Duplicates**: Ensure the profile doesn't already exist in the `profiles/` directory.
2.  **Create a JSON File**: Create a new JSON file in the appropriate OS subdirectory (e.g., `profiles/win10/`).
3.  **Follow the Schema**: Ensure your JSON matches the defined schema.
    *   **ID**: Use a kebab-case slug: `make-model-variant-os`.
    *   **Metadata**: Accurate make, model, year, and target OS.
    *   **Hardware**: Precise specs for that specific configuration.
4.  **Submit a Pull Request**: Push your changes and open a PR.

### Reporting Issues
If you find an inaccurate profile or a bug in the generator scripts, please open an issue on GitHub.

## Code of Conduct
Please be respectful and constructive in all interactions.
