package com.suraksha.agent

import android.Manifest
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.suraksha.agent.scanner.PermissionManager
import com.suraksha.agent.scanner.ScanNotificationHelper
import com.suraksha.agent.ui.screens.*
import com.suraksha.agent.ui.theme.SurakshaTheme

sealed class Screen(val route: String, val label: String) {
    object Home       : Screen("home", "Home")
    object Scan       : Screen("scan", "Scan")
    object Shield     : Screen("shield", "Shield")
    object History    : Screen("history", "History")
    object News       : Screen("news", "News")
    object Report     : Screen("report", "Report")
}

val bottomNavItems = listOf(
    Screen.Home    to Icons.Default.Home,
    Screen.Scan    to Icons.Default.Search,
    Screen.Shield  to Icons.Default.Shield,
    Screen.History to Icons.Default.History,
    Screen.News    to Icons.Default.Newspaper,
)

class MainActivity : ComponentActivity() {

    // Permission launcher — requests all scanner permissions on first launch
    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions(),
    ) { results ->
        val allGranted = results.values.all { it }
        if (allGranted) {
            // All permissions granted — start background scanner
            PermissionManager.startScannerService(this)
        }
        // Even if denied, app works for manual scanning
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        // Create notification channels
        ScanNotificationHelper.createChannels(this)

        // Request permissions on first launch
        requestScannerPermissions()

        setContent {
            SurakshaTheme {
                SurakshaApp()
            }
        }
    }

    private fun requestScannerPermissions() {
        val permissions = buildList {
            add(Manifest.permission.RECEIVE_SMS)
            add(Manifest.permission.READ_SMS)
            add(Manifest.permission.READ_PHONE_STATE)
            add(Manifest.permission.READ_CALL_LOG)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                add(Manifest.permission.POST_NOTIFICATIONS)
            }
        }.toTypedArray()

        val missing = PermissionManager.getMissingPermissions(this)
        if (missing.isNotEmpty()) {
            permissionLauncher.launch(permissions)
        } else {
            // Already have all permissions — start scanner
            PermissionManager.startScannerService(this)
        }
    }
}

@Composable
fun SurakshaApp() {
    val navController = rememberNavController()
    val currentBackStack by navController.currentBackStackEntryAsState()
    val currentRoute = currentBackStack?.destination?.route

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        bottomBar = {
            NavigationBar {
                bottomNavItems.forEach { (screen, icon) ->
                    NavigationBarItem(
                        icon = { Icon(icon, contentDescription = screen.label) },
                        label = { Text(screen.label) },
                        selected = currentRoute == screen.route,
                        onClick = {
                            navController.navigate(screen.route) {
                                popUpTo(Screen.Home.route) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Home.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Screen.Home.route) {
                HomeScreen(
                    onNavigateToScan = { navController.navigate(Screen.Scan.route) },
                    onNavigateToNews = { navController.navigate(Screen.News.route) },
                    onNavigateToReport = { navController.navigate(Screen.Report.route) }
                ) {
                    navController.navigate(Screen.Shield.route)
                }
            }
            composable(Screen.Scan.route)    { ScanScreen() }
            composable(Screen.Shield.route)  { PermissionScreen() }
            composable(Screen.History.route) { HistoryScreen() }
            composable(Screen.News.route)    { NewsScreen() }
            composable(Screen.Report.route)  { ReportScreen() }
        }
    }
}
