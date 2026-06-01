# Table on Page 791

**Page:** 791 | **Type:** table

**Table 1 on Page 791**

| Test Step | Result / Action to Take |
| --- | --- |
| K1 VERIFY THE SCAN TOOL COMMUNICATES WITH THE PCM | Yes GO to K2 . No REFER to Section 418-00 to diagnose no communication with the PCM. |
| (cid:122) Connect the scan tool. (cid:122) Check that a vehicle session can be established using the scan tool. (cid:122) Can a vehicle session be established? |  |
| K2 CHECK THE ABS MODULE CONTINUOUS MEMORY DTCs | Yes GO to K3 . No The system is operating correctly at this time. The DTC may have been set due to high network traffic or an intermittent fault condition. |
| (cid:122) Ignition ON. (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —ABS Module . (cid:122) Clear the DTCs. (cid:122) Wait 10 seconds. (cid:122) Repeat the ABS module self-test. (cid:122) Is DTC U0100 retrieved again? |  |
| K3 RETRIEVE THE RECORDED DTCs FROM THE PCM KOEO SELF-TEST | Yes For PCM DTCs, REFER to Section 303-14 . No GO to K4 . |
| (cid:122) Check for recorded DTCs from the PCM Key ON Engine OFF (KOEO) self-test. (cid:122) Is DTC P0562 or P0563 recorded? |  |
| K4 RETRIEVE THE RECORDED DTCs FROM THE ABS MODULE SELF-TEST | Yes GO to Pinpoint Test A . No GO to K5 . |
| (cid:122) Check for recorded DTCs from the ABS module self-test. (cid:122) Is DTC B1676 recorded? |  |
| K5 CHECK FOR DTC U0100 SET IN OTHER MODULES | Yes INSTALL a new PCM. REFER to Section 303-14 . TEST the system for normal operation. No INSTALL a new ABS module. REFER to Anti-Lock Brake System (ABS) Module in this section. TEST the system for normal operation. |
| (cid:122) Ignition ON. (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —All CMDTCs . (cid:122) Retrieve the continuous memory DTCs from all modules. (cid:122) Is DTC U0100:00 or U0100 set in more than 1 module? |  |

---