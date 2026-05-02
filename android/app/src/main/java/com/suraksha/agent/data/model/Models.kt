package com.suraksha.agent.data.model

import com.google.gson.annotations.SerializedName

// ── Request Models ────────────────────────────────────────────────────────────

data class AnalyzeMessageRequest(
    val message: String,
    val language: String = "en"
)

data class AnalyzeUrlRequest(
    val url: String,
    val context: String? = null
)

data class AnalyzeCallRequest(
    val summary: String,
    val language: String = "en"
)

data class ReportScamRequest(
    val content: String,
    @SerializedName("scam_type") val scamType: String? = null,
    @SerializedName("reporter_note") val reporterNote: String? = null,
    val source: String = "app"
)

// ── Response Models ───────────────────────────────────────────────────────────

data class RiskScoreBreakdown(
    @SerializedName("urgency_score") val urgencyScore: Int,
    @SerializedName("authority_impersonation_score") val authorityScore: Int,
    @SerializedName("payment_pressure_score") val paymentScore: Int,
    @SerializedName("deception_fear_score") val deceptionScore: Int,
    val total: Int
)

data class AnalysisResult(
    @SerializedName("risk_level") val riskLevel: String,
    @SerializedName("risk_score") val riskScore: Int,
    @SerializedName("score_breakdown") val scoreBreakdown: RiskScoreBreakdown,
    @SerializedName("scam_type") val scamType: String,
    val confidence: Float,
    @SerializedName("red_flags") val redFlags: List<String>,
    @SerializedName("why_risky") val whyRisky: String,
    @SerializedName("what_not_to_do") val whatNotToDo: List<String>,
    @SerializedName("what_to_do") val whatToDo: List<String>,
    @SerializedName("scrubbed_text") val scrubbedText: String,
    val language: String = "en"
)

data class UrlAnalysisResult(
    val url: String,
    @SerializedName("is_safe") val isSafe: Boolean,
    @SerializedName("risk_level") val riskLevel: String,
    @SerializedName("risk_score") val riskScore: Int,
    val threats: List<String>,
    @SerializedName("domain_age_days") val domainAgeDays: Int?,
    @SerializedName("is_brand_impersonation") val isBrandImpersonation: Boolean,
    @SerializedName("impersonated_brand") val impersonatedBrand: String?,
    @SerializedName("safe_browsing_flagged") val safeBrowsingFlagged: Boolean,
    val recommendation: String
)

data class NewsFeedItem(
    val id: String,
    val title: String,
    val slug: String,
    val summary: String,
    @SerializedName("scam_type") val scamType: String,
    val severity: String,
    @SerializedName("report_count") val reportCount: Int,
    @SerializedName("published_at") val publishedAt: String,
    val tags: List<String>
)

data class ReportScamResponse(
    val success: Boolean,
    @SerializedName("report_id") val reportId: String,
    val message: String
)

// ── UI State ──────────────────────────────────────────────────────────────────

enum class RiskLevel { SAFE, SUSPICIOUS, HIGH_RISK }

fun String.toRiskLevel(): RiskLevel = when (this) {
    "SAFE" -> RiskLevel.SAFE
    "SUSPICIOUS" -> RiskLevel.SUSPICIOUS
    "HIGH_RISK" -> RiskLevel.HIGH_RISK
    else -> RiskLevel.SUSPICIOUS
}
