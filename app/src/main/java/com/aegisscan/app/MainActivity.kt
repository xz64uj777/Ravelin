/*
 * Ravelin
 * Copyright (c) 2026 Kyle. All rights reserved.
 * Build ID: RAVELIN-KYLE-2026-V41
 */
package com.aegisscan.app

import android.annotation.SuppressLint
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import java.io.File

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    companion object {
        const val BUNDLED = "file:///android_asset/index.html"
        const val LIVE =
            "https://raw.githubusercontent.com/xz64uj777/Ravelin/main/Ravelin.html"
        const val REMOTE_BASE =
            "https://raw.githubusercontent.com/xz64uj777/Ravelin/main/"
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        title = "Ravelin © Kyle"
        webView = WebView(this)
        setContentView(webView)

        val settings: WebSettings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.databaseEnabled = true
        settings.allowFileAccess = true
        settings.allowContentAccess = true
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        settings.mixedContentMode = WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
        settings.mediaPlaybackRequiresUserGesture = false

        webView.addJavascriptInterface(RavelinBridge(), "RavelinNative")
        webView.webChromeClient = WebChromeClient()
        webView.webViewClient = WebViewClient()

        if (savedInstanceState != null) {
            webView.restoreState(savedInstanceState)
        } else {
            openBestConsole()
        }
    }

    private fun cachedConsole(): File = File(filesDir, "console.html")

    private fun openBestConsole() {
        val cached = cachedConsole()
        if (cached.exists() && cached.length() > 20000L) {
            webView.loadUrl("file://" + cached.absolutePath)
        } else {
            webView.loadUrl(BUNDLED)
        }
    }

    inner class RavelinBridge {
        @JavascriptInterface
        fun reloadLive(url: String) {
            runOnUiThread { openBestConsole() }
        }

        @JavascriptInterface
        fun reloadBundled() {
            runOnUiThread {
                webView.settings.cacheMode = WebSettings.LOAD_DEFAULT
                webView.loadUrl(BUNDLED)
            }
        }

        @JavascriptInterface
        fun applyHtml(html: String) {
            if (html.length < 20000) return
            try {
                cachedConsole().writeText(html, Charsets.UTF_8)
            } catch (_: Exception) {
            }
            runOnUiThread {
                webView.settings.cacheMode = WebSettings.LOAD_NO_CACHE
                webView.loadDataWithBaseURL(
                    REMOTE_BASE,
                    html,
                    "text/html",
                    "UTF-8",
                    null
                )
            }
        }

        @JavascriptInterface
        fun apkVersion(): String = "41"
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        webView.saveState(outState)
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        if (this::webView.isInitialized && webView.canGoBack()) {
            webView.goBack()
        } else {
            @Suppress("DEPRECATION")
            super.onBackPressed()
        }
    }
}
