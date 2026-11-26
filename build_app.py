#!/usr/bin/env python3
"""Self-contained builder for Platen — Paper & Ink Android APK (By Abbas Ebrahimi)."""
import os, math
from PIL import Image, ImageDraw

def wf(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

def make_vintage_icon():
    S = 1024
    img = Image.new("RGBA", (S, S), (22, 16, 12, 255))
    dr = ImageDraw.Draw(img)
    cx, cy = S // 2, S // 2

    for r in range(512, 0, -4):
        t = r / 512.0
        col = (int(58 - 36 * t), int(38 - 22 * t), int(24 - 13 * t), 255)
        dr.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)

    dr.ellipse((78, 78, S - 78, S - 78), fill=(72, 42, 24, 255), outline=(212, 166, 92, 255), width=14)
    dr.ellipse((114, 114, S - 114, S - 114), outline=(186, 138, 66, 210), width=5)
    dr.ellipse((136, 136, S - 136, S - 136), fill=(40, 24, 15, 255), outline=(224, 182, 108, 170), width=3)

    for i in range(24):
        a = math.radians(i * 15)
        rx = cx + int(386 * math.cos(a))
        ry = cy + int(386 * math.sin(a))
        rad = 8 if i % 6 == 0 else 4
        dr.ellipse((rx - rad, ry - rad, rx + rad, ry + rad), fill=(235, 194, 118, 255))

    dr.rounded_rectangle((310, 200, 714, 570), radius=34, fill=(246, 236, 212, 255), outline=(188, 162, 120, 255), width=5)
    dr.rectangle((316, 480, 708, 560), fill=(224, 210, 180, 255))
    for i, w_ln in enumerate([280, 320, 250, 295, 190]):
        y = 262 + i * 38
        dr.rounded_rectangle((360, y, 360 + w_ln, y + 10), radius=5, fill=(76, 58, 40, 190))

    dr.rounded_rectangle((226, 520, 798, 668), radius=48, fill=(24, 68, 48, 255), outline=(218, 174, 96, 255), width=8)
    dr.rounded_rectangle((250, 542, 774, 572), radius=14, fill=(68, 128, 96, 160))
    dr.rounded_rectangle((250, 628, 774, 654), radius=12, fill=(14, 42, 30, 180))

    dr.rounded_rectangle((176, 544, 234, 644), radius=16, fill=(198, 152, 76, 255), outline=(244, 212, 142, 255), width=5)
    dr.rounded_rectangle((790, 544, 848, 644), radius=16, fill=(198, 152, 76, 255), outline=(244, 212, 142, 255), width=5)

    dr.rounded_rectangle((246, 492, 778, 514), radius=10, fill=(226, 182, 102, 255), outline=(120, 84, 34, 255), width=3)
    dr.rounded_rectangle((368, 482, 412, 524), radius=8, fill=(32, 82, 58, 255), outline=(232, 192, 114, 255), width=4)
    dr.rounded_rectangle((612, 482, 656, 524), radius=8, fill=(32, 82, 58, 255), outline=(232, 192, 114, 255), width=4)

    dr.polygon([(512, 792), (454, 668), (512, 622), (570, 668)], fill=(232, 190, 112, 255), outline=(112, 78, 30, 255))
    dr.line([(512, 782), (512, 680)], fill=(48, 32, 18, 255), width=6)
    dr.ellipse((498, 668, 526, 696), fill=(48, 32, 18, 255))

    fg = Image.new("RGBA", (432, 432), (22, 16, 12, 255))
    inner = img.resize((324, 324), Image.Resampling.LANCZOS)
    fg.paste(inner, (54, 54), inner)
    os.makedirs("app/src/main/res/drawable-nodpi", exist_ok=True)
    fg.save("app/src/main/res/drawable-nodpi/ic_launcher_foreground.png", "PNG")

    for folder, px in [("mipmap-mdpi", 48), ("mipmap-hdpi", 72), ("mipmap-xhdpi", 96), ("mipmap-xxhdpi", 144), ("mipmap-xxxhdpi", 192)]:
        d = f"app/src/main/res/{folder}"
        os.makedirs(d, exist_ok=True)
        sq = img.resize((px, px), Image.Resampling.LANCZOS)
        sq.save(f"{d}/ic_launcher.png", "PNG")
        mask = Image.new("L", (px, px), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, px - 1, px - 1), fill=255)
        rnd = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        rnd.paste(sq, (0, 0), mask)
        rnd.save(f"{d}/ic_launcher_round.png", "PNG")

wf("settings.gradle.kts", '''pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name = "PlatenPaperAndInk"
include(":app")
''')

wf("build.gradle.kts", '''plugins {
    id("com.android.application") version "8.6.1" apply false
    id("org.jetbrains.kotlin.android") version "2.0.20" apply false
}
''')

wf("gradle.properties", '''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
''')

wf("app/proguard-rules.pro", "# Platen\n")

wf("app/build.gradle.kts", '''plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "com.abbasebrahimi.platen"
    compileSdk = 35
    defaultConfig {
        applicationId = "com.abbasebrahimi.platen"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
    }
    signingConfigs {
        create("release") {
            val ks = rootProject.file("release.keystore")
            if (ks.exists()) {
                storeFile = ks
                storePassword = System.getenv("KEYSTORE_PASS") ?: "platen2026"
                keyAlias = System.getenv("KEY_ALIAS") ?: "platen"
                keyPassword = System.getenv("KEY_PASS") ?: "platen2026"
            }
        }
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            val ks = rootProject.file("release.keystore")
            if (ks.exists()) signingConfig = signingConfigs.getByName("release")
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
}
dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("androidx.activity:activity-ktx:1.9.2")
}
''')

