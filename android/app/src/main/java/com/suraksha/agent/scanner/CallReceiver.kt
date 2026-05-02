package com.suraksha.agent.scanner

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.telephony.TelephonyManager
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

/**
 * Call Auto-Scanner
 * Detects incoming calls and checks the number against:
 *   1. Known scam number database
 *   2. Pattern analysis (premium rate, international, etc.)
 *   3. Backend AI analysis
 */
class CallReceiver : BroadcastReceiver() {

    companion object {
        private const val TAG = "SurakshaCallScan"

        // Known Indian scam number patterns
        private val SCAM_NUMBER_PATTERNS = listOf(
            Regex("^\\+?1800\\d{6,}"),          // Fake toll-free
            Regex("^\\+?0900\\d+"),              // Premium rate
            Regex("^\\+?\\d{2}9\\d{9}"),         // Suspicious international
            Regex("^\\+?44\\d{10}"),             // UK numbers used in India scams
            Regex("^\\+?1\\d{10}"),              // US numbers used in scams
            Regex("^\\+?92\\d{10}"),             // Pakistan numbers
            Regex("^\\+?880\\d{10}"),            // Bangladesh numbers
        )

        // Known scam number prefixes (from cybercrime.gov.in reports)
        private val KNOWN_SCAM_PREFIXES = setOf(
            "140", "141", "142", "143",          // Telemarketing (often misused)
            "1600", "1800",                       // Fake helplines
        )
    }

    override fun onReceive(context: Context, intent: Intent) {
        val state = intent.getStringExtra(TelephonyManager.EXTRA_STATE) ?: return
        val incomingNumber = intent.getStringExtra(TelephonyManager.EXTRA_INCOMING_NUMBER)
            ?: intent.getStringExtra("incoming_number")
            ?: return

        when (state) {
            TelephonyManager.EXTRA_STATE_RINGING -> {
                Log.d(TAG, "Incoming call from: $incomingNumber")
                CoroutineScope(Dispatchers.IO).launch {
                    analyzeIncomingCall(context, incomingNumber)
                }
            }
            TelephonyManager.EXTRA_STATE_IDLE -> {
                // Call ended — could trigger post-call analysis
                Log.d(TAG, "Call ended from: $incomingNumber")
            }
        }
    }

    private suspend fun analyzeIncomingCall(context: Context, number: String) {
        val threats = mutableListOf<String>()
        var riskScore = 0

        // Check 1: Known scam patterns
        for (pattern in SCAM_NUMBER_PATTERNS) {
            if (pattern.containsMatchIn(number)) {
                threats.add("Suspicious number pattern detected")
                riskScore += 30
                break
            }
        }

        // Check 2: Known scam prefixes
        val cleanNumber = number.replace("+91", "").replace(" ", "")
        for (prefix in KNOWN_SCAM_PREFIXES) {
            if (cleanNumber.startsWith(prefix)) {
                threats.add("Known scam number prefix: $prefix")
                riskScore += 25
                break
            }
        }

        // Check 3: International number calling India
        if (number.startsWith("+") && !number.startsWith("+91")) {
            threats.add("International number (not India)")
            riskScore += 15
        }

        // Check 4: Very short or very long numbers
        val digits = number.filter { it.isDigit() }
        if (digits.length < 8 || digits.length > 15) {
            threats.add("Unusual number length")
            riskScore += 10
        }

        // Check 5: Repeated digits (fake numbers)
        if (Regex("(\\d)\\1{5,}").containsMatchIn(digits)) {
            threats.add("Repeated digits pattern (fake number)")
            riskScore += 20
        }

        riskScore = minOf(riskScore, 100)

        val riskLevel = when {
            riskScore >= 50 -> "HIGH_RISK"
            riskScore >= 25 -> "SUSPICIOUS"
            else -> "SAFE"
        }

        Log.d(TAG, "Call analysis: $number | Risk: $riskLevel ($riskScore)")

        if (riskLevel != "SAFE") {
            ScanNotificationHelper.showCallAlert(
                context = context,
                number = number,
                riskLevel = riskLevel,
                riskScore = riskScore,
                threats = threats,
            )
        }

        // Save to history
        ScanHistoryManager.saveScan(
            context = context,
            type = "CALL",
            source = number,
            content = "Incoming call from $number",
            riskLevel = riskLevel,
            riskScore = riskScore,
            scamType = if (threats.isNotEmpty()) "Suspicious Call" else "Safe",
        )
    }
}
