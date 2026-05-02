package com.suraksha.agent.scanner

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log

/**
 * Background Scanner Service
 * Runs as a foreground service so Android doesn't kill it.
 * Shows persistent notification "Suraksha Agent Active".
 * Keeps SMS/Call receivers alive even when app is closed.
 */
class ScannerService : Service() {

    companion object {
        private const val TAG = "SurakshaService"
        const val SERVICE_ID = 1
    }

    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, "Scanner service started")
        ScanNotificationHelper.createChannels(this)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Start as foreground service with persistent notification
        val notification = ScanNotificationHelper.buildServiceNotification(this)
        startForeground(SERVICE_ID, notification)
        Log.d(TAG, "Foreground service running — SMS/Call/URL scanning active")
        return START_STICKY  // Restart if killed by system
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "Scanner service stopped")
    }
}
