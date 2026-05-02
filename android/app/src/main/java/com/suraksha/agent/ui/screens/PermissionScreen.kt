package com.suraksha.agent.ui.screens

import android.Manifest
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.suraksha.agent.scanner.PermissionManager
import com.suraksha.agent.scanner.ScanHistoryManager

@Composable
fun PermissionScreen() {
    val context = LocalContext.current
    var permissionStatus by remember { mutableStateOf(PermissionManager.getPermissionStatus(context)) }
    var scannerActive by remember { mutableStateOf(false) }
    var stats by remember { mutableStateOf(ScanHistoryManager.getStats(context)) }

    // Permission launcher
    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { results ->
        permissionStatus = PermissionManager.getPermissionStatus(context)
        // Auto-start scanner if all permissions granted
        if (PermissionManager.hasAllPermissions(context)) {
            PermissionManager.startScannerService(context)
            scannerActive = true
        }
    }

    // Refresh stats on resume
    LaunchedEffect(Unit) {
        permissionStatus = PermissionManager.getPermissionStatus(context)
        stats = ScanHistoryManager.getStats(context)
    }

    val allGranted = permissionStatus.values.all { it }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(16.dp))

        // Header
        Text(
            text = "Auto-Scanner",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onBackground
        )
        Text(
            text = "Automatic protection for SMS, Calls & URLs",
            fontSize = 13.sp,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(top = 4.dp, bottom = 24.dp)
        )

        // Scanner Status Card
        ScannerStatusCard(
            isActive = allGranted && scannerActive,
            stats = stats,
            onToggle = { enable ->
                if (enable) {
                    if (PermissionManager.hasAllPermissions(context)) {
                        PermissionManager.startScannerService(context)
                        scannerActive = true
                    } else {
                        // Request permissions first
                        val perms = buildList {
                            add(Manifest.permission.RECEIVE_SMS)
                            add(Manifest.permission.READ_SMS)
                            add(Manifest.permission.READ_PHONE_STATE)
                            add(Manifest.permission.READ_CALL_LOG)
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                                add(Manifest.permission.POST_NOTIFICATIONS)
                            }
                        }.toTypedArray()
                        permissionLauncher.launch(perms)
                    }
                } else {
                    PermissionManager.stopScannerService(context)
                    scannerActive = false
                }
            }
        )

        Spacer(modifier = Modifier.height(20.dp))

        // Permissions Section
        Text(
            text = "Required Permissions",
            fontSize = 15.sp,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onBackground,
            modifier = Modifier
                .align(Alignment.Start)
                .padding(bottom = 10.dp)
        )

        PermissionItem(
            icon = Icons.Default.Sms,
            title = "SMS Access",
            description = "Read & receive SMS to detect scam messages automatically",
            granted = permissionStatus["SMS Scanning"] ?: false,
            onRequest = {
                permissionLauncher.launch(
                    arrayOf(Manifest.permission.RECEIVE_SMS, Manifest.permission.READ_SMS)
                )
            }
        )

        Spacer(modifier = Modifier.height(8.dp))

        PermissionItem(
            icon = Icons.Default.Call,
            title = "Phone / Call Access",
            description = "Detect incoming calls from known scam numbers",
            granted = permissionStatus["Call Detection"] ?: false,
            onRequest = {
                permissionLauncher.launch(
                    arrayOf(Manifest.permission.READ_PHONE_STATE, Manifest.permission.READ_CALL_LOG)
                )
            }
        )

        Spacer(modifier = Modifier.height(8.dp))

        PermissionItem(
            icon = Icons.Default.Notifications,
            title = "Notifications",
            description = "Show instant alerts when scam is detected",
            granted = permissionStatus["Notifications"] ?: false,
            onRequest = {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    permissionLauncher.launch(arrayOf(Manifest.permission.POST_NOTIFICATIONS))
                }
            }
        )

        Spacer(modifier = Modifier.height(20.dp))

        // What we scan section
        Text(
            text = "What Gets Scanned",
            fontSize = 15.sp,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onBackground,
            modifier = Modifier
                .align(Alignment.Start)
                .padding(bottom = 10.dp)
        )

        ScanTypeCard(
            icon = Icons.Default.Sms,
            title = "Every Incoming SMS",
            description = "Scanned for UPI fraud, fake KYC, OTP theft, lottery scams",
            color = Color(0xFF3B82F6)
        )
        Spacer(modifier = Modifier.height(8.dp))
        ScanTypeCard(
            icon = Icons.Default.Link,
            title = "URLs in Messages",
            description = "Every link in SMS checked against 789k phishing database",
            color = Color(0xFFEF4444)
        )
        Spacer(modifier = Modifier.height(8.dp))
        ScanTypeCard(
            icon = Icons.Default.Call,
            title = "Incoming Calls",
            description = "Caller ID checked for known scam patterns",
            color = Color(0xFF22C55E)
        )

        Spacer(modifier = Modifier.height(20.dp))

        // Privacy note
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.3f)
            )
        ) {
            Row(
                modifier = Modifier.padding(14.dp),
                verticalAlignment = Alignment.Top
            ) {
                Icon(
                    Icons.Default.Lock,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier
                        .size(18.dp)
                        .padding(top = 2.dp)
                )
                Spacer(modifier = Modifier.width(10.dp))
                Column {
                    Text(
                        "Privacy Protected",
                        fontSize = 13.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.primary
                    )
                    Text(
                        "Your PAN, Aadhaar, phone numbers are masked before analysis. Messages are never stored on our servers.",
                        fontSize = 12.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(top = 2.dp)
                    )
                }
            }
        }

        // Open settings button (if permissions denied)
        AnimatedVisibility(!allGranted) {
            Column {
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedButton(
                    onClick = { PermissionManager.openAppSettings(context) },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Icon(Icons.Default.Settings, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Open App Settings")
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
    }
}

@Composable
private fun ScannerStatusCard(
    isActive: Boolean,
    stats: ScanHistoryManager.ScanStats,
    onToggle: (Boolean) -> Unit
) {
    val statusColor = if (isActive) Color(0xFF22C55E) else Color(0xFF6B7280)

    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = if (isActive)
                Color(0xFF22C55E).copy(alpha = 0.1f)
            else
                MaterialTheme.colorScheme.surfaceVariant
        ),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    // Pulsing dot
                    Box(
                        modifier = Modifier
                            .size(10.dp)
                            .clip(CircleShape)
                            .background(statusColor)
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Column {
                        Text(
                            text = if (isActive) "Scanner Active" else "Scanner Inactive",
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Bold,
                            color = statusColor
                        )
                        Text(
                            text = if (isActive) "Protecting you 24/7" else "Tap to enable protection",
                            fontSize = 12.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                Switch(
                    checked = isActive,
                    onCheckedChange = onToggle,
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = Color.White,
                        checkedTrackColor = Color(0xFF22C55E)
                    )
                )
            }

            if (stats.totalScans > 0) {
                Spacer(modifier = Modifier.height(16.dp))
                HorizontalDivider(color = MaterialTheme.colorScheme.outline.copy(alpha = 0.3f))
                Spacer(modifier = Modifier.height(12.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    StatItem("${stats.totalScans}", "Total Scans", Color(0xFF3B82F6))
                    StatItem("${stats.scamsDetected}", "Scams Found", Color(0xFFEF4444))
                    StatItem("${stats.suspicious}", "Suspicious", Color(0xFFF59E0B))
                }
            }
        }
    }
}

@Composable
private fun StatItem(value: String, label: String, color: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(value, fontSize = 20.sp, fontWeight = FontWeight.Bold, color = color)
        Text(label, fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
private fun PermissionItem(
    icon: ImageVector,
    title: String,
    description: String,
    granted: Boolean,
    onRequest: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        )
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(RoundedCornerShape(10.dp))
                    .background(
                        if (granted) Color(0xFF22C55E).copy(alpha = 0.15f)
                        else MaterialTheme.colorScheme.surfaceVariant
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    icon,
                    contentDescription = null,
                    tint = if (granted) Color(0xFF22C55E) else MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(20.dp)
                )
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(title, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                Text(
                    description,
                    fontSize = 11.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(top = 2.dp)
                )
            }
            Spacer(modifier = Modifier.width(8.dp))
            if (granted) {
                Icon(
                    Icons.Default.CheckCircle,
                    contentDescription = "Granted",
                    tint = Color(0xFF22C55E),
                    modifier = Modifier.size(24.dp)
                )
            } else {
                TextButton(onClick = onRequest) {
                    Text("Allow", fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                }
            }
        }
    }
}

@Composable
private fun ScanTypeCard(
    icon: ImageVector,
    title: String,
    description: String,
    color: Color
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = color.copy(alpha = 0.08f)
        )
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = color, modifier = Modifier.size(22.dp))
            Spacer(modifier = Modifier.width(12.dp))
            Column {
                Text(title, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = color)
                Text(
                    description,
                    fontSize = 11.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(top = 2.dp)
                )
            }
        }
    }
}
