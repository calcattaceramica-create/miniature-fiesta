/**
 * Auto switch to Arabic language
 */
document.addEventListener('DOMContentLoaded', function() {
    // Check if current language is not Arabic
    const currentLang = document.documentElement.lang;
    
    if (currentLang !== 'ar') {
        // Auto redirect to Arabic
        console.log('Auto switching to Arabic...');
        window.location.href = '/auth/change-language/ar';
    }
});

