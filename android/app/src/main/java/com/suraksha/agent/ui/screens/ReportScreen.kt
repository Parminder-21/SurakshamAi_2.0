package com.suraksha.agent.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.suraksha.agent.data.api.RetrofitClient
import com.suraksha.agent.data.model.ReportScamRequest
import kotlinx.coroutines.launch

// ── Constants ─────────────────────────────────────────────────────────────────

private val BgColor = Color(0xFF0F172A)
private val SurfaceColor = Color(0xFF1E293B)
private val PrimaryColor = Color(0xFF3B82F6)
private val DangerColor = Color(0xFFF87171)
private val SafeColor = Color(0xFF4ADE80)
private val MutedColor = Color(0xFF94A3B8)

private val scamTypes = listOf(
    "UPI Fraud",
    "Fake KYC",
    "Digital Arrest",
    "Job Fraud",
    "Courier Scam",
    "Investment Scam",
    "OTP Fraud",
    "Phishing",
    "Other"
)

private fun scamTypeEmoji(type: String): String = when (type) {
    "UPI Fraud" -> "💸"
    "Fake KYC" -> "🏦"
    "Digital Arrest" -> "⚖️"
    "Job Fraud" -> "💼"
    "Courier Scam" -> "📦"
    "Investment Scam" -> "📈"
    "OTP Fraud" -> "🔑"
    "Phishing" -> "🔗"
    else -> "⚠️"
}

// ── Screen ────────────────────────────────────────────────────────────────────

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReportScreen() {
    val scope = rememberCoroutineScope()

    var selectedScamType by remember { mutableStateOf("") }
    var content by remember { mutableStateOf("") }
    var note by remember { mutableStateOf("") }
    var loading by remember { mutableStateOf(false) }
    var success by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf("") }
    var dropdownExpanded by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        // Header
        Row(verticalAlignment = Alignment.CenterVertically) {
            Surface(
                color = PrimaryColor.copy(alpha = 0.15f),
                shape = androidx.compose.foundation.shape.CircleShape
            ) {
                Icon(
                    Icons.Default.Shield,
                    contentDescription = null,
                    modifier = Modifier
                        .padding(10.dp)
                        .size(24.dp),
                    tint = PrimaryColor
                )
            }
            Spacer(Modifier.width(12.dp))
            Column {
                Text(
                    "Report a Scam",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                Text(
                    "Help protect others in India",
                    fontSize = 13.sp,
                    color = MutedColor
                )
            }
        }

        Spacer(Modifier.height(24.dp))

        if (success) {
            SuccessState(
                onReportAnother = {
                    success = false
                    content = ""
                    note = ""
                    selectedScamType = ""
                    error = ""
                }
            )
        } else {
            // Scam type selector
            Text(
                "Scam Type",
                fontSize = 13.sp,
                fontWeight = FontWeight.Medium,
                color = Color.White
            )
            Spacer(Modifier.height(8.dp))

            ExposedDropdownMenuBox(
                expanded = dropdownExpanded,
                onExpandedChange = { dropdownExpanded = it }
            ) {
                OutlinedTextField(
                    value = if (selectedScamType.isEmpty()) "" else "${scamTypeEmoji(selectedScamType)}  $selectedScamType",
                    onValueChange = {},
                    readOnly = true,
                    modifier = Modifier
                        .fillMaxWidth()
                        .menuAnchor(),
                    placeholder = {
                        Text("Select scam type...", fontSize = 13.sp, color = MutedColor)
                    },
                    trailingIcon = {
                        ExposedDropdownMenuDefaults.TrailingIcon(expanded = dropdownExpanded)
                    },
                    shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = PrimaryColor,
                        unfocusedBorderColor = Color(0xFF334155),
                        focusedContainerColor = SurfaceColor,
                        unfocusedContainerColor = SurfaceColor,
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White
                    )
                )
                ExposedDropdownMenu(
                    expanded = dropdownExpanded,
                    onDismissRequest = { dropdownExpanded = false },
                    modifier = Modifier.exposedDropdownSize()
                ) {
                    scamTypes.forEach { type ->
                        DropdownMenuItem(
                            text = {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Text(scamTypeEmoji(type), fontSize = 16.sp)
                                    Spacer(Modifier.width(10.dp))
                                    Text(type, fontSize = 14.sp)
                                }
                            },
                            onClick = {
                                selectedScamType = type
                                dropdownExpanded = false
                            }
                        )
                    }
                }
            }

            Spacer(Modifier.height(18.dp))

            // Scam content input
            Text(
                "Scam Content *",
                fontSize = 13.sp,
                fontWeight = FontWeight.Medium,
                color = Color.White
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = content,
                onValueChange = { content = it },
                modifier = Modifier.fillMaxWidth(),
                placeholder = {
                    Text(
                        "Paste the scam message, URL, or describe the call...",
                        fontSize = 13.sp,
                        color = MutedColor
                    )
                },
                minLines = 5,
                maxLines = 12,
                shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp),
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
                    "PAN, Aadhaar & phone numbers are masked before storage",
                    fontSize = 11.sp,
                    color = SafeColor
                )
            }

            Spacer(Modifier.height(18.dp))

            // Notes input
            Text(
                "Additional Notes",
                fontSize = 13.sp,
                fontWeight = FontWeight.Medium,
                color = Color.White
            )
            Spacer(Modifier.height(4.dp))
            Text(
                "Optional — add context about how you received this",
                fontSize = 11.sp,
                color = MutedColor
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = note,
                onValueChange = { note = it },
                modifier = Modifier.fillMaxWidth(),
                placeholder = {
                    Text(
                        "e.g. Received via WhatsApp, caller had foreign accent...",
                        fontSize = 13.sp,
                        color = MutedColor
                    )
                },
                minLines = 3,
                maxLines = 6,
                shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp),
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

            // Error message
            if (error.isNotEmpty()) {
                Spacer(Modifier.height(12.dp))
                Surface(
                    color = Color(0xFF1C0A0A),
                    shape = androidx.compose.foundation.shape.RoundedCornerShape(10.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.Error,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp),
                            tint = DangerColor
                        )
                        Spacer(Modifier.width(8.dp))
                        Text(error, fontSize = 13.sp, color = DangerColor)
                    }
                }
            }

            Spacer(Modifier.height(24.dp))

            // Submit button
            Button(
                onClick = {
                    scope.launch {
                        loading = true
                        error = ""
                        try {
                            RetrofitClient.api.reportScam(
                                ReportScamRequest(
                                    content = content,
                                    scamType = selectedScamType.ifBlank { null },
                                    reporterNote = note.ifBlank { null }
                                )
                            )
                            success = true
                        } catch (e: Exception) {
                            error = e.message ?: "Submission failed. Please try again."
                        } finally {
                            loading = false
                        }
                    }
                },
                enabled = content.isNotBlank() && !loading,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(14.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PrimaryColor)
            ) {
                if (loading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(20.dp),
                        color = Color.White,
                        strokeWidth = 2.dp
                    )
                    Spacer(Modifier.width(10.dp))
                    Text("Submitting...", fontWeight = FontWeight.SemiBold, color = Color.White)
                } else {
                    Icon(Icons.Default.Send, contentDescription = null, tint = Color.White)
                    Spacer(Modifier.width(8.dp))
                    Text("Submit Report", fontWeight = FontWeight.SemiBold, color = Color.White)
                }
            }

            Spacer(Modifier.height(12.dp))

            // Disclaimer
            Text(
                "Reports are reviewed by our team and used to improve scam detection for everyone.",
                fontSize = 11.sp,
                color = MutedColor,
                lineHeight = 16.sp
            )
        }
    }
}

