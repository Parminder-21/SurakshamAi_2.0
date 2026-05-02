package com.suraksha.agent.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.suraksha.agent.scanner.ScanHistoryManager
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen() {
    val context = LocalContext.current
    var history by remember { mutableStateOf(ScanHistoryManager.getHistory(context)) }
    var stats by remember { mutableStateOf(ScanHistoryManager.getStats(context)) }
    var showClearDialog by remember { mutableStateOf(false) }
    var selectedFilter by remember { mutableStateOf("ALL") }

    val filters = listOf("ALL", "HIGH_RISK", "SUSPICIOUS", "SAFE")

    val filteredHistory = remember(history, selectedFilter) {
        if (selectedFilter == "ALL") history
        else history.filter { it.riskLevel == selectedFilter }
    }

    if (showClearDialog) {
        AlertDialog(
            onDismissRequest = { showClearDialog = false },
            title = { Text("Clear History?") },
            text = { Text("All ${history.size} scan records will be deleted permanently.") },
            confirmButton = {
                TextButton(onClick = {
                    ScanHistoryManager.clearHistory(context)
                    history = emptyList()
                    stats = ScanHistoryManager.getStats(context)
                    showClearDialog = false
                }) { Text("Clear", color = Color(0xFFEF4444)) }
            },
            dismissButton = {
                TextButton(onClick = { showClearDialog = false }) { Text("Cancel") }
            }
        )
    }

    Column(modifier = Modifier.fillMaxSize()) {
        TopAppBar(
            title = {
                Column {
                    Text("Scan History", fontWeight = FontWeight.Bold)
                    Text(
                        "${history.size} scans total",
                        fontSize = 12.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            },
            actions = {
                if (history.isNotEmpty()) {
                    IconButton(onClick = { showClearDialog = true }) {
                        Icon(Icons.Default.DeleteOutline, contentDescription = "Clear")
                    }
                }
            }
        )

        if (history.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(
                        Icons.Default.History,
                        contentDescription = null,
                        modifier = Modifier.size(64.dp),
                        tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.4f)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        "No scans yet",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        "Enable auto-scanner to start protecting yourself",
                        fontSize = 13.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f),
                        modifier = Modifier.padding(top = 6.dp)
                    )
                }
            }
        } else {
            // Stats row
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                MiniStatChip("${stats.scamsDetected}", "Scams", Color(0xFFEF4444), Modifier.weight(1f))
                MiniStatChip("${stats.suspicious}", "Suspicious", Color(0xFFF59E0B), Modifier.weight(1f))
                MiniStatChip("${stats.smsScanned}", "SMS", Color(0xFF3B82F6), Modifier.weight(1f))
                MiniStatChip("${stats.urlsScanned}", "URLs", Color(0xFFA855F7), Modifier.weight(1f))
            }

            // Filter chips
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                filters.forEach { filter ->
                    FilterChip(
                        selected = selectedFilter == filter,
                        onClick = { selectedFilter = filter },
                        label = { Text(filter.replace("_", " "), fontSize = 11.sp) },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = riskColor(filter).copy(alpha = 0.2f),
                            selectedLabelColor = riskColor(filter)
                        )
                    )
                }
            }

            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(filteredHistory, key = { it.id }) { record ->
                    HistoryItem(record)
                }
            }
        }
    }
}

@Composable
private fun HistoryItem(record: ScanHistoryManager.ScanRecord) {
    val color = riskColor(record.riskLevel)
    val typeIcon = when (record.type) {
        "SMS" -> Icons.Default.Sms
        "CALL" -> Icons.Default.Call
        "URL" -> Icons.Default.Link
        else -> Icons.Default.Shield
    }
    val dateFormat = remember { SimpleDateFormat("dd MMM, hh:mm a", Locale.getDefault()) }

    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = color.copy(alpha = 0.06f))
    ) {
        Row(modifier = Modifier.padding(12.dp), verticalAlignment = Alignment.Top) {
            Box(
                modifier = Modifier
                    .size(38.dp)
                    .clip(RoundedCornerShape(10.dp))
                    .background(color.copy(alpha = 0.15f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(typeIcon, contentDescription = null, tint = color, modifier = Modifier.size(18.dp))
            }

            Spacer(modifier = Modifier.width(12.dp))

            Column(modifier = Modifier.weight(1f)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        record.source,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    RiskBadgeSmall(record.riskLevel, record.riskScore)
                }

                if (record.content.isNotBlank()) {
                    Text(
                        record.content,
                        fontSize = 11.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.padding(top = 3.dp)
                    )
                }

                Row(
                    modifier = Modifier.padding(top = 6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (record.scamType.isNotBlank() && record.scamType != "SAFE") {
                        Text(
                            record.scamType,
                            fontSize = 10.sp,
                            color = color,
                            fontWeight = FontWeight.Medium
                        )
                        Text(
                            " • ",
                            fontSize = 10.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    Text(
                        dateFormat.format(Date(record.timestamp)),
                        fontSize = 10.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun MiniStatChip(value: String, label: String, color: Color, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(containerColor = color.copy(alpha = 0.1f))
    ) {
        Column(
            modifier = Modifier.padding(8.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(value, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = color)
            Text(label, fontSize = 9.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun RiskBadgeSmall(riskLevel: String, score: Int) {
    val color = riskColor(riskLevel)
    val label = when (riskLevel) {
        "HIGH_RISK" -> "HIGH"
        "SUSPICIOUS" -> "WARN"
        else -> "SAFE"
    }
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(4.dp))
            .background(color.copy(alpha = 0.15f))
            .padding(horizontal = 6.dp, vertical = 2.dp)
    ) {
        Text(
            "$label $score",
            fontSize = 10.sp,
            fontWeight = FontWeight.Bold,
            color = color
        )
    }
}

fun riskColor(riskLevel: String): Color = when (riskLevel) {
    "HIGH_RISK" -> Color(0xFFEF4444)
    "SUSPICIOUS" -> Color(0xFFF59E0B)
    "SAFE" -> Color(0xFF22C55E)
    else -> Color(0xFF6B7280)
}
