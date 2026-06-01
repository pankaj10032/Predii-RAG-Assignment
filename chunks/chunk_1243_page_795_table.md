# Table on Page 795

**Page:** 795 | **Type:** table

**Table 1 on Page 795**

| N3 RETRIEVE THE RECORDED DTCs
FROM THE ABS MODULE AND SCCM
SELF-TESTS | Yes
For ABS module DTC B1676, GO to Pinpoint Test A .
For SCCM DTCs, REFER to Section 211-05 .
No
GO to N4 . |
| --- | --- |
| (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —ABS Module . (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —SCCM . (cid:122) Is DTC B1676 (or B11D9:16) or DTC B11D9:17 recorded? |  |
| N4 RECHECK THE ABS MODULE DTCs | Yes GO to N5 . No The system is operating correctly at this time. The DTC may have been set due to high network traffic or an intermittent fault condition. |
| (cid:122) Clear the DTCs. (cid:122) Ignition OFF. (cid:122) Wait 10 seconds. (cid:122) Ignition ON. (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —ABS Module . (cid:122) Is DTC U0131 still present? |  |
| N5 CHECK FOR DTC U0131 SET IN OTHER MODULES | Yes INSTALL a new SCCM . REFER to Section 211-00A . CLEAR the DTCs. REPEAT the ABS module self-test. No INSTALL a new ABS module. REFER to Anti-Lock Brake System (ABS) Module in this section. TEST the system for normal operation. |
| (cid:122) Clear the DTCs. (cid:122) Ignition OFF. (cid:122) Ignition ON. (cid:122) Wait 10 seconds. (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —All CMDTCs . (cid:122) Is DTC U0131 set in more than 1 module? |  |

---