// ── Success State ─────────────────────────────────────────────────────────────

@Composable
private fun SuccessState(onReportAnother: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceColor)
    ) {
        Column(
            modifier = Modifier
                .padding(32.dp)
                .fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Surface(
                color = SafeColor.copy(alpha = 0.15f),
                shape = androidx.compose.foundation.shape.CircleShape
            ) {
                Icon(
                    Icons.Default.CheckCircle,
                    contentDescription = null,
                    tint = SafeColor,
                    modifier = Modifier
                        .padding(16.dp)
                        .size(40.dp)
                )
            }

            Spacer(Modifier.height(16.dp))

            Text(
                "Report Submitted!",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )

            Spacer(Modifier.height(8.dp))

            Text(
                "Thank you for helping protect others. Your report has been received and will be reviewed by our team.",
                fontSize = 13.sp,
                color = MutedColor,
                lineHeight = 20.sp,
                textAlign = androidx.compose.ui.text.style.TextAlign.Center
            )

            Spacer(Modifier.height(8.dp))

            Surface(
                color = PrimaryColor.copy(alpha = 0.1f),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(10.dp)
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("🛡️", fontSize = 16.sp)
                    Spacer(Modifier.width(8.dp))
                    Text(
                        "Your report helps train our AI to detect similar scams",
                        fontSize = 12.sp,
                        color = PrimaryColor,
                        lineHeight = 18.sp
                    )
                }
            }

            Spacer(Modifier.height(24.dp))

            OutlinedButton(
                onClick = onReportAnother,
                modifier = Modifier.fillMaxWidth(),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp),
                colors = ButtonDefaults.outlinedButtonColors(contentColor = PrimaryColor),
                border = ButtonDefaults.outlinedButtonBorder
            ) {
                Icon(Icons.Default.Add, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(Modifier.width(6.dp))
                Text("Report Another Scam", fontWeight = FontWeight.Medium)
            }
        }
    }
}
