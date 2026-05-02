package com.suraksha.agent.scanner

import android.content.Context
import android.util.Log
import com.suraksha.agent.data.api.RetrofitClient
import com.suraksha.agent.data.model.AnalyzeUrlRequest

/**
 * URL Auto-Scanner
 * Extracts URLs from SMS/notifications and scans them automatically.
 * Also provides manual URL scanning.
 */
object UrlScanner {

    private const val TAG = "SurakshaUrlScan"

    // Regex to extract URLs from text
    private val URL_REGEX = Regex(
        """https?://[^\s<>"{}|\\^`\[\]]+|www\.[^\s<>"{}|\\^`\[\]]+""",
        RegexOption.IGNORE_CASE
    )

    /**
     * Extract all URLs from a text message.
     */
    fun extractUrls(text: String): List<String> {
        return URL_REGEX.findAll(text)
            .map { it.value.trimEnd('.', ',', ')', ']') }
            .filter { it.length > 10 }
            .distinct()
            .toList()
    }

    /**
     * Scan all URLs found in a message.
     * Called automatically when SMS contains links.
     */
    suspend fun scanUrlsInMessage(
        context: Context,
        message: String,
        sender: String,
    ) {
        val urls = extractUrls(message)
        if (urls.isEmpty()) return

        Log.d(TAG, "Found ${urls.size} URLs in message from $sender")

        for (url in urls) {
            scanSingleUrl(context, url, sender)
        }
    }

    /**
     * Scan a single URL.
     */
    suspend fun scanSingleUrl(
        context: Context,
        url: String,
        source: String = "Manual",
    ): UrlScanResult {
        return try {
            Log.d(TAG, "Scanning URL: $url")

            val result = RetrofitClient.api.analyzeUrl(AnalyzeUrlRequest(url = url))

            val scanResult = UrlScanResult(
                url = url,
                riskLevel = result.riskLevel,
                riskScore = result.riskScore,
                threats = result.threats,
                isBrandImpersonation = result.isBrandImpersonation,
                impersonatedBrand = result.impersonatedBrand,
                recommendation = result.recommendation,
            )

            // Show notification if risky
            if (result.riskLevel == "SUSPICIOUS" || result.riskLevel == "HIGH_RISK") {
                ScanNotificationHelper.showUrlAlert(
                    context = context,
                    url = url,
                    source = source,
                    riskLevel = result.riskLevel,
                    riskScore = result.riskScore,
                    threats = result.threats,
                    recommendation = result.recommendation,
                )
            }

            // Save to history
            ScanHistoryManager.saveScan(
                context = context,
                type = "URL",
                source = source,
                content = url,
                riskLevel = result.riskLevel,
                riskScore = result.riskScore,
                scamType = if (result.isBrandImpersonation) "Phishing URL" else "Suspicious URL",
            )

            scanResult

        } catch (e: Exception) {
            Log.e(TAG, "URL scan failed for $url: ${e.message}")
            UrlScanResult(
                url = url,
                riskLevel = "UNKNOWN",
                riskScore = 0,
                threats = listOf("Scan failed: ${e.message}"),
                isBrandImpersonation = false,
                impersonatedBrand = null,
                recommendation = "Could not scan. Be cautious.",
            )
        }
    }
}

data class UrlScanResult(
    val url: String,
    val riskLevel: String,
    val riskScore: Int,
    val threats: List<String>,
    val isBrandImpersonation: Boolean,
    val impersonatedBrand: String?,
    val recommendation: String,
)
