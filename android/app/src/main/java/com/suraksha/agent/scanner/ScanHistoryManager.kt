package com.suraksha.agent.scanner

import android.content.Context
import android.content.SharedPreferences
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

/**
 * Scan History Manager
 * Saves all auto-scanned SMS, calls, and URLs locally.
 * Shown in the History screen of the app.
 */
object ScanHistoryManager {

    private const val PREFS_NAME = "suraksha_scan_history"
    private const val KEY_HISTORY = "history"
    private const val MAX_HISTORY = 200  // Keep last 200 scans

    private val gson = Gson()

    data class ScanRecord(
        val id: Long = System.currentTimeMillis(),
        val type: String,           // SMS | CALL | URL
        val source: String,         // Phone number / URL / App
        val content: String,        // Message preview / URL
        val riskLevel: String,      // SAFE | SUSPICIOUS | HIGH_RISK
        val riskScore: Int,
        val scamType: String,
        val timestamp: Long = System.currentTimeMillis(),
    )

    fun saveScan(
        context: Context,
        type: String,
        source: String,
        content: String,
        riskLevel: String,
        riskScore: Int,
        scamType: String,
    ) {
        val record = ScanRecord(
            type = type,
            source = source,
            content = content.take(300),
            riskLevel = riskLevel,
            riskScore = riskScore,
            scamType = scamType,
        )

        val history = getHistory(context).toMutableList()
        history.add(0, record)  // Add to front

        // Keep only last MAX_HISTORY records
        val trimmed = if (history.size > MAX_HISTORY) history.take(MAX_HISTORY) else history

        getPrefs(context).edit()
            .putString(KEY_HISTORY, gson.toJson(trimmed))
            .apply()
    }

    fun getHistory(context: Context): List<ScanRecord> {
        val json = getPrefs(context).getString(KEY_HISTORY, null) ?: return emptyList()
        return try {
            val type = object : TypeToken<List<ScanRecord>>() {}.type
            gson.fromJson(json, type) ?: emptyList()
        } catch (e: Exception) {
            emptyList()
        }
    }

    fun getStats(context: Context): ScanStats {
        val history = getHistory(context)
        return ScanStats(
            totalScans = history.size,
            scamsDetected = history.count { it.riskLevel == "HIGH_RISK" },
            suspicious = history.count { it.riskLevel == "SUSPICIOUS" },
            smsScanned = history.count { it.type == "SMS" },
            callsScanned = history.count { it.type == "CALL" },
            urlsScanned = history.count { it.type == "URL" },
        )
    }

    fun clearHistory(context: Context) {
        getPrefs(context).edit().remove(KEY_HISTORY).apply()
    }

    private fun getPrefs(context: Context): SharedPreferences =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    data class ScanStats(
        val totalScans: Int,
        val scamsDetected: Int,
        val suspicious: Int,
        val smsScanned: Int,
        val callsScanned: Int,
        val urlsScanned: Int,
    )
}
