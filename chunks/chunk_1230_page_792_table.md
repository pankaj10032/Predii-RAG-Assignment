# Table on Page 792

**Page:** 792 | **Type:** table

**Table 1 on Page 792**

| Test Step | Result / Action to Take |
| --- | --- |
| L1 VERIFY THE CUSTOMER CONCERN | Yes GO to L2 . No The system is operating normally at this time. The DTC may have been set due to high network traffic or an intermittent fault condition. |
| (cid:122) Ignition ON. (cid:122) Verify there is an observable symptom present. (cid:122) Is an observable symptom present? |  |
| L2 CHECK THE COMMUNICATION NETWORK | Yes GO to L3 . No REFER to Section 418-00 . |
| (cid:122) Using a scan tool, carry out a Network Test. (cid:122) Does the TCCM pass the network test? |  |
| L3 RETRIEVE THE RECORDED DTCs FROM THE ABS MODULE AND TCCM SELF-TESTS | Yes For ABS module DTC B1676, GO to Pinpoint Test A . For TCCM DTCs, REFER to Section 308-07A . No GO to L4 . |
| (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —ABS Module . (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —TCCM . (cid:122) Is DTC B1676 (or P0562:00) or DTC P0563:00 recorded? |  |
| L4 RECHECK THE ABS MODULE DTCs | Yes GO to L5 . No The system is operating correctly at this time. The DTC may have been set due to high network traffic or an intermittent fault condition. |
| (cid:122) Clear the DTCs. (cid:122) Ignition OFF. (cid:122) Wait 10 seconds. (cid:122) Ignition ON. (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —ABS Module . (cid:122) Is DTC U0114 still present? |  |
| L5 CHECK FOR DTC U0114 SET IN OTHER MODULES |  |

---