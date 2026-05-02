package com.suraksha.agent.ui.screens

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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.suraksha.agent.scanner.PermissionManager
import com.suraksha.agent.scanner.ScanHistoryManager

@Composable
fun HomeScreen(
    onNavigateToScan: () -> Unit,
    onNavigateToNews: () -> Unit,
    onNavigateToReport: () -> Unit,
    onNavigateToShield: () -> Unit,
) {
    val context = LocalContext.current

    // Live scanner status — refreshes on every recomposition
    var scannerActive by remember { mutableStateOf(PermissionManager.hasAllPermissions(context)) }
    var stats by remember { mutableStateOf(ScanHistoryManager.getStats(context)) }

    // Refresh on resume
    LaunchedEffect(Unit) {
        scannerActive = PermissionManager.hasAllPermissions(context)
        stats = ScanHistoryManager.getStats(context)
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(16.dp))

        // ── Scanner Status Banner ─────────────────────────────────────────────
        ScannerStatusBanner(
            isActive = scannerActive,
            stats = stats,
            onSetupClick = onNavigateToShield
        )

        Spacer(modifier = Modifier.height(20.dp))

        // ── Logo + Title ──────────────────────────────────────────────────────
        Icon(
            imageVector = Icons.Default.Security,
            contentDescription = "Shield",
            tint = MaterialTheme.colorScheme.primary,
            modifier = Modifier.size(52.dp)
        )
        Spacer(modifier = Modifier.height(10.dp))
        Text(
            text = "Suraksham AI",
            fontSize = 26.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onBackground
        )
        Text(
            text = "AI Cyber Safety — India's #1 Scam Detector",
            fontSize = 13.sp,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(top = 4.dp)
        )

        Spacer(modifier = Modifier.height(24.dp))

        // ── Primary CTA ───────────────────────────────────────────────────────
        Button(
            onClick = onNavigateToScan,
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp),
            shape = MaterialTheme.shapes.large
        ) {
            Icon(Icons.Default.Search, contentDescription = null)
            Spacer(modifier = Modifier.width(8.dp))
            Text("Check a Message or URL", fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
        }

        Spacer(modifier = Modifier.height(12.dp))

        // ── Secondary Actions ─────────────────────────────────────────────────
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            OutlinedButton(
                onClick = onNavigateToShield,
                modifier = Modifier.weight(1f).height(46.dp),
                shape = MaterialTheme.shapes.medium
            ) {
                Icon(Icons.Default.Shield, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text("Auto-Scan", fontSize = 13.sp)
            }
            OutlinedButton(
                onClick = onNavigateToNews,
                modifier = Modifier.weight(1f).height(46.dp),
                shape = MaterialTheme.shapes.medium
            ) {
                Icon(Icons.Default.Newspaper, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text("Scam News", fontSize = 13.sp)
            }
            OutlinedButton(
                onClick = onNavigateToReport,
                modifier = Modifier.weight(1f).height(46.dp),
                shape = MaterialTheme.shapes.medium
            ) {
                Icon(Icons.Default.Report, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text("Report", fontSize = 13.sp)
            }
        }

        Spacer(modifier = Modifier.height(28.dp))

        // ── What We Detect ────────────────────────────────────────────────────
        Text(
            text = "What we detect",
            fontSize = 15.sp,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onBackground,
            modifier = Modifier.align(Alignment.Start)
        )
        Spacer(modifier = Modifier.height(10.dp))

        val features = listOf(
            Triple(Icons.Default.CreditCard,      "Fake KYC Scams",       Color(0xFF3B82F6)),
            Triple(Icons.Default.AccountBalance,  "UPI / Payment Fraud",  Color(0xFFF59E0B)),
            Triple(Icons.Default.Work,            "Job Fraud",            Color(0xFF22C55E)),
            Triple(Icons.Default.LocalShipping,   "Courier Scams",        Color(0xFFF97316)),
            Triple(Icons.Default.EmojiEvents,     "Lottery Scams",        Color(0xFFA855F7)),
            Triple(Icons.Default.Key,             "OTP Theft",            Color(0xFFEF4444)),
            Triple(Icons.Default.Gavel,             "Digital Arrest",       Color(0xFFEC4899)),
            Triple(Icons.Default.TrendingUp,      "Investment Scams",     Color(0xFF14B8A6)),
        )

        features.chunked(2).forEach { row ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                row.forEach { (icon, label, color) ->
                    FeatureChip(icon = icon, label = label, color = color, modifier = Modifier.weight(1f))
                }
                if (row.size == 1) Spacer(modifier = Modifier.weight(1f))
            }
            Spacer(modifier = Modifier.height(8.dp))
        }

        Spacer(modifier = Modifier.height(20.dp))

        // ── Privacy Note ──────────────────────────────────────────────────────
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.3f)
            )
        ) {
            Row(
                modifier = Modifier.padding(14.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    Icons.Default.Lock,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(18.dp)
                )
                Spacer(modifier = Modifier.width(10.dp))
                Text(
                    text = "Your PAN, Aadhaar & phone numbers are masked before any analysis.",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
    }
}

// ── Scanner Status Banner ─────────────────────────────────────────────────────

@Composable
private fun ScannerStatusBanner(
    isActive: Boolean,
    stats: ScanHistoryManager.ScanStats,
    onSetupClick: () -> Unit
) {
    val statusColor = if (isActive) Color(0xFF22C55E) else Color(0xFFF59E0B)
    val bgColor = statusColor.copy(alpha = 0.1f)

    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = bgColor),
        shape = RoundedCornerShape(14.dp),
        onClick = onSetupClick
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Pulsing status dot
            Box(
                modifier = Modifier
                    .size(10.dp)
                    .clip(CircleShape)
                    .background(statusColor)
            )
            Spacer(modifier = Modifier.width(10.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = if (isActive) "🛡️ Auto-Scanner Active" else "⚠️ Auto-Scanner Off",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = statusColor
                )
                Text(
                    text = if (isActive)
                        "${stats.totalScans} scans • ${stats.scamsDetected} scams blocked"
                    else
                        "Tap to enable automatic SMS & call protection",
                    fontSize = 11.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Icon(
                Icons.Default.ChevronRight,
                contentDescription = null,
                tint = statusColor,
                modifier = Modifier.size(18.dp)
            )
        }
    }
}

// ── Feature Chip ──────────────────────────────────────────────────────────────

@Composable
private fun FeatureChip(
    icon: ImageVector,
    label: String,
    color: Color,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        )
    ) {
        Row(
            modifier = Modifier.padding(10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = color, modifier = Modifier.size(16.dp))
            Spacer(modifier = Modifier.width(6.dp))
            Text(label, fontSize = 11.sp, fontWeight = FontWeight.Medium)
        }
    }
}
