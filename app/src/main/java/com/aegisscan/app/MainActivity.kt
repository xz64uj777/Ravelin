/*
 * Ravelin
 * Copyright (c) 2026 Kyle. All rights reserved.
 * Build ID: RAVELIN-KYLE-2026-V40
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

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    companion object {
        const val BUNDLED = "file:///android_asset/index.html"
        const val LIVE =
            "https://raw.githubusercontent.com/xz64uj777/Ravelin/main/Ravelin.html"
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
            webView.loadUrl(BUNDLED)
        }
    }

    inner class RavelinBridge {
        @JavascriptInterface
        fun reloadLive(url: String) {
            val target = if (url.isBlank()) LIVE else url
            runOnUiThread {
                webView.settings.cacheMode = WebSettings.LOAD_NO_CACHE
                webView.clearCache(true)
                val sep = if (target.contains("?")) "&" else "?"
                webView.loadUrl(target + sep + "t=" + System.currentTimeMillis())
            }
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
            if (html.length < 2000) return
            runOnUiThread {
                webView.settings.cacheMode = WebSettings.LOAD_NO_CACHE
                webView.loadDataWithBaseURL(
                    "https://raw.githubusercontent.com/xz64uj777/Ravelin/main/",
                    html,
                    "text/html",
                    "UTF-8",
                    null
                )
            }
        }

        @JavascriptInterface
        fun apkVersion(): String = "40"
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
