<!-- --- file: docs/gpio-map.md -->

# WanOS GPIO map (current production — WISC)

**Board:** WISC v5 rev **2.5.3** (main I/O carrier).  
**Software SoT:** [wanos](https://github.com/gitwannes/wanos) root [`config_hardware.yaml`](https://github.com/gitwannes/wanos/blob/main/config_hardware.yaml).  
**This file:** canonical **BCM inventory** (claimed / free / 1-wire notes) for production WanOS on WISC — lived in the wanos repo; home is now **wanos-pcb**.  
**wanos-pcb-v1 (new carrier):** [`gpio-interface.md`](gpio-interface.md) — do not treat this map as the v1 pinout.

BCM numbers below are **Raspberry Pi BCM** (same as `config_hardware.yaml` `pin:` / relay keys).  
Header pin = physical 40-pin header position.

WanOS has **no** 1-wire / DS18B20 driver today. Free-pin notes are for **hardware wiring + dtoverlay** only.

---

## All BCM GPIOs — current usage

```
BCM  Header  Status    Usage                          Notes
---  ------  --------  -----------------------------  ------------------------------------------
  0     27   reserved  -                              do not use (ID_SD HAT EEPROM)
  1     28   reserved  -                              do not use (ID_SC HAT EEPROM)
  2      3   free      -                              unused by WanOS; I2C SDA; header only
  3      5   free      -                              unused by WanOS; I2C SCL; header only
  4      7   used      safety_gpio                    master safety contactor
  5     29   used      water_hot                      idx 11003
  6     31   used      water_cold                     idx 11002
  7     26   used      sht11 sauna_low pin_c          idx 20002
  8     24   used      sht11 sauna_low pin_d          idx 20002
  9     21   used      sht11 cinema pin_d             idx 20003
 10     19   used      sht11 cinema pin_c             idx 20003
 11     23   used      sht11 sauna_high pin_d         idx 20001
 12     32   used      kwh_meter                      idx 11001
 13     33   free      -                              candidate 1wire; header pin 33 only (no JST)
 14      8   used      ir_relais                      -
 15     10   used      sauna_relais_phase_U           3500 W
 16     36   free      -                              candidate 1wire; J3 e-ink D0+ (if J3 free)
 17     11   used      sauna_relais_phase_V           3500 W
 18     12   used      sauna_relais_phase_W           2000 W
 19     35   free      -                              candidate 1wire; header pin 35 only (no JST)
 20     38   free      -                              candidate 1wire; J3 e-ink CEC (if J3 free)
 21     40   free      -                              candidate 1wire; J3 e-ink D1+ (if J3 free)
 22     15   used      door_bathroom1                 idx 10002
 23     16   used      sht11 bathroom1 pin_c          idx 20004
 24     18   used      sht11 bathroom1 pin_d          idx 20004
 25     22   used      sht11 sauna_high pin_c         idx 20001
 26     37   free      -                              candidate 1wire; J3 e-ink SDA (if J3 free)
 27     13   used      door_sauna                     idx 10001
```

---

## Free GPIOs (summary)

```
BCM  Access on WISC 2.5.3              Notes
---  --------------------------------  ------------------------------------------
  2  Pi header pin 3                   unused by WanOS; I2C SDA — keep free if I2C planned
  3  Pi header pin 5                   unused by WanOS; I2C SCL — keep free if I2C planned
 13  Pi header pin 33 only             candidate 1wire; no field connector
 16  J3 e-ink D0+ (or header pin 36)   candidate 1wire; prefer if e-ink cable unused
 19  Pi header pin 35 only             candidate 1wire; no field connector
 20  J3 e-ink CEC (or header pin 38)   candidate 1wire; prefer if e-ink cable unused
 21  J3 e-ink D1+ (or header pin 40)   candidate 1wire; prefer if e-ink cable unused
 26  J3 e-ink SDA (or header pin 37)   candidate 1wire; prefer if e-ink cable unused
```

**Not free:** BCM **4** (safety). Linux default `w1-gpio` uses GPIO **4** — **do not** use the default overlay on this Pi.

---

## 1-wire (DS18B20 etc.)

| Item | Guidance |
|---|---|
| **Default overlay pin** | BCM **4** — **blocked** (safety_gpio) |
| **Recommended** | Pick one free pin above; set overlay explicitly, e.g. `dtoverlay=w1-gpio,gpiopin=16` |
| **Easiest field access** | BCM **16 / 20 / 21 / 26** via **J3** when e-ink is disconnected |
| **Header-only** | BCM **13** or **19** (solder / tap Pi header) |
| **I2C pins** | BCM **2 / 3** work electrically but conflict with any future I2C on this bus — avoid unless intentional |
| **WanOS software** | No 1-wire reader / entity path yet — kernel/`w1` only until a ship adds it |

---

## Related

- Runtime pins: [wanos `config_hardware.yaml`](https://github.com/gitwannes/wanos/blob/main/config_hardware.yaml)
- wanos-pcb-v1 board map: [`gpio-interface.md`](gpio-interface.md)
- WISC KiCad (read-only): [`reference/wisc-board/`](reference/wisc-board/)
- Sauna / IR (software): [wanos `docs/sauna-ir.md`](https://github.com/gitwannes/wanos/blob/main/docs/sauna-ir.md)
