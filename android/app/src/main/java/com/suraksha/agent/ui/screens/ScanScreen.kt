package com.suraksha.agent.ui.screens

import androidx.compose.animation.*
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.suraksha.agent.data.model.AnalysisResult
import com.suraksha.agent.data.model.RiskLevel
import com.suraksha.agent.data.model.UrlAnalysisResult
import com.suraksha.agent.data.model.toRiskLevel
import com.suraksha.agent.ui.viewmodel.AnalyzeUiState
import com.suraksha.agent.ui.viewmodel.AnalyzeViewModel

// ── Constants ─────────────────────────────────────────────────────────────────

private val BgColor = Color(0xFF0F172A)
private val SurfaceColor = Color(0xFF1E293B)
private val PrimaryColor = Color(0xFF3B82F6)
private val DangerColor = Color(0xFFF87171)
private val WarnColor = Color(0xFFFBBF24)
private val SafeColor = Color(0xFF4ADE80)
private val MutedColor = Color(0xFF94A3B8)

enum class ScanTab { MESSAGE, URL, CALL }

private data class SampleChip(val label: String, val text: String)

private val messageSamples = listOf(
    SampleChip(
        "KYC Scam",
        "Dear Customer, Your SBI account KYC is expired. Account will be blocked in 24 hours. Update now: http://sbi-kyc-update.xyz/verify"
    ),
    SampleChip(
        "UPI Fraud",
        "Congratulations! You have received Rs.15,000 in your UPI account. Click to claim: http://upi-reward.tk/claim?ref=WIN2024"
    ),
    SampleChip(
        "Digital Arrest",
        "This is CBI officer Sharma. Your Aadhaar is linked to money laundering case. You are under digital arrest. Call 9876543210 immediately or face arrest."
    ),
    SampleChip(
        "Job Scam",
        "Work from home job! Earn Rs.5000/day by liking YouTube videos. No experience needed. Registration fee Rs.500 only. WhatsApp: 8765432109"
    )
)

private val urlSamples = listOf(
    SampleChip("Phishing Link", "https://sbi-netbanking-secure.xyz/login.php"),
    SampleChip("Fake Bank", "https://hdfc-bank-kyc-update.tk/verify")
)

private val callSamples = listOf(
    SampleChip(
        "CBI Scam",
        "Caller claims to be CBI officer, says my Aadhaar is linked to drug trafficking, demanding Rs.50,000 to avoid arrest"
    ),
    SampleChip(
        "TRAI Notice",
        "Automated call saying my mobile number will be disconnected in 2 hours due to illegal activities, press 9 to speak to officer"
    )
)

// ── Screen ────────────────────────────────────────────────────────────────────

