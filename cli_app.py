from __future__ import annotations

from core import store_record


def main() -> None:
    print("Specimen Actual Size Calculator")
    print("Formula: actual size = microscope size / magnification")
    print("-" * 54)

    username = input("Enter username: ").strip()
    microscope_size = float(input("Enter microscope size (e.g. 850): ").strip())
    magnification = float(input("Enter magnification (e.g. 40): ").strip())
    unitPicked = input("Enter unit (default: um): ").strip() or "um"

    record_id, actual_size = store_record(
        username, microscope_size, magnification, unitPicked
    )

    print("\nSaved successfully.")
    print(f"Record ID: {record_id}")
    print(f"Actual size: {actual_size:.6f} {unitPicked}")


if __name__ == "__main__":
    main()
