package com.suraksha.agent.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.suraksha.agent.data.api.RetrofitClient
import com.suraksha.agent.data.model.NewsFeedItem
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

// ── Constants ─────────────────────────────────────────────────────────────────

private val BgColor = Color(0xFF0F172A)
private val SurfaceColor = Color(0xFF1E293B)
private val PrimaryColor = Color(0xFF3B82F6)
private val DangerColor = Color(0xFFF87171)
private val WarnColor = Color(0xFFFBBF24)
private val SafeColor = Color(0xFF4ADE80)
private val MutedColor = Color(0xFF94A3B8)

// ── Helpers ───────────────────────────────────────────────────────────────────

private fun scamEmoji(scamType: String): String = when {
    scamType.contains("UPI", ignoreCase = true) ||
    scamType.contains("Payment", ignoreCase = true) -> "💸"
    scamType.contains("KYC", ignoreCase = true) ||
    scamType.contains("Bank", ignoreCase = true) -> "🏦"
    scamType.contains("Job", ignoreCase = true) -> "💼"
    scamType.contains("Courier", ignoreCase = true) ||
    scamType.contains("Parcel", ignoreCase = true) -> "📦"
    scamType.contains("Lottery", ignoreCase = true) ||
    scamType.contains("Prize", ignoreCase = true) -> "🎰"
    scamType.contains("Digital Arrest", ignoreCase = true) -> "⚖️"
    scamType.contains("Investment", ignoreCase = true) -> "📈"
    scamType.contains("OTP", ignoreCase = true) -> "🔑"
    scamType.contains("Phishing", ignoreCase = true) -> "🔗"
    scamType.contains("Electricity", ignoreCase = true) ||
    scamType.contains("Utility", ignoreCase = true) -> "⚡"
    scamType.contains("Aadhaar", ignoreCase = true) ||
    scamType.contains("PAN", ignoreCase = true) -> "🪪"
    scamType.contains("Ransomware", ignoreCase = true) ||
    scamType.contains("Malware", ignoreCase = true) -> "🦠"
    else -> "⚠️"
}

private fun timeAgo(publishedAt: String): String {
    return try {
        val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
        sdf.timeZone = TimeZone.getTimeZone("UTC")
        val date = sdf.parse(publishedAt) ?: return publishedAt
        val diffMs = System.currentTimeMillis() - date.time
        val diffMin = diffMs / 60_000
        when {
            diffMin < 60 -> "${diffMin}m ago"
            diffMin < 1440 -> "${diffMin / 60}h ago"
            diffMin < 10080 -> "${diffMin / 1440}d ago"
            else -> "${diffMin / 10080}w ago"
        }
    } catch (e: Exception) {
        publishedAt
    }
}

private fun Int.toLocaleString(): String = String.format("%,d", this)

// ── Screen ────────────────────────────────────────────────────────────────────

@Composable
fun NewsScreen() {
    val scope = rememberCoroutineScope()
    var items by remember { mutableStateOf<List<NewsFeedItem>>(emptyList()) }
    var loading by remember { mutableStateOf(true) }
    var error by remember { mutableStateOf("") }
    var selectedFilter by remember { mutableStateOf("ALL") }

    fun loadNews() {
        scope.launch {
            loading = true
            error = ""
            try {
                items = RetrofitClient.api.getNewsFeed(limit = 50)
            } catch (e: Exception) {
                error = "Could not load news. Check your connection."
            } finally {
                loading = false
            }
        }
    }

    LaunchedEffect(Unit) { loadNews() }

    val filteredItems = remember(items, selectedFilter) {
        when (selectedFilter) {
            "HIGH" -> items.filter { it.severity == "HIGH" }
            "MEDIUM" -> items.filter { it.severity == "MEDIUM" }
            else -> items
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(BgColor)
    ) {
        // Header
        Column(
            modifier = Modifier
                .background(SurfaceColor)
                .padding(horizontal = 16.dp, vertical = 16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        "Cyber Fraud News",
                        fontSize = 22.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(6.dp)
                                .clip(CircleShape)
                                .background(SafeColor)
                        )
                        Spacer(Modifier.width(5.dp))
                        Text(
                            "Live from 8 sources",
                            fontSize = 12.sp,
                            color = MutedColor
                        )
                    }
                }
                IconButton(
                    onClick = { loadNews() },
                    enabled = !loading
                ) {
                    if (loading) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(20.dp),
                            color = PrimaryColor,
                            strokeWidth = 2.dp
                        )
                    } else {
                        Icon(
                            Icons.Default.Refresh,
                            contentDescription = "Refresh",
                            tint = MutedColor
                        )
                    }
                }
            }

            Spacer(Modifier.height(12.dp))

            // Filter chips
            val filters = listOf("ALL", "HIGH", "MEDIUM")
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(filters) { filter ->
                    val selected = selectedFilter == filter
                    val chipColor = when (filter) {
                        "HIGH" -> DangerColor
                        "MEDIUM" -> WarnColor
                        else -> PrimaryColor
                    }
                    Surface(
                        color = if (selected) chipColor.copy(alpha = 0.2f) else Color(0xFF0F172A),
                        shape = RoundedCornerShape(20.dp),
                        modifier = Modifier.clickable { selectedFilter = filter }
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            if (filter != "ALL") {
                                Box(
                                    modifier = Modifier
                                        .size(6.dp)
                                        .clip(CircleShape)
                                        .background(if (selected) chipColor else MutedColor)
                                )
                                Spacer(Modifier.width(5.dp))
                            }
                            Text(
                                filter,
                                fontSize = 12.sp,
                                fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Normal,
                                color = if (selected) chipColor else MutedColor
                            )
                        }
                    }
                }
            }
        }

        // Content
        when {
            loading && items.isEmpty() -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator(color = PrimaryColor)
                        Spacer(Modifier.height(12.dp))
                        Text("Loading latest alerts...", fontSize = 13.sp, color = MutedColor)
                    }
                }
            }

            error.isNotEmpty() && items.isEmpty() -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier.padding(32.dp)
                    ) {
                        Text("📡", fontSize = 48.sp)
                        Spacer(Modifier.height(12.dp))
                        Text(
                            "Connection Error",
                            fontSize = 16.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = Color.White
                        )
                        Spacer(Modifier.height(6.dp))
                        Text(
                            error,
                            fontSize = 13.sp,
                            color = MutedColor,
                            textAlign = androidx.compose.ui.text.style.TextAlign.Center
                        )
                        Spacer(Modifier.height(20.dp))
                        Button(
                            onClick = { loadNews() },
                            colors = ButtonDefaults.buttonColors(containerColor = PrimaryColor),
                            shape = RoundedCornerShape(10.dp)
                        ) {
                            Icon(Icons.Default.Refresh, contentDescription = null, modifier = Modifier.size(16.dp))
                            Spacer(Modifier.width(6.dp))
                            Text("Retry")
                        }
                    }
                }
            }

            filteredItems.isEmpty() -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("🔍", fontSize = 40.sp)
                        Spacer(Modifier.height(10.dp))
                        Text(
                            "No ${selectedFilter.lowercase()} severity alerts",
                            fontSize = 14.sp,
                            color = MutedColor
                        )
                    }
                }
            }

            else -> {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(filteredItems, key = { it.id }) { item ->
                        NewsItemCard(item)
                    }
                }
            }
        }
    }
}

