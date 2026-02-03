#!/usr/bin/env python3
"""
Bytecode patch for Sone LogoutPage.class

This script patches the isEnabled() method in LogoutPage.class to always
return true (when user is logged in), removing the check that requires
more than 1 local Sone to show the logout option.

Original bytecode at offset 0xbf2:
  9f 00 07  - if_icmpeq +7 (if size == 1, jump to return false)

Patched bytecode:
  57 57 00  - pop, pop, nop (discard size comparison, fall through to return true)

Usage:
  1. Extract LogoutPage.class from sone JAR:
     unzip sone.jar net/pterodactylus/sone/web/pages/LogoutPage.class

  2. Run this patch:
     python3 patch-logout.py net/pterodactylus/sone/web/pages/LogoutPage.class

  3. Update the JAR:
     zip -u sone.jar net/pterodactylus/sone/web/pages/LogoutPage.class

  4. Load patched JAR in Hyphanet
"""

import sys

def patch_logout_class(filepath):
    with open(filepath, 'rb') as f:
        data = bytearray(f.read())

    # Find the pattern: invokeinterface size() followed by iconst_1 and if_icmpeq
    # Pattern: b9 00 54 01 00 04 9f
    pattern = bytes.fromhex('b900540100049f')

    pos = data.find(pattern)
    if pos == -1:
        # Try alternate search - just find the if_icmpeq after size check
        for i in range(len(data) - 10):
            if data[i] == 0xb9:  # invokeinterface
                chunk = data[i:i+12]
                if 0x04 in chunk[4:8] and 0x9f in chunk[5:9]:
                    idx = i + chunk.index(0x9f, 5)
                    print(f"Found if_icmpeq at offset {hex(idx)}")
                    pos = idx - 6  # Adjust to pattern start
                    break

    if pos == -1:
        print("ERROR: Could not find bytecode pattern to patch")
        print("This may not be a compatible LogoutPage.class")
        sys.exit(1)

    # The if_icmpeq is at pos + 6
    patch_offset = pos + 6

    print(f"Found pattern at offset {hex(pos)}")
    print(f"Patching if_icmpeq at offset {hex(patch_offset)}")
    print(f"Before: {data[patch_offset:patch_offset+3].hex()}")

    # Apply patch: change if_icmpeq (9f 00 07) to pop pop nop (57 57 00)
    if data[patch_offset] != 0x9f:
        print(f"WARNING: Expected 0x9f at patch offset, found {hex(data[patch_offset])}")
        resp = input("Continue anyway? (y/n): ")
        if resp.lower() != 'y':
            sys.exit(1)

    data[patch_offset] = 0x57     # pop
    data[patch_offset + 1] = 0x57 # pop
    data[patch_offset + 2] = 0x00 # nop

    print(f"After:  {data[patch_offset:patch_offset+3].hex()}")

    with open(filepath, 'wb') as f:
        f.write(data)

    print(f"\nPatch applied successfully to {filepath}")
    print("The logout option will now always be visible when logged in.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <LogoutPage.class>")
        sys.exit(1)

    patch_logout_class(sys.argv[1])
