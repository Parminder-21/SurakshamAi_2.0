package com.suraksha.agent.scanner

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.graphics.Color
import androidx.core.app.NotificationCompat
import com.suraksha.agent.MainActivity
import com.suraksha.agent.R

/**
 * Notification Helper
 * Shows instant alerts when scam SMS, call, or URL is detected.
 */
object ScanNotificationHelper {

    private const val CHANNEL_HIGH_RISK = "suraksha_high_risk"
    private const val CHANNEL_SUSPICIOUS = "suraksha_suspicious"
    private const val CHANNEL_SAFE = "suraksha_safe"

    private var notificationId = 1000

    fun createChannels(context: Context) {
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // HIGH RISK — Red, makes sound + vibration
        NotificationChannel(
            CHANNEL_HIGH_RISK,
            "High Risk Alerts",
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Scam detected — immediate action needed"
            enableLights(true)
            lightColor = Color.RED
            enableVibration(true)
            vibrationPattern = longArrayOf(0, 500, 200, 500, 200, 500)
            manager.createNotificationChannel(this)
        }

        // SUSPICIOUS — Yellow, makes sound
        NotificationChannel(
            CHANNEL_SUSPICIOUS,
            "Suspicious Alerts",
            NotificationManager.IMPORTANCE_DEFAULT
        ).apply {
            description = "Suspicious activity detected"
            enableLights(true)
            lightColor = Color.YELLOW
            manager.createNotificationChannel(this)
        }

        // SAFE — Silent info
        NotificationChannel(
            CHANNEL_SAFE,
            "Scan Results",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "Scan completed — safe"
            manager.createNotificationChannel(this)
        }
    }

    // ── SMS Alert ─────────────────────────────────────────────────────────────

    fun showSmsAlert(
        context: Context,
        sender: String,
        riskLevel: String,
        riskScore: Int,
        scamType: String,
        whyRisky: String,
        whatToDo: String,
    ) {
        val isHighRisk = riskLevel == "HIGH_RISK"
        val emoji = if (isHighRisk) "🔴" else "⚠️"
        val channel = if (isHighRisk) CHANNEL_HIGH_RISK else CHANNEL_SUSPICIOUS

        val title = "$emoji SCAM SMS Detected! ($riskScore/100)"
        val text = "From: $sender\nType: $scamType\n$whatToDo"

        showNotification(
            context = context,
            channel = channel,
            title = title,
            text = text,
            bigText = "$whyRisky\n\n✅ $whatToDo",
            isHighPriority = isHighRisk,
        )
    }

    // ── Call Alert ────────────────────────────────────────────────────────────

    fun showCallAlert(
        context: Context,
        number: String,
        riskLevel: String,
        riskScore: Int,
        threats: List<String>,
    ) {
        val isHighRisk = riskLevel == "HIGH_RISK"
        val emoji = if (isHighRisk) "🔴" else "⚠️"
        val channel = if (isHighRisk) CHANNEL_HIGH_RISK else CHANNEL_SUSPICIOUS

        val title = "$emoji Suspicious Call! ($riskScore/100)"
        val text = "Number: $number\n${threats.firstOrNull() ?: "Be cautious"}"
        val bigText = "Incoming call from $number\n\n" +
                threats.joinToString("\n") { "• $it" } +
                "\n\n⚠️ Do not share OTP, bank details, or personal info"

        showNotification(
            context = context,
            channel = channel,
            title = title,
            text = text,
            bigText = bigText,
            isHighPriority = isHighRisk,
        )
    }

    // ── URL Alert ─────────────────────────────────────────────────────────────

    fun showUrlAlert(
        context: Context,
        url: String,
        source: String,
        riskLevel: String,
        riskScore: Int,
        threats: List<String>,
        recommendation: String,
    ) {
        val isHighRisk = riskLevel == "HIGH_RISK"
        val emoji = if (isHighRisk) "🔴" else "⚠️"
        val channel = if (isHighRisk) CHANNEL_HIGH_RISK else CHANNEL_SUSPICIOUS

        val shortUrl = if (url.length > 50) url.take(47) + "..." else url
        val title = "$emoji Phishing URL Detected! ($riskScore/100)"
        val text = "In: $source\n$shortUrl"
        val bigText = "Phishing link found in $source:\n$url\n\n" +
                threats.take(3).joinToString("\n") { "• $it" } +
                "\n\n🛡️ $recommendation"

        showNotification(
            context = context,
            channel = channel,
            title = title,
            text = text,
            bigText = bigText,
            isHighPriority = isHighRisk,
        )
    }

    // ── Background Service Notification ──────────────────────────────────────

    fun buildServiceNotification(context: Context): android.app.Notification {
        createChannels(context)
        val intent = Intent(context, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            context, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        return NotificationCompat.Builder(context, CHANNEL_SAFE)
            .setSmallIcon(android.R.drawable.ic_lock_idle_lock)
            .setContentTitle("🛡️ Suraksham AI Active")
            .setContentText("Scanning SMS, calls, and URLs automatically")
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    // ── FCM Threat Alert ──────────────────────────────────────────────────────

    fun showThreatAlert(
        context: Context,
        title: String,
        message: String,
        severity: String,
    ) {
        val isHigh = severity == "HIGH"
        val channel = if (isHigh) CHANNEL_HIGH_RISK else CHANNEL_SUSPICIOUS
        showNotification(
            context = context,
            channel = channel,
            title = title,
            text = message,
            bigText = message,
            isHighPriority = isHigh,
        )
    }

    // ── Private Helper ────────────────────────────────────────────────────────

    private fun showNotification(
        context: Context,
        channel: String,
        title: String,
        text: String,
        bigText: String,
        isHighPriority: Boolean,
    ) {
        createChannels(context)

        val intent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val pendingIntent = PendingIntent.getActivity(
            context, notificationId, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(context, channel)
            .setSmallIcon(android.R.drawable.ic_dialog_alert)
            .setContentTitle(title)
            .setContentText(text)
            .setStyle(NotificationCompat.BigTextStyle().bigText(bigText))
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .setPriority(
                if (isHighPriority) NotificationCompat.PRIORITY_MAX
                else NotificationCompat.PRIORITY_HIGH
            )
            .setColor(if (isHighPriority) Color.RED else Color.parseColor("#F59E0B"))
            .build()

        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.notify(notificationId++, notification)
    }
}
