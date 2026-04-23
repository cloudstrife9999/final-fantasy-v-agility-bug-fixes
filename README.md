# Final Fantasy V Agility Bug Fix

Python scripts to patch the agility bug in *Final Fantasy V* across three versions: SNES, Game Boy Advance (US release), and Pixel Remaster (PC).

The bug causes the agility stat to have almost no effect on the damage multiplier of several weapon classes (boomerangs, bows, knives, short swords, and whips). A detailed write-up of the bug and its technical root cause in each version is available on the [FFV wiki](https://finalfantasy.fandom.com/wiki/Final_Fantasy_V_agility_bug).

## Requirements

Python 3.9 or later. No third-party dependencies.

## Scripts

All scripts are located in the `scripts` directory. Each script is independent and can be used to patch the corresponding version of the game.

### `snes.py` -- SNES version

Patches 4 bytes at ROM addresses `0x28113-0x28116`. Applies to both the original Japanese release and the RPGe fan translation.

The original file is not modified. A separate patched copy is written to the output path.

**Usage:**

``` bash
python snes.py -i <input> -o <output>
```

| Argument | Description |
|----------|-------------|
| `input`  | Path to the original SNES ROM |
| `output` | Path to write the patched ROM |

**Example:**

``` bash
python snes.py -i "Final Fantasy V.sfc" -o "Final Fantasy V (patched).sfc"
```

---

### `us_gba.py` -- Game Boy Advance version (US)

Patches 10 bytes at ROM addresses `0x0E4536-0x0E453F`.

The original file is not modified. A separate patched copy is written to the output path.

**Usage:**

``` bash
python us_gba.py -i <input> -o <output>
```

| Argument | Description |
|----------|-------------|
| `input`  | Path to the original *Advance* ROM |
| `output` | Path to write the patched ROM |

**Example:**

``` bash
python us_gba.py -i "Final Fantasy V Advance (USA).gba" -o "Final Fantasy V Advance (USA) (patched).gba"
```

---

### `pr.py` -- Pixel Remaster version (PC)

Patches 16 bytes at file offsets `0xAC105F-0xAC106E` in `GameAssembly.dll`.

Unlike the ROM scripts, this script modifies the file in place, since the game executable does not allow choosing which DLL to load. Before writing the patch, the original file is renamed to `GameAssembly_original.dll` as a backup. If the write fails, the script automatically attempts to restore the original. If the backup file already exists, the script aborts without making any changes.

**Usage:**

``` bash
python pr.py -i <input>
```

| Argument | Description |
|----------|-------------|
| `input`  | Path to `GameAssembly.dll` in the game's installation directory |

**Example:**

``` bash
python pr.py -i "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY V\GameAssembly.dll"
```

> **Note:** On Windows, you may need to run the script as administrator depending on where the game is installed.

## Verifying the patch

In all three versions, the patch can be verified in-game by comparing the damage of the `Assassin's Dagger` against the `Enhancer` on an enemy with low defense. Before patching, the `Enhancer` should deal more damage. After patching, the `Assassin's Dagger` should deal noticeably more damage due to the corrected agility contribution.

Please note that at the beginning of the game, when `Level × Agility < 128` due to low level and agility, the agility contribution to the damage multiplier is 0 with or without the bug. Therefore, the difference will only be visible once the character's level and agility are high enough.

### Benchmark

It is possibe to run `benchmark.py` to print the possible (bugged and non bugged) damage rolls in this scenario:
* Character: Bartz.
* Job: Thief.
* Level: 7.
* Job level: irrelevant.
* Strength: 29.
* Agility: 41.
* Enemy physical defence: 0.
* Weapon: Dagger (Atk: 14, random bonuses: [0, 1, 2, 3]).
* Other equipment: irrelevant, as long as it does not provide any Strength/Agility bonuses.
* Possible damage rolls: [70, 75, 80, 85].
* Possible bugged damage rolls: [42, 45, 48, 51].

``` bash
python benchmark.py
```

## Safety

All scripts validate the bytes at the target addresses before applying any changes. If the bytes do not match the expected values (for example, if the ROM or DLL has already been patched, or is a different revision), the script prints an error and exits without modifying anything.

It is recommended to make a backup of the relevant files before running any patch script (except for the Pixel Remaster script, which automatically creates a backup of the DLL).

It is also recommended to use different output paths for the patched files to avoid accidentally overwriting the original files (relevant for the SNES and *Advance* versions).

Finally, it is also recommended to check that any output path does not already exist (whether it is a file, directory, or symlink) before running the script, to avoid accidentally overwriting important files.

## Credits
Credits for the original SNES version fix go to J.L. Tseng (instructrtrepe) who first included a description of the bug/fix in his 2004 [Algorithms/Stats FAQ](https://gamefaqs.gamespot.com/snes/588331-final-fantasy-v/faqs/30040). 