@Composable
fun ScanScreen(vm: AnalyzeViewModel = viewModel()) {
    val uiState by vm.uiState.collectAsStateWithLifecycle()
    var selectedTab by remember { mutableStateOf(ScanTab.MESSAGE) }
    var inputText by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(BgColor)
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        // Header
        Text(
            "Analyze",
            fontSize = 26.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )
        Text(
            "Check messages, URLs and calls for scams",
            fontSize = 13.sp,
            color = MutedColor
        )

        Spacer(Modifier.height(20.dp))

        // Tab row
        val tabs = listOf(
            Triple(ScanTab.MESSAGE, "Message", Icons.Default.Sms),
            Triple(ScanTab.URL, "URL", Icons.Default.Link),
            Triple(ScanTab.CALL, "Call", Icons.Default.Call)
        )
        Surface(
            color = SurfaceColor,
            shape = RoundedCornerShape(14.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(modifier = Modifier.padding(4.dp)) {
                tabs.forEach { (tab, label, icon) ->
                    val selected = selectedTab == tab
                    Surface(
                        color = if (selected) PrimaryColor else Color.Transparent,
                        shape = RoundedCornerShape(10.dp),
                        modifier = Modifier
                            .weight(1f)
                    ) {
                        TextButton(
                            onClick = {
                                selectedTab = tab
                                inputText = ""
                                vm.reset()
                            },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Icon(
                                icon,
                                contentDescription = label,
                                modifier = Modifier.size(16.dp),
                                tint = if (selected) Color.White else MutedColor
                            )
                            Spacer(Modifier.width(6.dp))
                            Text(
                                label,
                                fontSize = 13.sp,
                                fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Normal,
                                color = if (selected) Color.White else MutedColor
                            )
                        }
                    }
                }
            }
        }

        Spacer(Modifier.height(16.dp))

        // Sample chips
        val chips = when (selectedTab) {
            ScanTab.MESSAGE -> messageSamples
            ScanTab.URL -> urlSamples
            ScanTab.CALL -> callSamples
        }
        Row(
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            chips.forEach { chip ->
                SuggestionChip(
                    onClick = { inputText = chip.text },
                    label = {
                        Text(chip.label, fontSize = 11.sp, maxLines = 1)
                    },
                    colors = SuggestionChipDefaults.suggestionChipColors(
                        containerColor = SurfaceColor,
                        labelColor = MutedColor
                    ),
                    border = SuggestionChipDefaults.suggestionChipBorder(
                        enabled = true,
                        borderColor = Color(0xFF334155)
                    )
                )
            }
        }

        Spacer(Modifier.height(12.dp))

        // Input field
        OutlinedTextField(
            value = inputText,
            onValueChange = { inputText = it },
            modifier = Modifier.fillMaxWidth(),
            placeholder = {
                Text(
                    when (selectedTab) {
                        ScanTab.MESSAGE -> "Paste suspicious SMS or message here..."
                        ScanTab.URL -> "Paste suspicious URL here..."
                        ScanTab.CALL -> "Describe the suspicious call in detail..."
                    },
                    fontSize = 13.sp,
                    color = MutedColor
                )
            },
            minLines = if (selectedTab == ScanTab.URL) 2 else 5,
            maxLines = 12,
            shape = RoundedCornerShape(12.dp),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = PrimaryColor,
                unfocusedBorderColor = Color(0xFF334155),
                focusedContainerColor = SurfaceColor,
                unfocusedContainerColor = SurfaceColor,
                focusedTextColor = Color.White,
                unfocusedTextColor = Color.White,
                cursorColor = PrimaryColor
            )
        )

        Spacer(Modifier.height(6.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(
                Icons.Default.Lock,
                contentDescription = null,
                modifier = Modifier.size(12.dp),
                tint = SafeColor
            )
            Spacer(Modifier.width(4.dp))
            Text(
                "PAN, Aadhaar & phone masked before analysis",
                fontSize = 11.sp,
                color = SafeColor
            )
        }

        Spacer(Modifier.height(14.dp))

        // Analyze button
        Button(
            onClick = {
                when (selectedTab) {
                    ScanTab.MESSAGE -> vm.analyzeMessage(inputText)
                    ScanTab.URL -> vm.analyzeUrl(inputText)
                    ScanTab.CALL -> vm.analyzeCall(inputText)
                }
            },
            enabled = inputText.isNotBlank() && uiState !is AnalyzeUiState.Loading,
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp),
            shape = RoundedCornerShape(14.dp),
            colors = ButtonDefaults.buttonColors(containerColor = PrimaryColor)
        ) {
            if (uiState is AnalyzeUiState.Loading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    color = Color.White,
                    strokeWidth = 2.dp
                )
                Spacer(Modifier.width(10.dp))
                Text("Analyzing...", fontWeight = FontWeight.SemiBold, color = Color.White)
            } else {
                Icon(Icons.Default.Security, contentDescription = null, tint = Color.White)
                Spacer(Modifier.width(8.dp))
                Text("Analyze", fontWeight = FontWeight.SemiBold, color = Color.White)
            }
        }

        Spacer(Modifier.height(24.dp))

        // Results
        AnimatedVisibility(
            visible = uiState !is AnalyzeUiState.Idle && uiState !is AnalyzeUiState.Loading,
            enter = fadeIn() + slideInVertically(),
            exit = fadeOut()
        ) {
            when (val state = uiState) {
                is AnalyzeUiState.MessageResult -> MessageResultCard(state.result)
                is AnalyzeUiState.UrlResult -> UrlResultCard(state.result)
                is AnalyzeUiState.Error -> ErrorCard(state.message)
                else -> {}
            }
        }
    }
}

