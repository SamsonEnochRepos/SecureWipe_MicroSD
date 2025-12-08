import os
import json
from datetime import datetime

from recovery.scanner import RecoveryScanner
from wiping.wipe import wipe_image_file
from certificates.generator import generate_wipe_certificate
from utils.hashing import hash_file


def prompt_path(prompt_text: str) -> str:
    path = input(prompt_text).strip('"').strip()
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    return path


def option_scan_and_recover():
    print("\n=== Scan & Recover from Image ===")
    image_path = prompt_path("Enter path to disk image file (e.g. sd_dump.img): ")

    output_dir = input("Enter output directory for recovered files [default: recovered_output]: ").strip()
    if not output_dir:
        output_dir = "recovered_output"

    os.makedirs(output_dir, exist_ok=True)

    scanner = RecoveryScanner()
    summary = scanner.scan_image(image_path, output_dir)

    summary_path = os.path.join(output_dir, "recovery_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    print(f"\nRecovery complete.")
    print(f"Recovered items summary saved to: {summary_path}")
    print("Details:")
    for k, v in summary.items():
        print(f"  {k}: {v}")


def option_secure_wipe():
    print("\n=== Secure Wipe Image + Certificate ===")
    image_path = prompt_path("Enter path to disk image file to wipe (WARNING: this will destroy data): ")

    confirm = input(f"Type 'WIPE' to confirm wiping {image_path}: ").strip()
    if confirm != "WIPE":
        print("Wipe cancelled.")
        return

    print("\nComputing hash BEFORE wipe...")
    hash_before = hash_file(image_path)

    passes_input = input("Number of overwrite passes [default: 1]: ").strip()
    passes = int(passes_input) if passes_input else 1

    print(f"\nStarting wipe ({passes} pass(es))...")
    wipe_image_file(image_path, passes=passes)

    print("Computing hash AFTER wipe...")
    hash_after = hash_file(image_path)

    device_info = {
        "device_type": "disk_image",
        "path": os.path.abspath(image_path),
        "size_bytes": os.path.getsize(image_path),
    }

    timestamp = datetime.utcnow().isoformat() + "Z"
    method = f"{passes}-pass overwrite"

    cert_dir = "certificates_output"
    os.makedirs(cert_dir, exist_ok=True)

    cert_paths = generate_wipe_certificate(
        device_info=device_info,
        timestamp=timestamp,
        method=method,
        hash_before=hash_before,
        hash_after=hash_after,
        output_dir=cert_dir,
    )

    print("\nWipe complete.")
    print("Certificate generated:")
    for name, path in cert_paths.items():
        print(f"  {name}: {path}")


def main():
    while True:
        print("\n==============================")
        print(" SecureWipe microSD Prototype ")
        print("==============================")
        print("1. Scan & Recover from Image")
        print("2. Secure Wipe Image + Generate Certificate")
        print("3. Exit")
        choice = input("Select an option [1-3]: ").strip()

        try:
            if choice == "1":
                option_scan_and_recover()
            elif choice == "2":
                option_secure_wipe()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid option, please choose 1-3.")
        except Exception as e:
            print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    main()