wf("app/src/main/AndroidManifest.xml", '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.VIBRATE" />
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.Platen">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustResize"
            android:configChanges="orientation|screenSize|screenLayout|smallestScreenSize|keyboardHidden|keyboard|uiMode">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths" />
        </provider>
    </application>
</manifest>
''')

wf("app/src/main/res/xml/file_paths.xml", '<?xml version="1.0" encoding="utf-8"?><paths><cache-path name="shared_images" path="shared/" /></paths>\n')
wf("app/src/main/res/values/strings.xml", '<?xml version="1.0" encoding="utf-8"?><resources><string name="app_name">Platen</string></resources>\n')
wf("app/src/main/res/values/colors.xml", '<?xml version="1.0" encoding="utf-8"?><resources><color name="ic_launcher_background">#16100C</color><color name="platen_day_bg">#E6DECB</color></resources>\n')
wf("app/src/main/res/values/themes.xml", '''<?xml version="1.0" encoding="utf-8"?>
<resources><style name="Theme.Platen" parent="Theme.AppCompat.DayNight.NoActionBar">
<item name="android:statusBarColor">@color/platen_day_bg</item>
<item name="android:navigationBarColor">@color/platen_day_bg</item>
<item name="android:windowLightStatusBar">true</item>
</style></resources>
''')
wf("app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml", '<?xml version="1.0" encoding="utf-8"?><adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/ic_launcher_background"/><foreground android:drawable="@drawable/ic_launcher_foreground"/></adaptive-icon>\n')
wf("app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml", '<?xml version="1.0" encoding="utf-8"?><adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/ic_launcher_background"/><foreground android:drawable="@drawable/ic_launcher_foreground"/></adaptive-icon>\n')

wf("app/src/main/java/com/abbasebrahimi/platen/MainActivity.kt", '''package com.abbasebrahimi.platen

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.net.Uri
import android.os.*
import android.print.PrintAttributes
import android.print.PrintManager
import android.util.Base64
import android.webkit.*
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import androidx.core.view.WindowInsetsControllerCompat
import java.io.File
import java.io.FileOutputStream

class MainActivity : AppCompatActivity() {
    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        webView = WebView(this)
        setContentView(webView)
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true
            allowFileAccess = true
            allowContentAccess = true
            mediaPlaybackRequiresUserGesture = false
            useWideViewPort = true
            loadWithOverviewMode = true
        }
        webView.webViewClient = WebViewClient()
        webView.webChromeClient = WebChromeClient()
        webView.addJavascriptInterface(PlatenBridge(this, webView), "PlatenBridge")
        webView.loadUrl("file:///android_asset/index.html")

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                webView.evaluateJavascript("window.platenHandleBack && window.platenHandleBack()") { res ->
                    if (res != "true") { isEnabled = false; onBackPressedDispatcher.onBackPressed(); isEnabled = true }
                }
            }
        })
    }

    inner class PlatenBridge(private val ctx: Context, private val wv: WebView) {
        @JavascriptInterface fun vibrate(ms: Long) {
            try {
                val d = ms.coerceIn(5L, 80L)
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                    (ctx.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as VibratorManager).defaultVibrator
                        .vibrate(VibrationEffect.createOneShot(d, VibrationEffect.DEFAULT_AMPLITUDE))
                } else {
                    @Suppress("DEPRECATION")
                    val v = ctx.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) v.vibrate(VibrationEffect.createOneShot(d, VibrationEffect.DEFAULT_AMPLITUDE))
                    else @Suppress("DEPRECATION") v.vibrate(d)
                }
            } catch (_: Exception) {}
        }
        @JavascriptInterface fun setTheme(theme: String) {
            runOnUiThread {
                val night = theme == "night"
                val c = if (night) Color.parseColor("#120E0B") else Color.parseColor("#E6DECB")
                window.statusBarColor = c
                window.navigationBarColor = c
                WindowInsetsControllerCompat(window, window.decorView).apply {
                    isAppearanceLightStatusBars = !night
                    isAppearanceLightNavigationBars = !night
                }
            }
        }
        @JavascriptInterface fun shareText(title: String, text: String) {
            startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply {
                type = "text/plain"; putExtra(Intent.EXTRA_SUBJECT, title); putExtra(Intent.EXTRA_TEXT, text)
            }, title))
        }
        @JavascriptInterface fun shareImageBase64(dataUrl: String, fileName: String) {
            try {
                val bytes = Base64.decode(dataUrl.substringAfter("base64,", dataUrl), Base64.DEFAULT)
                val dir = File(ctx.cacheDir, "shared").apply { mkdirs() }
                val file = File(dir, fileName)
                FileOutputStream(file).use { it.write(bytes) }
                val uri = FileProvider.getUriForFile(ctx, "${ctx.packageName}.fileprovider", file)
                startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply {
                    type = "image/png"; putExtra(Intent.EXTRA_STREAM, uri); addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }, "Share Platen Sheet"))
            } catch (_: Exception) {}
        }
        @JavascriptInterface fun printPage(jobName: String) {
            runOnUiThread {
                try {
                    val pm = ctx.getSystemService(Context.PRINT_SERVICE) as PrintManager
                    pm.print(jobName, wv.createPrintDocumentAdapter(jobName), PrintAttributes.Builder().build())
                } catch (_: Exception) {}
            }
        }
        @JavascriptInterface fun openUrl(url: String) {
            try { startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) } catch (_: Exception) {}
        }
    }
}
''')

make_vintage_icon()
print("Built Android skeleton & vintage icons successfully!")
