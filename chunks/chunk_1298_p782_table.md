# Table on Page 782
**Page:** 782 | **Type:** table | **Parent:** Suspension System Manual

**Table 1 - Page 782**

| Test Step | Result / Action to Take |
| --- | --- |
| G1 MONITOR THE ABS MODULE BRAKE ON/OFF (BOO_ABS) PID | Yes GO to G3 . No GO to G2 . |
| (cid:122) Connect the scan tool. (cid:122) Ignition ON. (cid:122) Enter the following diagnostic mode on the scan tool: DataLogger —ABS Module . (cid:122) Press and release the brake pedal while monitoring the BOO_ABS PID. (cid:122) Does the PID display ON with the brake pedal applied and OFF with the brake pedal released? |  |
| G2 MONITOR THE PCM BRAKE ON/OFF (BOO1) PID | Yes REFER to Section 418-00 to continue diagnosis of the HS-CAN . No REFER to Section 417-01 to continue diagnosis of the stoplamp switch fault. |
| (cid:122) Enter the following diagnostic mode on the scan tool: DataLogger —PCM . (cid:122) Press and release the brake pedal while monitoring the BOO1 PID. (cid:122) Does the PID display ON with the brake pedal applied and OFF with the brake pedal released? |  |
| G3 MONITOR THE INITIAL (BRAKE PEDAL NOT APPLIED) BRAKE PRESSURE USING THE ABS MODULE BRAKE PRESSURE (BRAKPRES) PID | Yes GO to G4 . No INSTALL a new HCU . REFER to Hydraulic Control Unit (HCU) in this section. |
| (cid:122) Enter the following diagnostic mode on the scan tool: DataLogger —ABS Module . (cid:122) With the brake pedal not applied, record the pressure displayed by the BRAKPRES PID. (cid:122) Is the initial brake pressure less than 275 kPa (40 psi) with the brake pedal not applied? |  |

---