// ── Message Result Card ───────────────────────────────────────────────────────

@Composable
fun MessageResultCard(result: AnalysisResult) {
    val riskLevel = result.riskLevel.toRiskLevel()
    val (accentColor, bgColor, badgeLabel, badgeEmoji) = when (riskLevel) {
        RiskLevel.HIGH_RISK -> listOf(DangerColor, Color(0xFF450A0A), "HIGH RISK", "🔴")
        RiskLevel.SUSPICIOUS -> listOf(WarnColor, Color(0xFF451A03), "SUSPICIOUS", "⚠️")
        RiskLevel.SAFE -> listOf(SafeColor, Color(0xFF052E16), "SAFE", "✅")
    }

    var evidenceExpanded by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceColor)
    ) {
        Column(modifier = Modifier.padding(20.dp)) {

            // Risk badge + score row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Badge
                Surface(
                    color = (accentColor as Color).copy(alpha = 0.15f),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(badgeEmoji as String, fontSize = 16.sp)
                        Spacer(Modifier.width(6.dp))
                        Text(
                            badgeLabel as String,
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Bold,
                            color = accentColor
                        )
                    }
                }

                // Score circle
                Box(
                    modifier = Modifier
                        .size(56.dp)
                        .clip(CircleShape)
                        .background(accentColor.copy(alpha = 0.15f)),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            "${result.riskScore}",
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold,
                            color = accentColor
                        )
                        Text("/100", fontSize = 9.sp, color = MutedColor)
                    }
                }
            }

            Spacer(Modifier.height(12.dp))

            // Scam type
            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(
                    color = Color(0xFF1E3A5F),
                    shape = RoundedCornerShape(6.dp)
                ) {
                    Text(
                        result.scamType,
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium,
                        color = PrimaryColor
                    )
                }
            }

            HorizontalDivider(
                modifier = Modifier.padding(vertical = 16.dp),
                color = Color(0xFF334155)
            )

            // Risk breakdown bars
            val breakdown = result.scoreBreakdown
            Text(
                "Risk Breakdown",
                fontSize = 13.sp,
                fontWeight = FontWeight.SemiBold,
                color = Color.White
            )
            Spacer(Modifier.height(10.dp))
            RiskBar("Urgency", breakdown.urgencyScore, 25, WarnColor)
            Spacer(Modifier.height(6.dp))
            RiskBar("Authority", breakdown.authorityScore, 25, DangerColor)
            Spacer(Modifier.height(6.dp))
            RiskBar("Payment", breakdown.paymentScore, 25, Color(0xFFA78BFA))
            Spacer(Modifier.height(6.dp))
            RiskBar("Deception", breakdown.deceptionScore, 25, Color(0xFFFB923C))

            HorizontalDivider(
                modifier = Modifier.padding(vertical = 16.dp),
                color = Color(0xFF334155)
            )

            // Why it's risky
            if (result.whyRisky.isNotEmpty()) {
                Text(
                    "⚠️ Why it's risky",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = Color.White
                )
                Spacer(Modifier.height(6.dp))
                Text(
                    result.whyRisky,
                    fontSize = 13.sp,
                    color = MutedColor,
                    lineHeight = 20.sp
                )
                Spacer(Modifier.height(14.dp))
            }

            // Evidence chain (collapsible)
            if (result.redFlags.isNotEmpty()) {
                Surface(
                    color = Color(0xFF1A0A0A),
                    shape = RoundedCornerShape(10.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                "🔗 Evidence Chain",
                                fontSize = 13.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = DangerColor
                            )
                            TextButton(
                                onClick = { evidenceExpanded = !evidenceExpanded },
                                contentPadding = PaddingValues(0.dp)
                            ) {
                                Text(
                                    if (evidenceExpanded) "Hide" else "Show ${result.redFlags.size}",
                                    fontSize = 12.sp,
                                    color = MutedColor
                                )
                                Icon(
                                    if (evidenceExpanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp),
                                    tint = MutedColor
                                )
                            }
                        }
                        AnimatedVisibility(visible = evidenceExpanded) {
                            Column(modifier = Modifier.padding(top = 8.dp)) {
                                result.redFlags.forEach { flag ->
                                    Row(
                                        modifier = Modifier.padding(vertical = 3.dp),
                                        verticalAlignment = Alignment.Top
                                    ) {
                                        Text("🚩", fontSize = 12.sp)
                                        Spacer(Modifier.width(6.dp))
                                        Text(
                                            flag,
                                            fontSize = 12.sp,
                                            color = Color(0xFFFCA5A5),
                                            lineHeight = 18.sp
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
                Spacer(Modifier.height(14.dp))
            }

            // Do NOT list
            if (result.whatNotToDo.isNotEmpty()) {
                Text(
                    "❌ Do NOT",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = DangerColor
                )
                Spacer(Modifier.height(6.dp))
                result.whatNotToDo.forEach { action ->
                    Row(
                        modifier = Modifier.padding(vertical = 2.dp),
                        verticalAlignment = Alignment.Top
                    ) {
                        Text("•", fontSize = 13.sp, color = DangerColor)
                        Spacer(Modifier.width(6.dp))
                        Text(action, fontSize = 13.sp, color = MutedColor, lineHeight = 19.sp)
                    }
                }
                Spacer(Modifier.height(14.dp))
            }

            // What to do list
            if (result.whatToDo.isNotEmpty()) {
                Text(
                    "✅ What to do",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = SafeColor
                )
                Spacer(Modifier.height(6.dp))
                result.whatToDo.forEach { action ->
                    Row(
                        modifier = Modifier.padding(vertical = 2.dp),
                        verticalAlignment = Alignment.Top
                    ) {
                        Text("•", fontSize = 13.sp, color = SafeColor)
                        Spacer(Modifier.width(6.dp))
                        Text(action, fontSize = 13.sp, color = MutedColor, lineHeight = 19.sp)
                    }
                }
            }
        }
    }
}

@Composable
private fun RiskBar(label: String, score: Int, maxScore: Int, color: Color) {
    val fraction = (score.coerceIn(0, maxScore).toFloat() / maxScore.toFloat())
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            label,
            fontSize = 12.sp,
            color = MutedColor,
            modifier = Modifier.width(72.dp)
        )
        Spacer(Modifier.width(8.dp))
        Box(
            modifier = Modifier
                .weight(1f)
                .height(6.dp)
                .clip(RoundedCornerShape(3.dp))
                .background(Color(0xFF334155))
        ) {
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth(fraction)
                    .clip(RoundedCornerShape(3.dp))
                    .background(color)
            )
        }
        Spacer(Modifier.width(8.dp))
        Text(
            "$score/$maxScore",
            fontSize = 11.sp,
            color = color,
            modifier = Modifier.width(36.dp)
        )
    }
}

