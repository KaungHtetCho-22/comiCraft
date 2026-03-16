/**
 * Internationalization (i18n) Module
 * Supports Chinese and English language switching
 */

const i18n = {
    // Current language
    currentLang: 'en',

    // Translation dictionary
    translations: {
        en: {
            // Page title
            pageTitle: 'comic-perfect',

            // Main header
            appName: 'ComicCraft AI',
            configBtn: '⚙️ Config',
            themeLabel: 'Theme',
            themeBtnLight: 'Light',
            themeBtnDark: 'Dark',
            languageLabelShort: 'Language',

            // Configuration panel
            configTitle: 'Environment Configuration',
            googleApiKeyLabel: 'Gemini API Key',
            googleApiKeyPlaceholder: 'Enter your Gemini API Key',
            saveConfigBtn: '💾 Save Config',

            // AI generation section
            promptPlaceholder: 'Describe the comic you want, e.g.: Generate a story about a shy robot learning to dance',
            pageCountLabel: 'Pages:',
            rowsPerPageLabel: 'Rows per Page:',
            comicStyleLabel: 'Comic Style:',
            comicLanguageLabel: 'Language:',
            generateBtn: '✨ Generate Comic',
            generating: 'Generating...',

            // Prompt optimization
            optimizePromptTitle: 'Optimize Prompt',
            statusOptimizeSuccess: 'Prompt optimized',
            alertEmptyPrompt: 'Please enter content first',
            alertOptimizeFailed: 'Optimization failed: {error}',

            // Comic styles
            styleDoraemon: 'Doraemon Style',
            styleAmerican: 'American Comic Style',
            styleWatercolor: 'Watercolor Style',
            styleDisney: 'Disney Animation Style',
            styleGhibli: 'Ghibli/Miyazaki Style',
            stylePixar: 'Pixar Animation Style',
            styleShonen: 'Japanese Shonen Manga Style',
            styleTomAndJerry: 'Tom and Jerry Style',
            styleNezha: 'Nezha Style',
            styleLanglangshan: 'Little Monster of Langlang Mountain Style',

            // Comic languages
            langZh: '中文',
            langEn: 'English',
            langJa: '日本語',
            langMy: 'မြန်မာ',

            // Page navigation
            prevBtn: '←',
            nextBtn: '→',
            pageIndicator: 'Page {current}/{total}',

            // Action buttons
            generateCurrentBtn: '🎨 Generate Current Page',
            generateAllBtn: '🎨 Generate All Pages',
            generateAllText: 'Generate All',
            renderThisPage: 'Render Page',
            btnGenerateCover: 'Generate Cover',
            xiaohongshuBtn: '📱 Generate Twitter Post',
            toggleView: 'Flip View',

            // Export dropdown
            exportBtn: 'Export',
            exportText: 'Export',
            xiaohongshuMenuItem: 'Generate Social Post',
            socialMediaContent: 'Generate Social Post',

            // Edit hint
            editHint: 'Click any panel to edit content directly',
            doubleClickToEdit: 'Double-click to edit script',

            // Empty state
            emptyStateTitle: 'Start Creating Your Comic',
            emptyStateDesc: 'Describe your story below, and AI will generate beautiful comic panels for you',
            emptyStep1: 'Describe Story',
            emptyStep2: 'AI Generates',
            emptyStep3: 'Render Images',

            // Status messages
            statusGenerating: 'Calling {model}...',
            statusSuccess: '✓ Generated successfully! {count} pages',
            statusError: '✗ Generation failed: {error}',
            statusPreparing: 'Preparing sketch...',
            statusGeneratingImage: 'Generating current comic image...',
            statusImageSuccess: '✓ Image generated successfully!',
            statusGeneratingPage: 'Generating page {current}/{total}...',
            statusAllSuccess: '✓ All {total} pages generated successfully!',
            statusXiaohongshu: 'Generating Twitter post...',
            statusXiaohongshuSuccess: '✓ Twitter post generated successfully!',
            statusSocialMedia: 'Generating Twitter post...',
            statusSocialMediaSuccess: '✓ Twitter post generated successfully!',

            // Alerts
            alertNoApiKey: 'Please enter OpenAI API Key',
            alertNoGoogleApiKey: 'Please enter Google API Key in settings',
            alertNoPrompt: 'Please describe the comic you want',
            alertConfigSaved: '✓ Configuration saved',
            alertConfigFailed: 'Configuration save failed',
            alertNoBaseUrl: 'Please enter Base URL',
            alertNoCustomModel: 'Please enter custom model name',
            alertNoPageData: 'No page data to generate',
            alertNoPages: 'No pages to generate',
            alertGenerateAll: 'Will generate all {total} pages, this may take some time. Continue?',
            alertBatchError: 'Error occurred during generation, but successfully generated {success}/{total} pages.\nError: {error}',
            alertBatchFailed: 'Batch generation failed: {error}',
            alertNoComicData: 'Please generate comic content first',
            alertDownloadFailed: 'Download failed, please right-click and save image',
            alertDownloadAlt: 'Cannot auto-download, please right-click and save image in new window',
            alertCopyFailed: 'Copy failed, please copy manually',
            alertFileTooLarge: 'File is too large. Please upload an image smaller than 5MB.',

            // Error messages
            errorJsonFormat: 'JSON format error',
            errorGenerationFailed: 'AI generation failed: {error}\n\nTips:\n1. Make sure backend service is running (python backend/app.py)\n2. Check if Base URL is configured correctly',
            errorImageFailed: 'Image generation failed: {error}\n\nTip: Please make sure backend service is running',

            // Modal titles
            modalGeneratedTitle: 'Generated - {count} pages',
            modalXiaohongshuTitle: '🐦 Twitter Post',
            modalTwitterTitle: '🐦 Twitter Post',
            modalTitleLabel: 'Title:',
            modalContentLabel: 'Content:',
            modalTagsLabel: 'Tags:',

            // Modal buttons
            btnDownloadThis: 'Download This',
            btnDownloadAll: 'Download All',
            btnDownloading: 'Downloading...',
            btnClose: 'Close',
            btnCopyAll: '📋 Copy All',
            btnCopied: '✓ Copied',
            btnDownloadImage: 'Download Image',
            btnCancel: 'Cancel',
            statusGeneratingCover: 'Generating Cover...',
            modalCoverTitle: 'Comic Cover',
            coverCustomTitle: 'Custom Cover Requirements',
            coverCustomOptional: '(Optional)',
            coverCustomPlaceholder: 'For example: Use contrasting colors and dramatic lighting. Left side: crying office worker, Right side: lightning drinking coffee',
            coverCustomGenerate: 'Generate',


            // Session management
            sessionTitle: 'Session Management',
            newSession: 'New Session',
            renameSession: 'Rename',
            deleteSession: 'Delete',
            switchSession: 'Switch',
            sessionName: 'Session Name',
            confirmDeleteSession: 'Are you sure you want to delete this session?',
            defaultSessionName: 'session',
            alertLastSession: 'Cannot delete the last session',
            alertStorageFull: 'Storage quota exceeded. Please delete some sessions or clear browser data.',
            confirmClearAll: 'Are you sure you want to delete all sessions? This cannot be undone.',
            sessionListTitle: 'All Sessions',
            currentSession: 'Current Session',

            // Errors
            // Language switcher
            languageLabel: 'Language',
        },
        my: {
            pageTitle: 'ComicCraft AI',
            appName: 'ComicCraft AI',
            configBtn: '⚙️ ပြင်ဆင်မှုများ',
            themeLabel: 'အပြင်အဆင်',
            themeBtnLight: 'အလင်း',
            themeBtnDark: 'အမှောင်',
            languageLabelShort: 'ဘာသာစကား',
            // Configuration panel
            configTitle: 'စနစ်ပြင်ဆင်မှုများ',
            googleApiKeyLabel: 'Gemini API Key',
            googleApiKeyPlaceholder: 'Gemini API Key ထည့်ပါ',
            saveConfigBtn: '💾 သိမ်းဆည်းမည်',
            promptPlaceholder: 'သင်လိုချင်သော ရုပ်ပြောင်ကို ဖော်ပြပါ၊ ဥပမာ - ကလေးလေးတစ်ယောက် ကျောင်းသွားသော ဇာတ်လမ်း',
            pageCountLabel: 'စာမျက်နှာအရေအတွက်:',
            rowsPerPageLabel: 'တစ်မျက်နှာလျှင် အတန်းအရေအတွက်:',
            comicStyleLabel: 'ရုပ်ပြပုံစံ:',
            comicLanguageLabel: 'ရုပ်ပြဘာသာစကား:',
            generateBtn: '✨ AI ဖြင့် ရုပ်ပြဖန်တီးမည်',
            generating: 'ဖန်တီးနေသည်...',
            optimizePromptTitle: 'Prompt ကို ပိုမိုကောင်းမွန်အောင်လုပ်မည်',
            statusOptimizeSuccess: 'Prompt ကို ပိုမိုကောင်းမွန်အောင်လုပ်ပြီးပါပြီ',
            alertEmptyPrompt: 'ကျေးဇူးပြု၍ အကြောင်းအရာထည့်ပါ',
            alertOptimizeFailed: 'ပိုမိုကောင်းမွန်အောင်လုပ်ခြင်း မအောင်မြင်ပါ: {error}',
            styleDoraemon: 'Doraemon ပုံစံ',
            styleAmerican: 'အမေရိကန်ရုပ်ပြပုံစံ',
            styleWatercolor: 'ရေဆေးပုံစံ',
            styleDisney: 'Disney ကာတွန်းပုံစံ',
            styleGhibli: 'Ghibli ပုံစံ',
            stylePixar: 'Pixar ကာတွန်းပုံစံ',
            styleShonen: 'ဂျပန် Shonen Manga ပုံစံ',
            styleTomAndJerry: 'Tom and Jerry ပုံစံ',
            styleNezha: 'Nezha ပုံစံ',
            styleLanglangshan: 'Langlangshan ဘီလူးလေးပုံစံ',
            langZh: 'တရုတ်',
            langEn: 'အင်္ဂလိပ်',
            langJa: 'ဂျပန်',
            langMy: 'မြန်မာ',
            prevBtn: '← ရှေ့သို့',
            nextBtn: 'နောက်သို့ →',
            pageIndicator: 'စာမျက်နှာ {current}/{total}',
            generateCurrentBtn: '🎨 လက်ရှိစာမျက်နှာကို ဖန်တီးမည်',
            generateAllBtn: '🎨 စာမျက်နှာအားလုံးကို ဖန်တီးမည်',
            generateAllText: 'အားလုံးဖန်တီးမည်',
            renderThisPage: 'ပုံဖော်မည်',
            btnGenerateCover: 'မျက်နှာဖုံးဖန်တီးမည်',
            xiaohongshuBtn: '📱 Twitter Post ဖန်တီးမည်',
            toggleView: 'ကြည့်ရှုမှုပြောင်းမည်',
            exportBtn: 'ထုတ်ယူမည်',
            exportText: 'ထုတ်ယူမည်',
            xiaohongshuMenuItem: 'လူမှုကွန်ရက် Post ဖန်တီးမည်',
            socialMediaContent: 'လူမှုကွန်ရက် Post ဖန်တီးမည်',
            editHint: 'တိုက်ရိုက်ပြင်ဆင်ရန် မည်သည့်အကွက်ကိုမဆို နှိပ်ပါ',
            doubleClickToEdit: 'ဇာတ်ညွှန်းကို ပြင်ဆင်ရန် နှစ်ကြိမ်နှိပ်ပါ',
            emptyStateTitle: 'သင့်ရုပ်ပြကို စတင်ဖန်တီးပါ',
            emptyStateDesc: 'သင့်ဇာတ်လမ်းကို အောက်တွင် ဖော်ပြပါ၊ AI က သင့်အတွက် လှပသော ရုပ်ပြများကို ဖန်တီးပေးပါမည်',
            emptyStep1: 'ဇာတ်လမ်းဖော်ပြရန်',
            emptyStep2: 'AI က ဖန်တီးမည်',
            emptyStep3: 'ရုပ်ပုံများပုံဖော်မည်',
            statusGenerating: '{model} ကို ခေါ်ဆိုနေသည်...',
            statusSuccess: '✓ အောင်မြင်စွာဖန်တီးပြီးပါပြီ။ စာမျက်နှာ {count} မျက်နှာ',
            statusError: '✗ ဖန်တီးခြင်း မအောင်မြင်ပါ: {error}',
            statusPreparing: 'ပုံကြမ်းပြင်ဆင်နေသည်...',
            statusGeneratingImage: 'လက်ရှိရုပ်ပြပုံကို ဖန်တီးနေသည်...',
            statusImageSuccess: '✓ ပုံကို အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ။',
            statusGeneratingPage: 'စာမျက်နှာ {current}/{total} ကို ဖန်တီးနေသည်...',
            statusAllSuccess: '✓ စာမျက်နှာအားလုံး {total} ကို အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ။',
            statusXiaohongshu: 'Twitter post ကို ဖန်တီးနေသည်...',
            statusXiaohongshuSuccess: '✓ Twitter post ကို အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ။',
            statusSocialMedia: 'Twitter post ကို ဖန်တီးနေသည်...',
            statusSocialMediaSuccess: '✓ Twitter post ကို အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ။',
            alertNoApiKey: 'ကျေးဇူးပြု၍ OpenAI API Key ထည့်ပါ',
            alertNoGoogleApiKey: 'ကျေးဇူးပြု၍ ပြင်ဆင်မှုများတွင် Google API Key ထည့်ပါ',
            alertNoPrompt: 'ကျေးဇူးပြု၍ သင်လိုချင်သော ရုပ်ပြအကြောင်း ဖော်ပြပါ',
            alertConfigSaved: '✓ ပြင်ဆင်မှုများ သိမ်းဆည်းပြီးပါပြီ',
            alertConfigFailed: 'ပြင်ဆင်မှုများ သိမ်းဆည်းခြင်း မအောင်မြင်ပါ',
            alertNoBaseUrl: 'ကျေးဇူးပြု၍ အခြေခံ URL ထည့်ပါ',
            alertNoCustomModel: 'ကျေးဇူးပြု၍ စိတ်ကြိုက်မော်ဒယ်အမည်ထည့်ပါ',
            alertNoPageData: 'ဖန်တီးရန် စာမျက်နှာဒေတာ မရှိပါ',
            alertNoPages: 'ဖန်တီးရန် စာမျက်နှာများ မရှိပါ',
            alertGenerateAll: 'စာမျက်နှာအားလုံး {total} ကို ဖန်တီးမည်၊ အချိန်အနည်းငယ်ကြာနိုင်ပါသည်။ ဆက်လုပ်မည်လား?',
            alertBatchError: 'ဖန်တီးနေစဉ် အမှားအယွင်းရှိခဲ့သည်၊ သို့သော် စာမျက်နှာ {success}/{total} ကို အောင်မြင်စွာ ဖန်တီးနိုင်ခဲ့သည်။\nအမှား: {error}',
            alertBatchFailed: 'အစုလိုက်ဖန်တီးခြင်း မအောင်မြင်ပါ: {error}',
            alertNoComicData: 'ကျေးဇူးပြု၍ ရုပ်ပြအကြောင်းအရာကို အရင်ဖန်တီးပါ',
            alertDownloadFailed: 'ဒေါင်းလုဒ်လုပ်ခြင်း မအောင်မြင်ပါ၊ ကျေးဇူးပြု၍ ညာကလစ်နှိပ်ပြီး ပုံကို သိမ်းပါ',
            alertDownloadAlt: 'အလိုအလျောက်ဒေါင်းလုဒ်လုပ်၍မရပါ၊ ကျေးဇူးပြု၍ ညာကလစ်နှိပ်ပြီး ပုံကို ဝင်းဒိုးအသစ်တွင် သိမ်းပါ',
            alertCopyFailed: 'ကူးယူခြင်း မအောင်မြင်ပါ၊ ကျေးဇူးပြု၍ ကိုယ်တိုင်ကူးယူပါ',
            alertFileTooLarge: 'ဖိုင်အရမ်းကြီးနေပါသည်။ ကျေးဇူးပြု၍ 5MB ထက်ငယ်သောပုံကို တင်ပါ။',
            errorJsonFormat: 'JSON ဖောမတ် မှားယွင်းနေသည်',
            errorGenerationFailed: 'AI ဖန်တီးခြင်း မအောင်မြင်ပါ: {error}\n\nအကြံပြုချက်:\n၁။ Backend ဝန်ဆောင်မှု အလုပ်လုပ်နေကြောင်း သေချာပါစေ (python backend/app.py)\n၂။ အခြေခံ URL ကို မှန်ကန်စွာ ပြင်ဆင်ထားခြင်းရှိမရှိ စစ်ဆေးပါ',
            errorImageFailed: 'ပုံဖန်တီးခြင်း မအောင်မြင်ပါ: {error}\n\nအကြံပြုချက်: ကျေးဇူးပြု၍ Backend ဝန်ဆောင်မှု အလုပ်လုပ်နေကြောင်း သေချာပါစေ',
            modalGeneratedTitle: 'ဖန်တီးပြီးပါပြီ - စာမျက်နှာ {count}',
            modalXiaohongshuTitle: '📱 Twitter Post',
            modalTwitterTitle: '🐦 Twitter 帖子',
            modalTitleLabel: 'ခေါင်းစဉ်:',
            modalContentLabel: 'အကြောင်းအရာ:',
            modalTagsLabel: 'တဂ်များ:',
            btnDownloadThis: 'ဒေါင်းလုဒ်လုပ်မည်',
            btnDownloadAll: 'အားလုံးကို ဒေါင်းလုဒ်လုပ်မည်',
            btnDownloading: 'ဒေါင်းလုဒ်လုပ်နေသည်...',
            btnClose: 'ပိတ်မည်',
            btnCopyAll: '📋 အားလုံးကို ကူးယူမည်',
            btnCopied: '✓ ကူးယူပြီးပါပြီ',
            btnDownloadImage: 'ပုံကို ဒေါင်းလုဒ်လုပ်မည်',
            btnCancel: 'ပယ်ဖျက်မည်',
            statusGeneratingCover: 'မျက်နှာဖုံး ဖန်တီးနေသည်...',
            modalCoverTitle: 'ရုပ်ပြမျက်နှာဖုံး',
            coverCustomTitle: 'စိတ်ကြိုက် မျက်နှာဖုံး လိုအပ်ချက်များ',
            coverCustomOptional: '(ရွေးချယ်နိုင်သည်)',
            coverCustomPlaceholder: 'ဥပမာ - ကလေးလေးတစ်ယောက် ကျောင်းသွားသော ဇာတ်လမ်းကို ပုံဖော်ပေးပါ',
            coverCustomGenerate: 'ဖန်တီးမည်',
            sessionTitle: 'Session စီမံခန့်ခွဲမှု',
            newSession: 'Session အသစ်',
            renameSession: 'အမည်ပြောင်းမည်',
            deleteSession: 'ဖျက်မည်',
            switchSession: 'ပြောင်းမည်',
            sessionName: 'Session အမည်',
            confirmDeleteSession: 'ဤ session ကို ဖျက်ရန် သေချာပါသလား?',
            defaultSessionName: 'session',
            alertLastSession: 'နောက်ဆုံး session ကို ဖျက်၍မရပါ',
            alertStorageFull: 'သိုလှောင်မှု ပြည့်နေပါသည်။ ကျေးဇူးပြု၍ session အချို့ကို ဖျက်ပါ သို့မဟုတ် ဘရောက်ဆာဒေတာကို ရှင်းလင်းပါ။',
            confirmClearAll: 'session အားလုံးကို ဖျက်ရန် သေချာပါသလား? ဤလုပ်ဆောင်ချက်ကို ပြန်လည်ရုပ်သိမ်း၍မရပါ။',
            sessionListTitle: 'Session အားလုံး',
            currentSession: 'လက်ရှိ Session',
            languageLabel: 'Language / ဘာသာစကား',
        }
    },

    /**
     * Initialize i18n with saved language preference
     */
    init() {
        const savedLang = localStorage.getItem('comic-perfect-lang') || 'en';
        this.setLanguage(savedLang);
    },

    /**
     * Get translation for a key
     * @param {string} key - Translation key
     * @param {Object} params - Parameters to replace in translation
     * @returns {string} Translated text
     */
    t(key, params = {}) {
        let text = this.translations[this.currentLang][key] || key;

        // Replace parameters
        Object.keys(params).forEach(param => {
            text = text.replace(`{${param}}`, params[param]);
        });

        return text;
    },

    /**
     * Set current language
     * @param {string} lang - Language code ('zh' or 'en')
     */
    setLanguage(lang) {
        if (!this.translations[lang]) {
            console.warn(`Language ${lang} not supported, falling back to en`);
            lang = 'en';
        }

        this.currentLang = lang;
        localStorage.setItem('comic-perfect-lang', lang);
        this.updateUI();
    },

    /**
     * Get current language
     * @returns {string} Current language code
     */
    getLanguage() {
        return this.currentLang;
    },

    /**
     * Update all UI text elements
     */
    updateUI() {
        // Update page title
        document.title = this.t('pageTitle');

        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const params = element.getAttribute('data-i18n-params');

            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = this.t(key, params ? JSON.parse(params) : {});
            } else if (element.tagName === 'OPTION') {
                element.textContent = this.t(key);
            } else {
                element.innerHTML = this.t(key, params ? JSON.parse(params) : {});
            }
        });

        // Update elements with data-i18n-tooltip attribute
        document.querySelectorAll('[data-i18n-tooltip]').forEach(element => {
            const key = element.getAttribute('data-i18n-tooltip');
            const params = element.getAttribute('data-i18n-params');
            element.setAttribute('data-tooltip', this.t(key, params ? JSON.parse(params) : {}));
        });

        // Trigger custom event for components that need to update
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: this.currentLang } }));

        // Update theme button title if theme manager exists
        if (window.themeManager) {
            window.themeManager.updateThemeButton();
        }
    }
};

// Initialize on load
if (typeof window !== 'undefined') {
    window.i18n = i18n;
}
