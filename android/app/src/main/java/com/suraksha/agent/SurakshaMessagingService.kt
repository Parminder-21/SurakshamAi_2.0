package com.suraksha.agent

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import com.suraksha.agent.scanner.ScanNotificationHelper

/**
 * Suraksha Messaging Service
 * Stub service for Firebase Cloud Messaging.
 * To enable FCM: add google-services.json and uncomment Firebase in build.gradle
 *
 * Currently acts as a placeholder so AndroidManifest.xml compiles without Firebase SDK.
 */
class SurakshaMessagingService : Service() {

    companion object {
        private const val TAG = "SurakshaFCM"

        /**
         * Call this to show a threat alert notification from anywhere.
         */
        fun showAlert(service: android.content.Context, title: String, message: String, severity: String) {
            Log.d(TAG, "Threat alert: $title")
            ScanNotificationHelper.showThreatAlert(
                context = service,
                title = title,
                message = message,
                severity = severity,
            )
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d(TAG, "SurakshaMessagingService started")
        return START_NOT_STICKY
    }
}
