# Table on Page 170

**Page:** 170 | **Type:** table

**Table 1 on Page 170**

| (cid:122) Using a scan tool, carry out the
TPM module self-test.
(cid:122) Using a scan tool, clear the
TPM module DTCs.
(cid:122) Ignition OFF.
(cid:122) Wait 10 seconds.
(cid:122) Ignition ON.
(cid:122) Using a scan tool, carry out the
TPM module self-test.
(cid:122) Is DTC U0140:87 retrieved
again? |  |
| --- | --- |
| I4 CHECK FOR DTCs IN THE BCM | Yes TPM module DTC U0140:87 may have been set due to a voltage issue in the BCM . REFER to the BCM DTC Chart in Section 419-10 . No GO to I5 . |
| (cid:122) Using a scan tool, carry out the BCM self-test. (cid:122) Is DTC U3003:16 or U3003:17 present? |  |
| I5 CHECK FOR DTC U0140, U0140:00, OR U0140:87 SET IN OTHER MODULES | Yes INSTALL a new BCM . REFER to Section 419-10 . CLEAR all continuous DTCs. REPEAT the self-test. No INSTALL a new TPM module. REFER to Tire Pressure Monitor (TPM) Module in this section. TEST the system for normal operation. |
| (cid:122) Clear the CMDTCs from all modules. (cid:122) Ignition OFF. (cid:122) Ignition ON. (cid:122) Wait 10 seconds. (cid:122) Using a scan tool, retrieve the CMDTCs from all modules. (cid:122) Is DTC U0140, U0140:00, or U0140:87 set in more than one module? |  |

---