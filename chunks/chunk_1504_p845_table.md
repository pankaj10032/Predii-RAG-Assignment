# Table on Page 845
**Page:** 845 | **Type:** table | **Parent:** Suspension System Manual

**Table 1 - Page 845**

| Test Step | Result / Action to Take |
| --- | --- |
| G1 VERIFY THE SCAN TOOL CAN COMMUNICATE WITH THE PCM | Yes GO to G2 . No REFER to Section 418-00 to diagnose no communication with the PCM. |
| (cid:122) Ignition ON. (cid:122) Allow at least 10 seconds for all modules to wake up and prove out. (cid:122) Verify that a vehicle session can be established with a scan tool. (cid:122) Can a vehicle session be established? |  |
| G2 CHECK THE TBC MODULE CONTINUOUS MEMORY DTCs | Yes GO to G3 . No The system is operating correctly at this time. The DTC may have been set due to high network traffic or an intermittent fault condition. |
| (cid:122) Ignition ON. (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —TBC Module . (cid:122) Clear the DTCs. Repeat the TBC module self-test. Record all TBC module DTCs. (cid:122) Is DTC U0100 retrieved again? |  |
| G3 RETRIEVE THE RECORDED DTCs FROM THE TBC MODULE SELF-TEST | Yes For DTC B1317, GO to Pinpoint Test D . For DTC B1318, GO to Pinpoint Test E . No GO to G4 . |
| (cid:122) Check for recorded TBC module DTCs from the previous self-test. (cid:122) Is DTC B1317 or DTC B1318 recorded? |  |
| G4 RETRIEVE THE RECORDED DTCs FROM THE PCM SELF-TEST | Yes REFER to Section 303-14 . No GO to G5 . |
| (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —PCM Key ON Engine OFF (KOEO) . (cid:122) Is DTC P0562 or DTC P0563 recorded? |  |
| G5 CHECK FOR DTC U0100:00 SET IN OTHER MODULES | Yes INSTALL a new PCM. REFER to Section 303-14 . No INSTALL a new TBC module. REFER to Trailer Brake Control (TBC) Module in this section. TEST the system for normal operation. |
| (cid:122) Using a scan tool, retrieve the continuous memory DTCs from the following modules: (cid:132) Accessory Protocol Interface Module (APIM) (if equipped) (cid:132) BCM (cid:132) Instrument Panel Cluster (IPC) (cid:132) Occupant Classification System Module (OCSM) (cid:132) Power Steering Control Module (PSCM) (if equipped) (cid:132) Restraints Control Module (RCM) (cid:132) Transfer Case Control Module (TCCM) (if equipped) (cid:122) Is DTC U0100:00 set in any of these modules? |  |

---
