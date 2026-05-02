package com.suraksha.agent.data.api

import com.suraksha.agent.data.model.*
import retrofit2.http.*

interface SurakshaApi {

    @POST("analyze/message")
    suspend fun analyzeMessage(@Body request: AnalyzeMessageRequest): AnalysisResult

    @POST("analyze/url")
    suspend fun analyzeUrl(@Body request: AnalyzeUrlRequest): UrlAnalysisResult

    @POST("analyze/call")
    suspend fun analyzeCall(@Body request: AnalyzeCallRequest): AnalysisResult

    @GET("news-feed/")
    suspend fun getNewsFeed(
        @Query("limit") limit: Int = 10,
    ): List<NewsFeedItem>

    @POST("report-scam/")
    suspend fun reportScam(@Body request: ReportScamRequest): ReportScamResponse

    @GET("health")
    suspend fun healthCheck(): Map<String, String>
}