// ── News Item Card ────────────────────────────────────────────────────────────

@Composable
fun NewsItemCard(item: NewsFeedItem) {
    var expanded by remember { mutableStateOf(false) }

    val severityColor = when (item.severity) {
        "HIGH" -> DangerColor
        "MEDIUM" -> WarnColor
        else -> SafeColor
    }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { expanded = !expanded },
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceColor)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {

            // Top row: severity badge + time
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Severity badge with pulsing dot
                Surface(
                    color = severityColor.copy(alpha = 0.12f),
                    shape = RoundedCornerShape(6.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(6.dp)
                                .clip(CircleShape)
                                .background(severityColor)
                        )
                        Spacer(Modifier.width(5.dp))
                        Text(
                            "${item.severity} RISK",
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            color = severityColor
                        )
                    }
                }

                Text(
                    timeAgo(item.publishedAt),
                    fontSize = 11.sp,
                    color = MutedColor
                )
            }

            Spacer(Modifier.height(10.dp))

            // Scam type emoji + type name
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(scamEmoji(item.scamType), fontSize = 16.sp)
                Spacer(Modifier.width(6.dp))
                Text(
                    item.scamType,
                    fontSize = 11.sp,
                    color = PrimaryColor,
                    fontWeight = FontWeight.Medium
                )
            }

            Spacer(Modifier.height(6.dp))

            // Title
            Text(
                item.title,
                fontSize = 15.sp,
                fontWeight = FontWeight.SemiBold,
                color = Color.White,
                lineHeight = 22.sp
            )

            Spacer(Modifier.height(6.dp))

            // Summary (expandable)
            Text(
                item.summary,
                fontSize = 13.sp,
                color = MutedColor,
                lineHeight = 20.sp,
                maxLines = if (expanded) Int.MAX_VALUE else 3,
                overflow = if (expanded) TextOverflow.Clip else TextOverflow.Ellipsis
            )

            if (!expanded && item.summary.length > 120) {
                Text(
                    "Read more",
                    fontSize = 12.sp,
                    color = PrimaryColor,
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.padding(top = 2.dp)
                )
            }

            Spacer(Modifier.height(12.dp))

            // Tags
            if (item.tags.isNotEmpty()) {
                LazyRow(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    items(item.tags.take(3)) { tag ->
                        Surface(
                            color = Color(0xFF0F172A),
                            shape = RoundedCornerShape(6.dp)
                        ) {
                            Text(
                                "#$tag",
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                                fontSize = 10.sp,
                                color = MutedColor
                            )
                        }
                    }
                }
                Spacer(Modifier.height(10.dp))
            }

            // Footer: report count + source
            HorizontalDivider(color = Color(0xFF334155))
            Spacer(Modifier.height(10.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        Icons.Default.Warning,
                        contentDescription = null,
                        modifier = Modifier.size(12.dp),
                        tint = WarnColor
                    )
                    Spacer(Modifier.width(4.dp))
                    Text(
                        "${item.reportCount.toLocaleString()} reports",
                        fontSize = 11.sp,
                        color = WarnColor,
                        fontWeight = FontWeight.Medium
                    )
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        Icons.Default.Source,
                        contentDescription = null,
                        modifier = Modifier.size(12.dp),
                        tint = MutedColor
                    )
                    Spacer(Modifier.width(4.dp))
                    Text(
                        item.slug.take(20),
                        fontSize = 11.sp,
                        color = MutedColor,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        }
    }
}
