package com.suraksha.agent.scanner

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import android.util.Log
import com.suraksha.agent.data.api.RetrofitClient
import com.suraksha.agent.data.model.AnalyzeMessageRequest
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

/**
 * SMS Auto-Scanner
 * Automatically intercepts every incoming SMS and scans it for fraud.
 * Shows instant notification if scam detected.
 */
class SmsReceiver : BroadcastReceiver() {

    companion object {
        private const val TAG = "SurakshaSmsScan"
    }

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != Telephony.Sms.Intents.SMS_RECEIVED_ACTION) return

        // Extract all SMS messages from the intent
        val messages = Telephony.Sms.Intents.getMessagesFromIntent(intent)
        if (messages.isNullOrEmpty()) return

        // Combine multi-part messages
        val sender = messages[0].originatingAddress ?: "Unknown"
        val fullBody = messages.joinToString("") { it.messageBody ?: "" }

        Log.d(TAG, "SMS received from: $sender | Length: ${fullBody.length}")

        // Scan in background (don't block the broadcast)
        CoroutineScope(Dispatchers.IO).launch {
            scanSms(context, sender, fullBody)
            // Also scan any URLs found in the message
            UrlScanner.scanUrlsInMessage(context, fullBody, sender)
        }
    }

    private suspend fun scanSms(context: Context, sender: String, body: String) {
        try {
            val result = RetrofitClient.api.analyzeMessage(
                AnalyzeMessageRequest(message = body, language = "en")
            )

            Log.d(TAG, "Scan result: ${result.riskLevel} | Score: ${result.riskScore}")

            // Show notification for SUSPICIOUS or HIGH_RISK
            if (result.riskLevel == "SUSPICIOUS" || result.riskLevel == "HIGH_RISK") {
                ScanNotificationHelper.showSmsAlert(
                    context = context,
                    sender = sender,
                    riskLevel = result.riskLevel,
                    riskScore = result.riskScore,
                    scamType = result.scamType,
                    whyRisky = result.whyRisky,
                    whatToDo = result.whatToDo.firstOrNull() ?: "Do not respond"
                )
            }

            // Save to scan history
            ScanHistoryManager.saveScan(
                context = context,
                type = "SMS",
                source = sender,
                content = body.take(200),
                riskLevel = result.riskLevel,
                riskScore = result.riskScore,
                scamType = result.scamType,
            )

        } catch (e: Exception) {
            Log.e(TAG, "SMS scan failed: ${e.message}")
        }
    }
}
