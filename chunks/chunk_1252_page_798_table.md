# Table on Page 798

**Page:** 798 | **Type:** table

**Table 1 on Page 798**

| Test Step | Result / Action to Take |
| --- | --- |
| P1 CHECK FOR A HS-CAN COMMUNICATION CONCERN WITH THE RCM OR PSCM | Yes GO to P2 . No REFER to Section 418-00 to diagnose the High Speed Controller Area Network (HS-CAN) bus. |
| (cid:122) Connect the scan tool. (cid:122) Ignition ON. (cid:122) NOTE: The Network Test does not test the dedicated CAN communications between the ABS module and RCM . (cid:122) Using a scan tool, carry out a Network Test. (cid:122) Does the RCM and PSCM pass the Network Test? |  |
| P2 CHECK FOR RCM AND PSCM DTCs | Yes For RCM DTCs, REFER to Section 501-20B . For PSCM DTCs, REFER to Section 211-00A . No If only one of the following ABS module DTCs C1280, C1282, C1516, C2770 was retrieved, GO to P3 . If more than one ABS module DTC C1280, C1282, C1516, C2770 was retrieved, GO to P7 . For DTCs U0151 and U0452, GO to P7 . For all other DTCs, GO to P3 . |
| (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —RCM . (cid:122) Enter the following diagnostic mode on the scan tool: Self Test —PSCM . (cid:122) Are any RCM or PSCM DTCs retrieved on-demand self-test? |  |
| P3 CHECK THE ABS MODULE YAW RATE (YAW_RATE_2) PID | Yes GO to P4 . No GO to P12 . |
| (cid:122) Enter the following diagnostic mode on the scan tool: Data Logger —ABS Module . (cid:122) NOTE: The vehicle must be on level ground and at a complete standstill. Any vehicle movement results in false values for this test. (cid:122) Monitor the YAW_RATE_2 PID. (cid:122) Is the YAW_RATE_2 PID value between -3.5 and 3.5? |  |

---