package com.suraksha.agent.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.suraksha.agent.data.api.RetrofitClient
import com.suraksha.agent.data.model.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

sealed class AnalyzeUiState {
    object Idle : AnalyzeUiState()
    object Loading : AnalyzeUiState()
    data class MessageResult(val result: AnalysisResult) : AnalyzeUiState()
    data class UrlResult(val result: UrlAnalysisResult) : AnalyzeUiState()
    data class Error(val message: String) : AnalyzeUiState()
}

class AnalyzeViewModel : ViewModel() {

    private val _uiState = MutableStateFlow<AnalyzeUiState>(AnalyzeUiState.Idle)
    val uiState: StateFlow<AnalyzeUiState> = _uiState

    fun analyzeMessage(text: String, language: String = "en") {
        viewModelScope.launch {
            _uiState.value = AnalyzeUiState.Loading
            try {
                val result = RetrofitClient.api.analyzeMessage(
                    AnalyzeMessageRequest(message = text, language = language)
                )
                _uiState.value = AnalyzeUiState.MessageResult(result)
            } catch (e: Exception) {
                _uiState.value = AnalyzeUiState.Error(e.message ?: "Analysis failed")
            }
        }
    }

    fun analyzeUrl(url: String) {
        viewModelScope.launch {
            _uiState.value = AnalyzeUiState.Loading
            try {
                val result = RetrofitClient.api.analyzeUrl(AnalyzeUrlRequest(url = url))
                _uiState.value = AnalyzeUiState.UrlResult(result)
            } catch (e: Exception) {
                _uiState.value = AnalyzeUiState.Error(e.message ?: "URL check failed")
            }
        }
    }

    fun analyzeCall(summary: String, language: String = "en") {
        viewModelScope.launch {
            _uiState.value = AnalyzeUiState.Loading
            try {
                val result = RetrofitClient.api.analyzeCall(
                    AnalyzeCallRequest(summary = summary, language = language)
                )
                _uiState.value = AnalyzeUiState.MessageResult(result)
            } catch (e: Exception) {
                _uiState.value = AnalyzeUiState.Error(e.message ?: "Call analysis failed")
            }
        }
    }

    fun reset() {
        _uiState.value = AnalyzeUiState.Idle
    }
}
