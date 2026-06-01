# Table on Page 797

**Page:** 797 | **Type:** table

**Table 1 on Page 797**

| DTC Description | Fault Trigger Condition |
| --- | --- |
| (cid:122) C1280 —Yaw Rate Sensor Signal Fault (cid:122) C1282 —Lateral Accelerometer Signal Fault (cid:122) C1516 —Roll Rate Sensor Signal Fault (cid:122) C2770 — Longitudinal Acceleration Sensor Signal Fault | If the ABS module receives a message from the RCM that is out of the normal operating range or one that does not agree with other sensor information, the appropriate signal fault DTC sets. |
| (cid:122) C1963 —Stability Control Inhibit Warning (cid:122) C1975 —IVD Plausibility Failure a | If conditions or DTCs exist that prevent the AdvanceTrac® and RSC® systems from operating, DTCs C1963 and/or C1975 sets. This DTC is usually set due to the steering wheel rotation sensor or the RCM being damaged or installed incorrectly. If DTCs are present from the RCM or PSCM , diagnose these DTCs first. |
| (cid:122) U0151 —Lost Communication with Restraints Control Module (RCM) (cid:122) U0452 —Invalid Data Received from RCM | The RCM uses a dedicated communication bus to send information to the ABS module. If, during normal operation, the ABS module does not receive any information from the RCM for more than 250 milliseconds, DTC U0151 or U0452 sets. U0151 monitors both the HS-CAN and the dedicated CAN circuits. If the ABS module does not receive the RCM serial number, over the HS-CAN , DTC U0151 sets. It also sets if the sensor data is not received over the dedicated CAN from the RCM . These DTCs can also be caused by another module software update. CLEAR all module DTCs and carry out another self-test to recheck the system. |

---