// ── URL Result Card ───────────────────────────────────────────────────────────

@Composable
fun UrlResultCard(result: UrlAnalysisResult) {
    val riskLevel = result.riskLevel.toRiskLevel()
    val (accentColor, badgeLabel, badgeEmoji) = when (riskLevel) {
        RiskLevel.HIGH_RISK -> Triple(DangerColor, "HIGH RISK", "🔴")
        RiskLevel.SUSPICIOUS -> Triple(WarnColor, "SUSPICIOUS", "⚠️")
        RiskLevel.SAFE -> Triple(SafeColor, "SAFE", "✅")
    }

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceColor)
    ) {
        Column(modifier = Modifier.padding(20.dp)) {

            // Badge + score
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    color = accentColor.copy(alpha = 0.15f),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(badgeEmoji, fontSize = 16.sp)
                        Spacer(Modifier.width(6.dp))
                        Text(
                            badgeLabel,
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Bold,
                            color = accentColor
                        )
                    }
                }
                Text(
                    "${result.riskScore}/100",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = accentColor
                )
            }

            Spacer(Modifier.height(12.dp))

            // URL display
            Surface(
                color = Color(0xFF0F172A),
                shape = RoundedCornerShape(8.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    result.url,
                    modifier = Modifier.padding(10.dp),
                    fontSize = 12.sp,
                    color = MutedColor,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }

            // Brand impersonation warning
            if (result.isBrandImpersonation && result.impersonatedBrand != null) {
                Spacer(Modifier.height(12.dp))
                Surface(
                    color = Color(0xFF451A03),
                    shape = RoundedCornerShape(10.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("🏦", fontSize = 18.sp)
                        Spacer(Modifier.width(8.dp))
                        Column {
                            Text(
                                "Brand Impersonation Detected",
                                fontSize = 13.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = WarnColor
                            )
                            Text(
                                "Pretending to be: ${result.impersonatedBrand}",
                                fontSize = 12.sp,
                                color = MutedColor
                            )
                        }
                    }
                }
            }

            HorizontalDivider(
                modifier = Modifier.padding(vertical = 14.dp),
                color = Color(0xFF334155)
            )

            // Threats
            if (result.threats.isNotEmpty()) {
                Text(
                    "🚩 Threats Detected",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = Color.White
                )
                Spacer(Modifier.height(8.dp))
                result.threats.forEach { threat ->
                    Row(
                        modifier = Modifier.padding(vertical = 3.dp),
                        verticalAlignment = Alignment.Top
                    ) {
                        Box(
                            modifier = Modifier
                                .padding(top = 5.dp)
                                .size(6.dp)
                                .clip(CircleShape)
                                .background(DangerColor)
                        )
                        Spacer(Modifier.width(8.dp))
                        Text(threat, fontSize = 13.sp, color = MutedColor, lineHeight = 19.sp)
                    }
                }
                Spacer(Modifier.height(12.dp))
            }

            // Domain age
            if (result.domainAgeDays != null) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        Icons.Default.Schedule,
                        contentDescription = null,
                        modifier = Modifier.size(14.dp),
                        tint = MutedColor
                    )
                    Spacer(Modifier.width(6.dp))
                    Text(
                        "Domain age: ${result.domainAgeDays} days",
                        fontSize = 12.sp,
                        color = if (result.domainAgeDays < 30) WarnColor else MutedColor
                    )
                }
                Spacer(Modifier.height(8.dp))
            }

            // Safe browsing flag
            if (result.safeBrowsingFlagged) {
                Surface(
                    color = Color(0xFF450A0A),
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.GppBad,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp),
                            tint = DangerColor
                        )
                        Spacer(Modifier.width(8.dp))
                        Text(
                            "Flagged by Google Safe Browsing",
                            fontSize = 12.sp,
                            color = DangerColor,
                            fontWeight = FontWeight.Medium
                        )
                    }
                }
                Spacer(Modifier.height(10.dp))
            }

            // Recommendation
            if (result.recommendation.isNotEmpty()) {
                HorizontalDivider(color = Color(0xFF334155))
                Spacer(Modifier.height(12.dp))
                Text(
                    "💡 Recommendation",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = Color.White
                )
                Spacer(Modifier.height(6.dp))
                Text(result.recommendation, fontSize = 13.sp, color = MutedColor, lineHeight = 20.sp)
            }
        }
    }
}

// ── Error Card ────────────────────────────────────────────────────────────────

@Composable
fun ErrorCard(message: String) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF1C0A0A))
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(CircleShape)
                    .background(DangerColor.copy(alpha = 0.15f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    Icons.Default.Error,
                    contentDescription = null,
                    tint = DangerColor,
                    modifier = Modifier.size(20.dp)
                )
            }
            Spacer(Modifier.width(12.dp))
            Column {
                Text(
                    "Analysis Failed",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = DangerColor
                )
                Text(
                    message,
                    fontSize = 12.sp,
                    color = MutedColor,
                    lineHeight = 18.sp
                )
            }
        }
    }
}
